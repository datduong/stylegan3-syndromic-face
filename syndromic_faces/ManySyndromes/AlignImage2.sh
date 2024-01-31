#!/bin/bash

# ---------------------------------------------------------------------------- #

source /data/$USER/conda/etc/profile.d/conda.sh
conda activate py37
module load CUDA/11.0
module load cuDNN/8.0.3/CUDA-11.0
module load gcc/8.3.0

# ---------------------------------------------------------------------------- #

# ! CENTER/ALIGN IMAGES 

# ---------------------------------------------------------------------------- #

# ! may need GPU
# sbatch --partition=gpu --time=2-00:00:00 --gres=gpu:v100x:2 --mem=24g --cpus-per-task=24 
# sbatch --partition=gpu --time=14:30:00 --gres=gpu:p100:1 --mem=8g --cpus-per-task=8 
# sinteractive --time=1:30:00 --gres=gpu:p100:1 --mem=4g --cpus-per-task=4


# ---------------------------------------------------------------------------- #

# ! cut out white space from powerpoint
headfolder=/data/duongdb/ManyFaceConditions12012022
outfolder_name=$headfolder/TrimImg # ! all images will be in same folder, we need to run the @extract_code 
mkdir $outfolder_name
codepath=/data/duongdb/stylegan3-syndromic-faces/syndromic_faces/ManySyndromes # ! 
cd $codepath
for type in 22q11DS BWS CdLS Down KS NS PWS RSTS1 WHS Unaffected WS  
do 
  datapath=$headfolder/$type
  python3 CropWhiteSpace.py --folder_name $datapath --padding 0 --outformat png --label $type --outfolder_name $outfolder_name > $type'trim_log.txt' # ! @png is probably best for ffhq 
done 
cd $outfolder_name


# ---------------------------------------------------------------------------- #

resolution=720

codepath=/data/duongdb/stylegan3-syndromic-faces/syndromic_faces/ManySyndromes # ! 
cd $codepath

headfolder=/data/duongdb/ManyFaceConditions12012022
img_path=$headfolder/TrimImg

colorcode=0

foutpath=$headfolder/TrimImg_no_bg_$colorcode'pix'_$resolution'rs'
foutpath2=$foutpath'_align'

# ! remove background 
python3 RemoveBackground.py --imagepath $img_path --foutpath $foutpath --colorcode $colorcode # ! set background pixel=0 a

# ! align
python3 AlignImage.py --input_file_path $foutpath --output_file_path $foutpath2 --output_size $resolution --centerface '0,0,720,720' --colorcode $colorcode --notblur --enable_padding

cd $foutpath




