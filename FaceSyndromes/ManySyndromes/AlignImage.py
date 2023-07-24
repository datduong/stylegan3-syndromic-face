
import os,sys,re,pickle
from tqdm import tqdm
import numpy as np

sys.path.append('/data/duongdb/StyleFlow')
os.chdir('/data/duongdb/StyleFlow')

from PIL import Image # pip install Pillow
from PIL import ImageOps

from utils import * # ! follow https://github.com/RameenAbdal/StyleFlow/issues/14#issuecomment-765644589

# ---------------------------------------------------------------------------


import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--input_file_path", type=str, default=None)
parser.add_argument("--output_file_path", type=str, default=None)
parser.add_argument("--output_size", type=int, default=None)
parser.add_argument("--transform_size", type=int, default=4096) # transform_size is not same as output_size, output_size override
parser.add_argument("--centerface", type=str, default='25,25,487,487')
parser.add_argument("--notblur", action='store_true', default=False)
parser.add_argument("--whitebackground", action='store_true', default=False)
parser.add_argument("--start", type=int, default=None)
parser.add_argument("--end", type=int, default=None)
parser.add_argument("--colorcode", type=int, default=None)
parser.add_argument("--skip_exist", action='store_true', default=False) # skip already created file
parser.add_argument("--verbose", action='store_true', default=False) # skip already created file
parser.add_argument("--enable_padding", action='store_true', default=False) # skip already created file


args = parser.parse_args()


if not os.path.exists (args.output_file_path): 
  os.mkdir(args.output_file_path)


if args.colorcode is not None: 
  if args.colorcode == 255: 
    args.whitebackground = True # override 
  elif args.colorcode == 0:
    args.whitebackground = False # override 
  else:
    print ('colorcode is 0 or 255')
    exit()

print ('background color is white : ? ', args.whitebackground)
# ---------------------------------------------------------------------------

imagelist = np.array ( sorted ( os.listdir(args.input_file_path) ) ) 

if args.start is not None: 
  if args.end > len(imagelist): 
    args.end = len(imagelist)
  #
  imagelist = imagelist[args.start:args.end]


for f in tqdm ( imagelist ) :
  
  print ('\n\n'+f) 
  dest_file=os.path.join(args.output_file_path,f)
  # check if file exists. 
  if args.skip_exist and os.path.exists(dest_file): 
    continue
    
  if args.verbose: # images can fail if it's too different from standard faces. ??? whatttt....
    print('align face '+f)
    Align_face_image(os.path.join(args.input_file_path,f), output_size=args.output_size, transform_size=args.transform_size, enable_padding=args.enable_padding, dest_file=dest_file, notblur=args.notblur, centerface=args.centerface, whitebackground=args.whitebackground)
  
  else: 
    try: 
      Align_face_image(os.path.join(args.input_file_path,f), output_size=args.output_size, transform_size=args.transform_size, enable_padding=args.enable_padding, dest_file=dest_file, notblur=args.notblur, centerface=args.centerface, whitebackground=args.whitebackground)
    except: 
      print('fail align face '+f)



