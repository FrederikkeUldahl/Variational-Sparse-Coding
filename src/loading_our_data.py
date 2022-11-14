import numpy as np
from torch.utils.data import DataLoader
import os
import pickle
import pandas as pd
import matplotlib.pyplot as plt
import torch
from torch.utils.data import Dataset

# Loading pickle file 
data_pickle = open ('data\data_1000_images', 'rb')
data = pickle.load(data_pickle)

# Class for dataset
class BBBC(Dataset):
    def __init__(self, annotations_file,typeFlag, transform=None, target_transform=None):
        self.transform = transform
        self.target_transform = target_transform
        
        train_size = int(np.ceil(0.8*annotations_file.shape[0]))
        test_size = int(annotations_file.shape[0]-train_size)

        if typeFlag == 'train':
          img_labels = annotations_file.head(train_size)
        elif typeFlag == 'test':
          img_labels = annotations_file.head(-test_size)
        
        self.img_labels = img_labels

    def __len__(self):
        return len(self.img_labels)

    def __getitem__(self, idx):
        image = self.img_labels.iloc[idx, 0]
        
        label = self.img_labels.iloc[idx, 1]
        
        if self.transform:
            image = self.transform(image)
        if self.target_transform:
            label = self.target_transform(label)
        
        return image, label

dset_train = BBBC(data,"train")
dset_test = BBBC(data,"test")

batch_size = 30

train_loader = DataLoader(dset_train,batch_size=batch_size)
test_loader = DataLoader(dset_test,batch_size=batch_size)

print(type(dset_train))       # <class '__main__.BBBC'>
print(type(dset_train[0]))    # <class 'tuple'>
print(type(dset_train[0][0])) # <class 'torch.Tensor'>
print(type(dset_train[0][1])) # <class 'int'>, but currently it is <class 'str'>