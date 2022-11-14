# -*- coding: utf-8 -*-
"""
Created on Sun Nov 13 13:57:51 2022

@author: jonat
"""

from typing import *
import numpy as np 
import os
import pandas as pd
import seaborn as sns
from PIL import Image
import matplotlib
import matplotlib.pyplot as plt
from IPython.display import Image, display, clear_output
import random
import math

#Load metadata-----------
dataPath = '..\..\..\data\singh_cp_pipeline_singlecell_images'
metaDataPath = '..\..\data'

#reading metadata csv
metadata = pd.read_csv(metaDataPath + '\metadata.csv', sep = ';', header = 0)
print(metadata.shape)

#testing for moa lable distributions
moas = metadata.moa
moa_types = moas.unique()
print("moa length: {}".format(len(moas)))
print("uniqe moa length: {}".format(len(moa_types)))

for moa in moa_types:
    moa_count = metadata[metadata['moa'] == moa]
    print("moa {} has: {}".format(moa, len(moa_count)))


#get an equaly distributed data set of one moa over folders
''' not in use
def get_distributed_subset(folders, size, data):
    #getting the number of samples from all folders
    amount = math.floor(size/len(folders))
    #getting the number of folder that need to have more representitives
    add = size % len(folders)
    #collecting the data
    dist_set = pd.DataFrame()
    for i in range(len(folders)):
        folder_subset = data[data['Multi_Cell_Image_Name'] == folders[i]]
        if i < add:
            idx = random.sample(range(0, len(folder_subset)), amount+1) #if the modulus should be added
        else:
            idx = random.sample(range(0, len(folder_subset)), amount) #if the modulus should not be added
        folder_subset = folder_subset.iloc[idx]
        dist_set = pd.concat([dist_set,folder_subset], ignore_index=True)
    return(dist_set)
'''  
  
#find the folders with the moa lable
''' not in use
def get_moa_folders(moa):
    moas = metadata[metadata['moa'] == moa]
    folders = moas.Multi_Cell_Image_Name
    folders = folders.unique()
    return(folders)
'''

#get a data subset from a lable
def get_subset(moa, amount):
    moas = metadata[metadata['moa'] == moa]
    moa_count = len(moas)
    idx = random.sample(range(0, moa_count), amount)
    subset = moas.iloc[idx]
    return(subset)

#get a specific sized dataset from the wanted moa lables
def get_subset_from(moas, size):
    amount = math.ceil(size/len(moas))
    dataset = pd.DataFrame()
    for moa in moas:
        #assert len(metadata[metadata['moa'] == moa]) >= amount, "Some moa labels has to few sampels"
        #if there is not enugh we take what we have
        if len(metadata[metadata['moa'] == moa]) < amount:
            subset = get_subset(moa,len(metadata[metadata['moa'] == moa]))
        else:
            subset = get_subset(moa,amount)
        #collecting the dataset
        dataset = pd.concat([dataset,subset], ignore_index=True)
    return(dataset)

#collecting one dataset of all moas
dataset_100000 = get_subset_from(moa_types, 100000)
print("100.000 real length: {}".format(len(dataset_100000)))

#collecting one dataset of all moas
dataset_10000 = get_subset_from(moa_types, 10000)
print("10.000 real length: {}".format(len(dataset_10000)))

#collecting one dataset of all moas
dataset_1000 = get_subset_from(moa_types, 1000)
print("1000 real length: {}".format(len(dataset_1000)))

'''
print("path: {}".format(os.getcwd()))
os.chdir(metaDataPath + '\Subset_CSVs')
print("new path: {}".format(os.getcwd()))
dataset_100000.to_csv('dataset_100000.csv',sep=';')
dataset_10000.to_csv('dataset_10000.csv',sep=';')
dataset_1000.to_csv('dataset_1000.csv',sep=';')
'''
