import pandas as pd
import os

list_path = []
os.chdir("/home/pengyuan/PycharmProjects/NASA_2018/")
for root, dirs, files in os.walk(".", topdown = False):
   for name in files:
     file_path = os.path.join(root, name)
     list_path.append(file_path)
print(list_path)
   # for name in dirs:
   #    print(os.path.join(root, name))

df = pd.DataFrame(list_path)
df.to_csv('./image_path.csv')


