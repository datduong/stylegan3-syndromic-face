

import os,sys,re,pickle
import numpy 
import json 

this_path = '/data/duongdb/SkinConditionImages11052020/ZoomCenter/weights'

rootpathlist = os.listdir(this_path)
for rootpath in rootpathlist: 
  temp_ = os.path.join(this_path,rootpath)
  temp2_ = [i for i in os.listdir(temp_) if '_best' in i]
  for i in temp2_: 
    os.system('rm ' + os.path.join(temp_,i))

# 
