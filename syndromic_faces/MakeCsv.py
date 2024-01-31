
from operator import index
import os,sys,re,pickle
import numpy as np 
import pandas as pd 

def sort_parse_comma_separated_list(s):
  if isinstance(s, list):
    return sorted(s)
  return sorted( s.split(',') ) 

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--filelist", type=sort_parse_comma_separated_list, default='BWS.csv,CdLS.csv,Down.csv,KS.csv,NS.csv,PWS.csv,RSTS1.csv,WHS.csv')
parser.add_argument("--outputname", type=str, default=None)
parser.add_argument("--label", type=str, default=None)
parser.add_argument("--imagepath", type=str, default='/data/duongdb/ManyFaceConditions01072022/Align1024BlankBackgroundCenter')
parser.add_argument("--extracsv", type=sort_parse_comma_separated_list, default=None)
parser.add_argument("--headfolder", type=str, default='/data/duongdb/ManyFaceConditions01072022')

args = parser.parse_args()

# os.chdir('/data/duongdb/ManyFaceConditions01072022')
# filelist = """
# BWS.csv           
# CdLS.csv          
# DownSyndrome.csv  
# KS.csv            
# NS.csv            
# PWS.csv           
# RSTS1.csv         
# WHS.csv""".split()

# ! read csv 
df = [ ] 

for f in args.filelist: #args.
  f = pd.read_csv(os.path.join(args.headfolder,f))
  f = f.fillna('none')
  f['slide_num'] = np.arange(2,stop=f.shape[0]+2,dtype=int)
  disease = re.sub ( ' ', '', f['Condition'].values[0] )
  f['image_slide_num'] = [ disease+'Slide'+str(sn) for sn in f['slide_num'].values ] # KSSlide80.png
  df.append(f)
 

# 
df = pd.concat (df)
for i in ['Age','Sex', 'Ancestry or origin']: 
  try: 
    print ( list ( sorted(set ( df[i] ) ) ) ) 
  except: 
    print ('empty value for ',i)


# how to convert age? 

import os,sys,re,pickle
import numpy as np 
import pandas as pd 

MAPSTRING = {'adol':'adolescence', 'adolescent':'adolescence', 'adult':'youngadult', 'infant':'2y', 'older adult':'olderadult', 'young adult':'youngadult', 'newborn':'2y', 'young adult':'youngadult', 'neweborn':'2y', 'nb':'2y'}

def TryBestConvertAge (string_age): 
  string_age = string_age.lower()
  if string_age.strip() in MAPSTRING: 
    return MAPSTRING[string_age.strip()]
  if any ( [ i in string_age for i in ['mt','month'] ] ):  
    return '2y'
  #
  string_age = re.sub('\?','',string_age)
  string_age = re.sub('<','',string_age)
  string_age = re.sub('>','',string_age)
  string_age = re.sub('--',' ',string_age)
  string_age = re.sub('-',' ',string_age)
  string_age = re.sub('~',' ',string_age)
  string_age = string_age.strip().split()
  try: 
    age = float(string_age[0])
  except:  
    try: # ! try 2nd spot
      age = float(string_age[1]) 
    except: 
      return 'not'
  # (1) under 2 years old, (2) 2-9 years old, (3) 10-19 years old, (4) 20-34 years old, and (5) ≥35 years old.
  if age <= 2: 
    return '2y'
  if age <= 10: 
    return 'youngchild'
  if age <= 20: 
    return 'adolescence'
  if age <= 35: 
    return 'youngadult'
  #
  return 'olderadult'


convert_age = [ TryBestConvertAge(i) for i in df['Age'].values ]
df['OriginalAge'] = df['Age'].values  
df['Age'] = convert_age

# ! need: name,path,label,fold,is_ext 
# ! example: 64142_01_Normalyoungchild.png,/data/duongdb/FairFace/FairFace-aligned-60k-agegroup-06012021-BlankBackgroundCenter/64142_01_Normalyoungchild.png,Normalyoungchild,3,1

print ( set ( df['Age'].values ) ) 
df['name'] = [i+'.png' for i in df['image_slide_num'].values ] 
df['label'] = [ c + a for c,a in zip ( df['Condition'].values, df['Age'].values ) ]
df['path'] = [os.path.join ( args.imagepath , i) for i in df['name'].values ]
df['is_ext'] = 0

gender = []
for index,row in df.iterrows():
  try: 
    g = row['Sex'].strip().lower() 
  except: 
    gender.append(-1)  
    continue
  #
  if len(g) == 0: 
    gender.append(-1)  
  elif g == 'f': 
    gender.append(1)
  else: 
    gender.append(0)

#
df['gender'] = gender 

# ! add extra 
if args.extracsv is not None: 
  extra_df = pd.concat ( [pd.read_csv(d) for d in args.extracsv] ) 
  df = pd.concat ([df,extra_df])
  
# ---------------------------------------------------------------------------- #

df.to_csv (args.outputname, index=False) 


