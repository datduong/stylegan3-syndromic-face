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


TryBestConvertAge('5--9') # example 

TryBestConvertAge('2 y estimated') # example 

