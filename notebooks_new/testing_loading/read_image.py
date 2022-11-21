# -*- coding: utf-8 -*-
"""
Created on Mon Nov 14 09:02:55 2022

@author: jonat
"""
import pandas as pd
import torch
import numpy as np
import os

metaDataPath_100000 = 'dataset_100000.csv'
#dataPath = '\singh_cp_pipeline_singlecell_images'
print("path: {}".format(os.getcwd())) #this should be in 'notebooks_new\testing_loading' directory. If not change the remaining directories to fit yours
os.chdir('..\..\data\Subset_CSVs')
print("new path: {}".format(os.getcwd())) #This should be in 'Subset_CSVs' directory

subset = pd.read_csv(metaDataPath_100000,sep = ';', header = 0)

os.chdir('..\singh_cp_pipeline_singlecell_images')
print("new path: {}".format(os.getcwd())) #This should be in working directory 'singh_cp_pipeline_singlecell_images' folder
subset['Images'] = subset.apply(lambda row: torch.tensor(np.load(f"{row.Multi_Cell_Image_Name}\{row.Multi_Cell_Image_Name}_{row.Single_Cell_Image_Id}.npy").tolist()), axis=1)

data = subset[['Images','moa']].copy()
data.to_pickle("..\Subset_CSVs\data_100000_images.pkl")
