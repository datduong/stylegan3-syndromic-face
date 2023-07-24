
from cProfile import label
import re,sys,pickle,os 
import pandas as pd 

df = pd.read_csv('/data/duongdb/ManyFaceConditions01072022/ManyCondition+10kNormal-Other.csv')
labels = sorted ( set ( df['label'].values ) ) 
for l in labels: 
  temp = df[df['label']==l]
  print (l,temp.shape[0])


