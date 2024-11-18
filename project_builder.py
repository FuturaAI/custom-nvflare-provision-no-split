#!/usr/bin/env python3
import os
import sys
from config.generate_nvflare_yaml import create_nvidia_flare_project_config
from config.generate_image_dataset import split_dataset
import time

def get_project_name_interactive():
    """Get project name through interactive prompt."""
    config_breakwords = ['q', 'exit']
    
    print("Project initialization started. To quit the configuration type 'q' or 'exit'")
    project_name = str(input("Insert project folder name: "))
    
    if project_name.lower() in config_breakwords:
        print("Configuration cancelled.")
        return None
        
    return project_name

def wait_for_path(project_name, site_path):  # site_path like "localhost" or "site-1" or "site-2"
    base_path = os.path.join("workspace", project_name, "prod_00", site_path, "local")
    timeout = 10  # 10 seconds
    start_time = time.time()
    
    while not os.path.exists(base_path):
        if time.time() - start_time > timeout:
            raise TimeoutError(f"Timeout waiting for path {base_path} to exist")
        print(f"Waiting for path {base_path} to exist...")
        time.sleep(5)  # Check every 5 seconds
    
    # Once base path exists, create the remaining structure
    full_path = os.path.join(base_path, "images", "split_images")
    os.makedirs(full_path, exist_ok=True)
    return full_path

def main():
    # Check if project name was provided as command line argument
    if len(sys.argv) > 1:
        project_name = sys.argv[1]
    else:
        # If no command line argument, fall back to interactive mode
        project_name = get_project_name_interactive()
    
    # If project name was provided or entered (not cancelled)
    if project_name:
        try:
            create_nvidia_flare_project_config(project_name=project_name)
            print(f"Configuration file created for project: {project_name}")

        except Exception as e:
            print(f"Error during configuration: {e}")
            sys.exit(1)
    else:
        print("No project name provided. Exiting.")
        sys.exit(1)

if __name__ == "__main__":
    main()