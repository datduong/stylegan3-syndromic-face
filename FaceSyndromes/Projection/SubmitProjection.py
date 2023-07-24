
import enum
import time,os,sys,re,pickle
from datetime import datetime

import numpy as np 
import pandas as pd 


# ! submit projection code. will need mutliple small jobs. 

BASESCRIPT = """#!/bin/bash

source /data/$USER/conda/etc/profile.d/conda.sh
conda activate py37
module load CUDA/11.0
module load cuDNN/8.0.3/CUDA-11.0
module load gcc/8.3.0

# sinteractive --time=2:00:00 --gres=gpu:p100:1 --mem=4g --cpus-per-task=4
# sbatch --partition=gpu --time=2-00:00:00 --gres=gpu:p100:2 --mem=24g --cpus-per-task=24 

#----------------------------------------------------------------------------
# ! project images into W space (or W+ space)

cd /data/duongdb/stylegan3-FaceSyndromes

workdir=/data/duongdb/ManyFaceConditions01312022

outdir=$workdir/ExampleProjection

network=$workdir/Stylegan3Model/Res256ManyCondition-Normal-Other-RmBgUp1-4/00000-stylegan2-Res256ManyCondition-Normal-Other-RmBgUp1-4-gpus4-batch64-gamma0.2048-multilabel/network-snapshot-001129.pkl


"""

basecommand = """

python3 projector.py --target=TARGET --project-in-wplus \
--num-steps=1000 \
--outdir $outdir --lump-outdir \
--network=$network \
--class-str=CLASSSTR --class-len=18

"""

# ---------------------------------------------------------------------------- #

os.chdir('/data/duongdb/ManyFaceConditions01312022')

# ---------------------------------------------------------------------------- #

df1 = pd.read_csv('/data/duongdb/ManyFaceConditions01312022/Classify/ManyCondition-Normal-Other-RmBgAlign-Easy-train.csv') 
df2 = pd.read_csv('/data/duongdb/ManyFaceConditions01312022/Classify/ManyCondition-Normal-Other-RmBg-train.csv')
df = pd.merge(df1,df2,on='name')
# assert (df.shape == df1.shape) or (df.shape == df2.shape)
df = df.sort_values(['name']).reset_index(drop=True)

# ---------------------------------------------------------------------------- #

age = sorted ( '2y,olderadult,youngadult,youngchild,adolescence'.split(',') ) 

# ! project 22q and ws ... for now. 

# df = df[ (df['label_x']=='22q11DS') | (df['label_x']=='WS') ]
# disease_list = 'Unaffected,BWS,CdLS,Down,KS,NS,PWS,RSTS1,WHS,22q11DS,WS'.split(',') # ['WS','22q11DS']
disease_list = 'Unaffected,KS'.split(',') # ['WS','22q11DS']
disease_list = sorted( disease_list ) 
disease_dict = {val:str(k) for k,val in enumerate(disease_list)}

counter = 0 
for disease in disease_dict: 
  # if disease in ['WS','22q11DS']: 
  #   continue # skip because already did it
  for i, a in enumerate(age): 
    basescript = BASESCRIPT 
    dftemp = df[ df['label_x'] == disease ]
    dftemp = dftemp [ dftemp['detail_label_y'].str.contains(a) ]
    for index,row in dftemp.iterrows(): 
      class_str = disease_dict [disease] # '10' if row['label_x'] == disease else '0' # ! fix later 
      #
      if a in row['detail_label_y'] :
        class_str = class_str + ',' + str(11 + i)
      #
      class_str = class_str+',16' if row['gender_y'] == 1 else class_str+',17'
      newcommand = re.sub('TARGET',row['path_x'], basecommand)
      newcommand = re.sub('CLASSSTR',class_str, newcommand)
      basescript = basescript + newcommand
    #
    # submit 
    counter = counter + 1 
    date_time = datetime.now().strftime("%m%d%Y%H%M%S") # current date and time
    fname = 'script'+str(counter+1)+date_time+'.sh'
    fout = open(fname,'w')
    fout.write(basescript)
    fout.close()
    counter = counter + 1
    time.sleep(2)
    os.system('sbatch --partition=gpu --time=1-00:00:00 --gres=gpu:p100:1 --mem=8g --cpus-per-task=4 '+fname)

    
      

    

