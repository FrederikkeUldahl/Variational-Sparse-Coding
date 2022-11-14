import pandas as pd

df = pd.read_csv(r'C:\Users\johan\OneDrive - Danmarks Tekniske Universitet\5. semester eft 2022\02456 Deep Learning\metadata.csv')
print(df)

from sklearn.model_selection import train_test_split

rest, dataset = train_test_split(df, test_size=0.20)

print(dataset) #100.000 rows

#print to new csv
data = dataset.to_csv('data.csv', index = True)
print('\nCSV String:\n', dataset) #bliver lagt i Variational sparse encoding som "data.csv" er meget random
