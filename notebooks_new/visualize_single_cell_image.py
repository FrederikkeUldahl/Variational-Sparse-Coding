import numpy as np 
import os
import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt
import random
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 300)

single_img_path = 'data\B02_s1_w16F89C55C-7808-4136-82E4-E066F8E3CB10\B02_s1_w16F89C55C-7808-4136-82E4-E066F8E3CB10'

idx = random.sample(range(1, 200), 9) 
fig, axs = plt.subplots(3, 3)

for i in range(3):
    for j in range(3):
        single_cell_image = np.load(single_img_path + '_{}.npy'.format(idx[(i-1)*3+j]))
        axs[i, j].imshow(single_cell_image/single_cell_image.max(axis=(0,1)))

plt.imshow(single_cell_image/single_cell_image.max(axis=(0,1)))
plt.show()