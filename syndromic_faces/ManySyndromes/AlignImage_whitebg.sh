#!/bin/bash

# ---------------------------------------------------------------------------- #

source /data/$USER/conda/etc/profile.d/conda.sh
conda activate py37
module load CUDA/11.0
module load cuDNN/8.0.3/CUDA-11.0
module load gcc/8.3.0

# ---------------------------------------------------------------------------- #

# ! ! ! CENTER/ALIGN IMAGES (BOTH TEST AND TRAIN SET)

# ---------------------------------------------------------------------------- #


# sbatch --partition=gpu --time=2-00:00:00 --gres=gpu:v100x:2 --mem=24g --cpus-per-task=24 
# sbatch --partition=gpu --time=8:30:00 --gres=gpu:p100:1 --mem=8g --cpus-per-task=8 
# sinteractive --time=1:30:00 --gres=gpu:p100:1 --mem=4g --cpus-per-task=4


# ---------------------------------------------------------------------------- #

# # ! cut out white space ---- specialized powerpoint 
# headfolder=/data/duongdb/ManyFaceConditions12012022
# outfolder_name=$headfolder/TrimImg # ! all images will be in same folder, we need to run the @extract_code 
# mkdir $outfolder_name
# codepath=/data/duongdb/stylegan3-FaceSyndromes/syndromic_faces/ManySyndromes # ! 
# cd $codepath
# for type in 22q11DS BWS CdLS Down KS NS PWS RSTS1 WHS Unaffected WS  
# do 
#   datapath=$headfolder/$type
#   rm $datapath/Slide1.PNG
#   python3 CropWhiteSpace.py --folder_name $datapath --padding 0 --outformat png --label $type --outfolder_name $outfolder_name > $type'trim_log.txt' # ! @png is probably best for ffhq 
# done 
# cd $outfolder_name


# ---------------------------------------------------------------------------- #

resolution=512

codepath=/data/duongdb/stylegan3-FaceSyndromes/syndromic_faces/ManySyndromes # ! 
cd $codepath

headfolder=/data/duongdb/ManyFaceConditions12012022
img_path=$headfolder/TrimImg

colorcode=255

foutpath=$headfolder/TrimImg_no_bg_$colorcode'pix'
foutpath2=$foutpath'_align'

# ! remove background 
python3 RemoveBackground.py --imagepath $img_path --foutpath $foutpath --colorcode $colorcode # ! white background 255 or black background pixel=0 ?

# ! align
python3 AlignImage.py --input_file_path $foutpath --output_file_path $foutpath2 --output_size $resolution --centerface '0,0,512,512' --colorcode $colorcode --notblur --enable_padding

cd $foutpath

# ---------------------------------------------------------------------------- #
# ! not remove background 
cd $codepath
foutpath=$headfolder/TrimImg_align_$colorcode'pix'

python3 AlignImage.py --input_file_path $img_path --output_file_path $foutpath --output_size $resolution --centerface '0,0,512,512' --colorcode $colorcode --notblur --enable_padding

# ---------------------------------------------------------------------------- #

# ! take some random images just for the sake of trying 

codepath=/data/duongdb/stylegan3-FaceSyndromes/syndromic_faces/ManySyndromes # ! 
cd $codepath

headfolder=/data/duongdb/ManyFaceConditions12012022
img_path=$headfolder/NormalImgChosenAsStressTest

colorcode=255

foutpath=$headfolder/TextbookImages_no_bg_$colorcode'pix'
foutpath2=$foutpath'_align'

# ! remove background 
python3 RemoveBackground.py --imagepath $img_path --foutpath $foutpath --colorcode $colorcode # ! white background 255 or black background pixel=0 ?

# ! align
python3 AlignImage.py --input_file_path $foutpath --output_file_path $foutpath2 --output_size $resolution --centerface '0,0,512,512' --colorcode $colorcode --notblur --enable_padding

cd $foutpath

# ! not remove background 
cd $codepath
foutpath=$headfolder/NormalImgChosenAsStressTest_align_$colorcode'pix'

python3 AlignImage.py --input_file_path $img_path --output_file_path $foutpath --output_size $resolution --centerface '0,0,512,512' --colorcode $colorcode --notblur --enable_padding

# ---------------------------------------------------------------------------- #

# ! a pre-defined folder 

# ! cut out white space ---- specialized powerpoint 
headfolder=/data/duongdb/ManyFaceConditions05251222
outfolder_name=$headfolder/SurveyPics_5_26_2022TrimImg # ! all images will be in same folder, we need to run the @extract_code 
mkdir $outfolder_name
codepath=/data/duongdb/stylegan3-FaceSyndromes/syndromic_faces/ManySyndromes # ! 
cd $codepath

datapath=$headfolder/SurveyPics_5_26_2022
python3 CropWhiteSpace.py --folder_name $datapath --padding 0 --outformat png --outfolder_name $outfolder_name > $type'trim_log.txt' # ! @png is probably best for ffhq 

cd $outfolder_name



codepath=/data/duongdb/stylegan3-FaceSyndromes/syndromic_faces/ManySyndromes # ! 
cd $codepath

headfolder=/data/duongdb/ManyFaceConditions05251222
img_path=$headfolder/SurveyPics_5_26_2022TrimImg

colorcode=255

foutpath=$headfolder/SurveyPics_5_26_2022_no_bg_$colorcode'pix'
foutpath2=$foutpath'_align'

# ! remove background 
python3 RemoveBackground.py --imagepath $img_path --foutpath $foutpath --colorcode $colorcode # ! white background 255 or black background pixel=0 ?

# ! align
python3 AlignImage.py --input_file_path $foutpath --output_file_path $foutpath2 --output_size $resolution --centerface '0,0,512,512' --colorcode $colorcode --notblur --enable_padding

cd $foutpath

# ! not remove background 
cd $codepath
foutpath=$headfolder/SurveyPics_5_26_2022_align_$colorcode'pix'

python3 AlignImage.py --input_file_path $img_path --output_file_path $foutpath --output_size $resolution --centerface '0,0,512,512' --colorcode $colorcode --notblur --enable_padding


