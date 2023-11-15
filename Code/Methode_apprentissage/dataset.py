from PIL import Image
import os
from torch.utils.data import Dataset
import numpy as np


class MaleFemaleDataset(Dataset):
    def __init__(self, root_male, root_female, transform=None):
        self.root_male = root_male
        self.root_female = root_female
        self.transform = transform

        self.male_images = os.listdir(root_male)
        self.female_images = os.listdir(root_female)
        self.length_dataset = max(len(self.male_images), len(self.female_images))
        self.male_len = len(self.male_images)
        self.female_len = len(self.female_images)

    def __len__(self):
        return self.length_dataset

    def __getitem__(self, index):
        male_img = self.male_images[index % self.male_len]
        female_img = self.female_images[index % self.female_len]

        male_path = os.path.join(self.root_male, male_img)
        female_path = os.path.join(self.root_female, female_img)

        male_img = np.array(Image.open(male_path).convert("RGB"))
        female_img = np.array(Image.open(female_path).convert("RGB"))

        if self.transform:
            augmentations = self.transform(image=male_img, image0=female_img)
            male_img = augmentations["image"]
            female_img = augmentations["image0"]

        return male_img, female_img
