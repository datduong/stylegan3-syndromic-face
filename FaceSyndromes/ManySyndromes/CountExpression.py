
import os,sys,re,pickle
import numpy as np
import pandas as pd 


# ---------------------------------------------------------------------------- #

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


# ---------------------------------------------------------------------------- #

# AGE_MAPPING = ['<2y','youngchild', 'adolescence', 'olderadult', 'youngadult']

input_csv = 'C:/Users/duongdb/Documents/ManyFaceConditions12012022/NS_05032023.csv'
string_to_age = True # ! only need to use this if we're running NS.csv 

df = pd.read_csv(input_csv)
df = df[df['URL'].notna()] # ! remove empty row with no URL, every image should have a URL

if string_to_age: # ! convert "5--9" --> youngchild 
  temp = [ TryBestConvertAge(i) for i in df['Age'].fillna('not').tolist()]
  df['Age Grouping'] = temp

#
age_array = df['Age Grouping'].tolist()
age_array = [str(a).strip().lower() for a in age_array]
age_array = [re.sub(' ','',a) for a in age_array] # just remove some spaces
print (set (age_array))

df['Age Grouping'] = age_array

for i in ['Full Smile','Partial Smile','No Smile']: 
  df[i] = df[i].fillna(0) # will in 0 for NaN
  df[i] = [float(str(val).replace(' ','0')) for val in df[i].values] # replace empty string " " with 0
  
# output_count = df.groupby(['Age Grouping']).count()[['URL','Full Smile','Partial Smile','No Smile']]
# print (output_count)

output_count = df.groupby(['Age Grouping'])[['Full Smile','Partial Smile','No Smile']].sum()
print (output_count)
# output_count = output_count.to_numpy()
# output_count.sum(1)

# ! we can write the formatted csv, but we don't need to. 
# df.to_csv('C:/Users/duongdb/Documents/ManyFaceConditions12012022/NS_05032023_agegroup.csv',index=False)

