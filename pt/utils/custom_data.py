import os
from torch.utils.data import Dataset
from PIL import Image

IMAGE_PATH = 'split_images'
IMAGES_ROOT = os.path.join(os.getcwd(), 'local/images/', IMAGE_PATH)

class CustomDataset(Dataset):
    def __init__(self, data_folder, transform=None):
        self.data_folder = data_folder
        self.transform = transform
        
        self.class_names = sorted(os.listdir(data_folder))
        self.class_to_idx = {class_name: idx for idx, class_name in enumerate(self.class_names)}
        
        self.image_paths = []
        self.labels = []
        
        for class_name in self.class_names:
            class_folder = os.path.join(data_folder, class_name)
            class_label = self.class_to_idx[class_name]
            
            for filename in os.listdir(class_folder):
                img_path = os.path.join(class_folder, filename)
                self.image_paths.append(img_path)
                self.labels.append(class_label)
    
    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, idx):
        img_path = self.image_paths[idx]
        image = Image.open(img_path)
        label = self.labels[idx]

        if self.transform:
            image = self.transform(image)

        return image, label