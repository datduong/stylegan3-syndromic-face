
import os,sys,re,pickle
from black import main 
import pandas as pd 
import numpy as np 

# ! replace the path to ones with background removed? 

maindir = '/data/duongdb/ManyFaceConditions01312022'
os.chdir (maindir)

foutname = 'ManyCondition-Normal-Other-RmBg.csv'

fin = 'ManyCondition-Normal-Other.csv' 
fin = os.path.join(maindir,fin)

# ! read in full input, remove controls and normal, replace path. 
path1new = '/data/duongdb/ManyFaceConditions01312022/Align512CenterRmBg11Cond/'
path1old = '/data/duongdb/WS22qOther_08102021/Align512BlankBackgroundCenter/'

path2new = '/data/duongdb/ManyFaceConditions01312022/Align512CenterRmBg11Cond/'
path2old = '/data/duongdb/ManyFaceConditions01072022//Align1024BlankBackgroundCenter/' 

newpath = []
fin = pd.read_csv(fin)

# # ! skip normal 
# fin = fin[~fin['label'].str.contains('Normal')]
# fin = fin.reset_index(drop=True)

for index,row in fin.iterrows(): 
  # Condition,Age,Ancestry or origin,Sex,URL,Notes,slide_num,image_slide_num,Gene,Ancestry or Origin,Note,OriginalAge,name,label,path,is_ext,gender,fold
  if any ( bool ( re.findall (i ,row['label']) ) for i in ['^WS','^22q'] ) : 
    newpath.append ( re.sub(path1old,path1new,row['path']) )
  if any ( bool ( re.findall (i ,row['label']) ) for i in ['^BWS', '^CdLS', '^Down', '^KS', '^NS', '^Unaffected', '^PWS', '^RSTS1', '^WHS'] ) : 
    newpath.append ( re.sub(path2old,path2new,row['path']) )


# 
fin['path'] = newpath
fin.to_csv(foutname,index=None) 


