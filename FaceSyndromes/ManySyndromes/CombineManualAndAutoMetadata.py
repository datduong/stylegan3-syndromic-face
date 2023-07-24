

import os,sys,re
import numpy as np
import pandas as pd 

# ! possible that we don't have manual metadata. 

maindir = '/data/duongdb/ManyFaceConditions08172022'
# fout = 'TrimImg_no_bg_0pix_align08172022_manual_auto_age_gender_race.csv'
auto_label = 'TrimImg_no_bg_0pix_align08172022_auto_age_gender_race_formated.csv' # ! note, using black pixel with fairface
fout = 'TrimImg_255pix_align08172022_manual_auto_age_gender_race.csv'

newpath = 'TrimImg_align_255pix'
oldpath = 'TrimImg_no_bg_0pix_align'

df_manual = os.path.join(maindir,'ManualMetaDataLabel.csv')
df_auto = os.path.join(maindir, auto_label)

df_manual = pd.read_csv(df_manual)
df_auto = pd.read_csv(df_auto)

print (df_manual.shape[0])
print (df_auto.shape[0])

df = df_manual.merge(df_auto,on='name',how="left").fillna('none')

df = df[df['name'] != 'none'].reset_index(drop=True)

# count 
print (df['Condition'].value_counts()) 

# ---------------------------------------------------------------------------- #
# ! fill in age group

print (set ( df['Age'] ) ) 
# >>> set (df['Age']) {'adolescence', 'not', 'youngchild', 'youngadult', '2y', 'olderadult'}

# (1) under 2 years old, (2) 2-9 years old, (3) 10-19 years old, (4) 20-34 years old, and (5) ≥35 years old.

for index,row in df.iterrows(): 
  if row['name'] == 'none': 
    continue
  # 
  if (row['Age'] == 'not') and (row['Expected_Age'] != 'none'): 
    if row['Expected_Age'] <= 2: 
      row['Age'] = '2y'
    elif (row['Expected_Age'] < 2) and (row['Expected_Age'] < 10): 
      row['Age'] = 'youngchild'
    elif (row['Expected_Age'] <= 10) and (row['Expected_Age'] < 20): 
      row['Age'] = 'adolescence'
    elif (row['Expected_Age'] <= 20) and (row['Expected_Age'] < 35): 
      row['Age'] = 'youngadult'
    else: 
      row['Age'] = 'olderadult'
  # 
  if (row['gender'] == -1) and (row['Female'] != 'none') : 
    if row['Female'] > 0.5: 
      row['gender'] = 1 # female = 1
    else: 
      row['gender'] = 0 


#
print (set ( df['Age'] ) ) 
print (set ( df['gender'] ) ) 

# ---------------------------------------------------------------------------- #

# ! replace path if needed
if newpath is not None: 
  temp = [re.sub(oldpath,newpath,i) for i in df['path'].values ]
  df['path'] = temp 


# ! check path exists 
df['validpath'] = [os.path.exists(i) for i in df['path'].values ]
df = df [ df['validpath'] == True ].reset_index(drop=True)

  
# 
df.to_csv(os.path.join(maindir,fout),index=None)

# ! count again after checking valid path
print (df['Condition'].value_counts()) 

