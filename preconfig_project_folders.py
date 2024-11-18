import os
import sys
import json
import glob
from config.generate_image_dataset import split_dataset, split_sites
import time
import shutil

def find_latest_prod_dir(project_name):
    workspace_path = os.path.join("workspace", project_name)
    if not os.path.exists(workspace_path):
        return None
    prod_dirs = glob.glob(os.path.join(workspace_path, "prod_*"))
    return os.path.basename(max(prod_dirs, key=lambda x: int(x.split('_')[-1]))) if prod_dirs else "prod_00"

def update_and_rename_resources_file(project_name, prod_dir, site_path):
    resources_default = os.path.join("workspace", project_name, prod_dir, site_path, "local", "resources.json.default")
    resources_json = os.path.join("workspace", project_name, prod_dir, site_path, "local", "resources.json")
    
    if os.path.exists(resources_default):
        with open(resources_default, 'r') as f:
            data = json.load(f)
        
        for component in data['components']:
            if component['id'] == 'resource_manager':
                component['args']['num_of_gpus'] = 1
                component['args']['mem_per_gpu_in_GiB'] = 6
        
        with open(resources_json, 'w') as f:
            json.dump(data, f, indent=2)
        
        os.remove(resources_default)

def wait_for_path(project_name, prod_dir, site_path):
    base_path = os.path.join("workspace", project_name, prod_dir, site_path, "local")
    timeout = 10
    start_time = time.time()
    
    while not os.path.exists(base_path):
        if time.time() - start_time > timeout:
            raise TimeoutError(f"Timeout waiting for path {base_path} to exist")
        print(f"Waiting for path {base_path} to exist...")
        time.sleep(5)
    
    full_path = os.path.join(base_path, "images", "split_images")
    os.makedirs(full_path, exist_ok=True)
    return full_path

def main():
    if len(sys.argv) != 2:
        print("Error: Project name not provided!")
        print("Usage: python prebuild_images_split.py <project_name>")
        sys.exit(1)
        
    project_name = sys.argv[1]
    prod_dir = find_latest_prod_dir(project_name)
    
    update_and_rename_resources_file(project_name, prod_dir, "site-1")
    update_and_rename_resources_file(project_name, prod_dir, "site-2")
    
    split_images_output_dir_site1 = wait_for_path(project_name, prod_dir, "site-1")
    split_images_output_dir_site2 = wait_for_path(project_name, prod_dir, "site-2")

    # First split data between sites
    site_folders = split_sites("images", num_sites=2)
    
    # Then split each site's data into train/val/test
    split_dataset(site_folders[0], split_images_output_dir_site1)
    split_dataset(site_folders[1], split_images_output_dir_site2)

    # Clean up temporary site folders
    for folder in site_folders:
        if os.path.exists(folder):
            shutil.rmtree(folder)

if __name__ == "__main__":
    main()