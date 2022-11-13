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

#get a data subset from a lable
def get_subset(moa, amount): #not implemented yet
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
        assert len(metadata[metadata['moa'] == moa]) >= amount, "Some moa labels has to few sampels"
        subset = get_subset(moa,amount)
        dataset = pd.concat([dataset,subset], ignore_index=True)
    return(dataset)

#collecting one dataset of all moas
dataset = get_subset_from(moa_types, 10000)
print("full dataset set: {}".format(dataset.shape))

data_tree = get_subset_from(moa_types[0:3], 30)
print("small dataset set: {}".format(data_tree.shape))


