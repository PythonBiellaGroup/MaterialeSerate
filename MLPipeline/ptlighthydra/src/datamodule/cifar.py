from typing import Optional

import pytorch_lightning as pl
from torch.utils.data import DataLoader, random_split
import torchvision.transforms as transforms
from ptlighthydra.src.datasets.cifar import CIFAR10

'''
A DataModule standardizes the training, val, test splits, data preparation and transforms. 
The main advantage is consistent data splits, data preparation and transforms across models.

This allows you to share a full dataset without explaining how to download, split, 
transform, and process the data
'''


class CIFAR10DataModule(pl.LightningDataModule):
    def __init__(self, data_dir='../../data', batch_size=64, train_val_split=None):
        super().__init__()

        self.transform = transforms.Compose(
            [transforms.ToTensor(),
             transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])

        self.batch_size = batch_size
        self.data_dir = data_dir

        if train_val_split is None:
            train_val_split = [45000, 5000]
        self.split_size = train_val_split

    def setup(self, stage: Optional[str] = None) -> None:
        # Assign train/val datasets for use in dataloaders
        if stage == "fit" or stage is None:
            cifar_full = CIFAR10(self.data_dir, train=True, transform=self.transform)
            self.cifar_train, self.cifar_val = random_split(cifar_full, self.split_size)

        # Assign test dataset for use in dataloader(s)
        if stage == "test" or stage is None:
            self.cifar_test = CIFAR10(self.data_dir, train=False, transform=self.transform)

    def train_dataloader(self):
        return DataLoader(self.cifar_train, batch_size=self.batch_size)

    def val_dataloader(self):
        return DataLoader(self.cifar_val, batch_size=self.batch_size)

    def test_dataloader(self):
        return DataLoader(self.cifar_test, batch_size=self.batch_size)

