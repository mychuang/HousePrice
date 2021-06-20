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





