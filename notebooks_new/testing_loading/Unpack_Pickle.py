# -*- coding: utf-8 -*-
"""
Created on Mon Nov 14 11:42:02 2022

@author: jonat
"""

import pandas as pd
import torch
import numpy as np
import os
import pickle

os.chdir('..\..\data\Subset_CSVs')
data_pickle = open ("data_1000_images.pkl", "rb")
data_content = pickle.load(data_pickle)
print(data_content.head())