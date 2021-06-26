# -*- coding: utf-8 -*-
"""
Created on Mon Jun 14 15:22:09 2021

@author: Miller
"""
import requests
import os
import zipfile
import time
import pandas as pd

#%%
def real_estate_crawler(year, season):
  if year > 1000:
    year -= 1911

  # download real estate zip content
  res = requests.get("https://plvr.land.moi.gov.tw//DownloadSeason?season="+str(year)+"S"+str(season)+"&type=zip&fileName=lvr_landcsv.zip")

  # save content to file
  print("save zip file")
  fname = str(year)+str(season)+'.zip'
  open(fname, 'wb').write(res.content)

   #make additional folder for files to extract
  folder = 'real_estate' + str(year) + str(season)
  if not os.path.isdir(folder):
    os.mkdir(folder)

   # extract files to the folder
  print("extract zip file")
  with zipfile.ZipFile(fname, 'r') as zip_ref:
      zip_ref.extractall(folder)

  time.sleep(3)
#-----------------------------------------------------
for year in range(102, 109):
  for season in range(1,5):
    print(year, season)
    real_estate_crawler(year, season)

real_estate_crawler(110, 1)

#%%
# import folders
dirs = [d for d in os.listdir() if d[:4] == 'real']
dfs = []

#----- data csv commment -----
#  $_lvr_land_%.csv
#  $: a~z : implies cities
#  %: a: house trade; b: new house trade; c: rent trade
#-----------------------------
# test for a group (台北市)
#
for d in dirs:
    print("import folder: ", d)
    df = pd.read_csv(os.path.join(d,'a_lvr_land_a.csv'), index_col=False)
    df['Q'] = d[-1]
    dfs.append(df.iloc[1:])
df = pd.concat(dfs, sort=True)

#%%
# data processing
# (1) create trading year
df['year'] = df['交易年月日'].str[:-4].astype(int) + 1911

# (2) combine data
if '單價元/平方公尺' in df.columns:
    df['單價元平方公尺'].fillna(df['單價元/平方公尺'], inplace=True)
    df.drop(columns='單價元/平方公尺')
    
# (3) convert m^2 to level ground
df['單價元平方公尺'] = df['單價元平方公尺'].astype(float)
df['單價元坪'] = df['單價元平方公尺'] * 3.30579

# (4) type of building
df['建物型態2'] = df['建物型態'].str.split('(').str[0]

# (5) delete unnomal data
df = df[df['備註'].isnull()]

# (6) change index
df.index = pd.to_datetime((df['交易年月日'].str[:-4].astype(int) + 1911).astype(str) + \
                          df['交易年月日'].str[-4:] ,errors='coerce')
    
#%%
#from matplotlib import font_manager
from matplotlib.font_manager import *
import numpy as np
import matplotlib.pyplot as plt

myfont = FontProperties(fname='msjh.ttc')

prices = {}
for district in set(df['鄉鎮市區']):
    cond = (
        (df['主要用途'] == '住家用')
        & (df['鄉鎮市區'] == district)
        & (df['單價元坪'] < df["單價元坪"].quantile(0.95))
        & (df['單價元坪'] > df["單價元坪"].quantile(0.05))
        )
    groups = df[cond]['year']
    
    prices[district] = df[cond]['單價元坪'].astype(float).groupby(groups).mean().loc[2012:2020]
    
fig, ax = plt.subplots()
price_history = pd.DataFrame(prices)
price_history.plot(ax =ax)
ax.legend(prop = myfont)






















