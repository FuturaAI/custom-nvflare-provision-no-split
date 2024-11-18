import splitfolders
import os
import shutil

def split_sites(input_folder, num_sites=2, seed=42):
    """
    Split dataset into different sites before train/val/test splitting.
    
    Parameters:
    input_folder (str): Path to input folder containing label subfolders
    num_sites (int): Number of sites to split data between
    seed (int): Random seed for reproducibility
    """
    
    label_folders = os.listdir(input_folder)
    
    for site in range(1, num_sites + 1):
        site_folder = f"{input_folder}_{site}"
        os.makedirs(site_folder, exist_ok=True)
        
        for label in label_folders:
            src_label_path = os.path.join(input_folder, label)
            dst_label_path = os.path.join(site_folder, label)
            os.makedirs(dst_label_path, exist_ok=True)
            
            # Get all images for this label
            images = os.listdir(src_label_path)
            
            # Calculate slice for this site
            start_idx = ((site-1) * len(images)) // num_sites
            end_idx = (site * len(images)) // num_sites
            site_images = images[start_idx:end_idx]
            
            # Copy images to site folder
            for img in site_images:
                src_path = os.path.join(src_label_path, img)
                dst_path = os.path.join(dst_label_path, img)
                shutil.copy2(src_path, dst_path)
    
    return [f"{input_folder}_{i}" for i in range(1, num_sites + 1)]

def split_dataset(input_folder, output_folder, ratio=(0.7, 0.2, 0.1), seed=42):
    """Split dataset into train/val/test sets"""
    os.makedirs(output_folder, exist_ok=True)
    splitfolders.ratio(
        input=input_folder,
        output=output_folder,
        seed=seed,
        ratio=ratio,
        group_prefix=None
    )

if __name__ == "__main__":
    # First split between sites
    site_folders = split_sites("images", num_sites=2)
    
    # Then split each site's data into train/val/test
    for site_folder in site_folders:
        output_folder = f"split_{site_folder}"
        split_dataset(site_folder, output_folder)