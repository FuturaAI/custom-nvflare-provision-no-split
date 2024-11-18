import splitfolders
import os

def split_dataset(input_folder, output_folder, ratio=(0.7, 0.2, 0.1), seed=42):
    """
    Split a dataset into train, validation, and test sets while maintaining the folder structure.
    
    Parameters:
    input_folder (str): Path to input folder containing category subfolders (cats, dogs)
    output_folder (str): Path where split datasets will be created
    ratio (tuple): Ratio for train, validation, test splits (default: 70%, 20%, 10%)
    seed (int): Random seed for reproducibility
    """
    
    # Create output directory if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    
    # Split the data
    splitfolders.ratio(
        input=input_folder,
        output=output_folder,
        seed=seed,
        ratio=ratio,
        group_prefix=None  # Don't add extra prefix to folders
    )

if __name__ == "__main__":
    # Example usage
    input_folder = "path/to/your/dataset"  # Folder containing 'cats' and 'dogs' subfolders
    output_folder = "path/to/output"       # Where you want the split datasets to be created
    
    # Split with default ratio (70/20/10)
    split_dataset(input_folder, output_folder)