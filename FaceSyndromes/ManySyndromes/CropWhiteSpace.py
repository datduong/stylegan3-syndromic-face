
from PIL import Image # pip install Pillow
import sys, re, os
import glob
from PIL import ImageOps
import numpy as np

from tqdm import tqdm

def center_crop(img, new_width=None, new_height=None, ratio=None):        

    width = img.size[1]
    height = img.size[0]

    if new_width is None:
        new_width = np.floor(width * ratio)
        
    if new_height is None:
        new_height = np.floor(height * ratio)

    left = int(np.ceil((width - new_width) / 2))
    right = width - int(np.floor((width - new_width) / 2))
  
    top = int(np.ceil((height - new_height) / 2))
    bottom = height - int(np.floor((height - new_height) / 2))

    center_cropped_img = img.crop((left, top, right, bottom))
    return center_cropped_img


# ! trim image

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--folder_name", type=str, default=None)
parser.add_argument("--padding", type=int, default=None)
parser.add_argument("--outformat", type=str, default='png')
parser.add_argument("--label", type=str, default=None)
parser.add_argument("--outfolder_name", type=str, default='TrimWhiteSpaceNoBorder')


args = parser.parse_args()

# !

args.padding = np.asarray([-1*args.padding, -1*args.padding, args.padding, args.padding])

print ('output format {}'.format(args.outformat))

if args.label is not None: 
    label = re.sub('/','',args.folder_name.split('/')[-1]) # ! should expect @args.folder_name = 'path/label'
else: 
    label = ''
   
print ('\n\nlabel {}\n\n'.format(label))

filePaths = glob.glob(args.folder_name + "/*.JPG") #search for all png images in the folder
if len(filePaths) == 0: 
    filePaths = glob.glob(args.folder_name + "/*.PNG") #search for all png images in the folder

if args.outfolder_name is None: 
    OutputFolder = os.path.join(args.folder_name,'TrimWhiteSpaceNoBorder')
else: 
    OutputFolder = args.outfolder_name

if not os.path.exists (OutputFolder): 
    os.mkdir (OutputFolder)


for filePath in tqdm(filePaths):

    image=Image.open(filePath).convert('RGB')
    image.load()
    imageSize = image.size

    # ! does not fully remove white space, so we have to add extra values to fully remove white space
    img_array = np.asarray(image).astype(int)
    img_array = img_array + 50 ## ! make picture brighter, USE ONLY FOR CROPPING, NOT SAVE THIS
    img_array[img_array>255] = 255 ## set as white

    image_addvalue = Image.fromarray(img_array.astype(np.uint8))
    # remove alpha channel
    invert_im = image_addvalue.convert("RGB") # @image_addvalue is used to get bounding boxes
    # invert image (so that white is 0)
    invert_im = ImageOps.invert(invert_im) # ! https://stackoverflow.com/questions/9870876/getbbox-method-from-python-image-library-pil-not-working
    imageBox = invert_im.getbbox()
    try: 
        imageBox = tuple(np.asarray(imageBox)+args.padding)
    except: 
        print ('skip ', filePath)
        continue # pass

    cropped = image.crop(imageBox) # ! NOTICE @image is used to retain original color
    # cropped = center_crop (cropped,ratio=0.55) # ! cut down each side to get rid of white space ... not ideal here, because we lose some info

    filePath = re.sub(r"(PNG|JPG)",args.outformat,filePath)
    filePath = label + filePath.split('/')[-1] # name only
    cropped.save( os.path.join(OutputFolder, filePath), format=args.outformat ) ## override 

