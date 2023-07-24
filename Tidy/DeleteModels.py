
import os,sys,re,pickle 
import json 
import numpy as np 


# ! look at best saved model a list of paths
mod = """Res256ManyCondition+10kNormal-Other-SkipAgeUp2-10""".split()
rootpathlist = ['/data/duongdb/ManyFaceConditions01312022/Stylegan3Model/' + m.strip() for m in mod]

for rootpath in rootpathlist: 
  print ('\n',rootpath)
  for f in os.listdir(rootpath): 
    try: 
      metric = open(os.path.join(rootpath,f,'metric-fid200_full.jsonl'),'r')
    except: 
      continue
    metric_array = []
    name = []
    for l in metric: 
      z = json.loads(l)
      metric_array.append ( z['results']['fid200_full'] ) 
      name.append ( z["snapshot_pkl"] )
    low_point = np.min ( np.array(metric_array) ) 
    metric.close()
    print (f, name[metric_array.index(low_point)], low_point)
    
  #


# ! delete 
import os,sys,re,pickle 
import json 
import numpy as np 

mod = """Res256AlignPix0-NoExternalUp1-4""".split()

skip_mod = ['00001-stylegan2-Res256AlignPix0-NoExternalUp1-4-gpus4-batch64-gamma0.2048-multilabel']

rootpathlist = ['/data/duongdb/ManyFaceConditions08172022/Stylegan3Model/' + m.strip() for m in mod]

skip = []
# skip = ["network-snapshot-001169"] # ['network-snapshot-001129' , 'network-snapshot-000766' ]

for rootpath in rootpathlist: 
  if not os.path.exists(rootpath): 
    continue
  for f in os.listdir(rootpath): 
    # if 'stylegan3-t' not in f: 
    #   continue
    if any (s in f for s in skip_mod): 
      print ('skip model', f)
      continue
    try: 
      metric = open(os.path.join(rootpath,f,'metric-fid5k_full.jsonl'),'r')
    except: 
      continue
    print (rootpath)
    metric_array = []
    for l in metric: 
      z = json.loads(l)
      metric_array.append ( z['results']['fid5k_full'] ) 
    try:
      low_point = np.sort ( np.array(metric_array) ) [1] # ! take some x last, like 2nd last, 3rd last ...
    except: 
      pass
    metric.close()
    # read again 
    metric = open(os.path.join(rootpath,f,'metric-fid5k_full.jsonl'),'r')
    for l in metric: 
      z = json.loads(l)
      if any (s in z['snapshot_pkl'] for s in skip): 
        print ('skip', z['snapshot_pkl'])
        continue
      if z['results']['fid5k_full'] > low_point: 
        if os.path.exists(os.path.join(os.path.join(rootpath,f,z['snapshot_pkl']))): 
          os.system('rm ' + os.path.join(os.path.join(rootpath,f,z['snapshot_pkl'])) )
          temp_ = re.sub('network-snapshot-','fakes',z['snapshot_pkl'])
          temp_ = re.sub('pkl','png',temp_)
          os.system('rm ' + os.path.join(os.path.join(rootpath,f,temp_)) ) # network-snapshot-001000.pkl --> fakes001000.png
    #
    metric.close()
    os.system ( 'rm ' + os.path.join(rootpath,f,'fakes_init.png') )
    os.system ( 'rm ' + os.path.join(rootpath,f,'reals.png') )

  #

