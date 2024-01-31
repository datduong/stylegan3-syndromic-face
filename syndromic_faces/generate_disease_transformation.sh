#!/bin/bash

source /data/$USER/conda/etc/profile.d/conda.sh
conda activate py37
module load CUDA/11.0
module load cuDNN/8.0.3/CUDA-11.0
module load gcc/8.3.0

# sinteractive --time=3:00:00 --gres=gpu:p100:1 --mem=4g --cpus-per-task=4
# sbatch --partition=gpu --time=2-00:00:00 --gres=gpu:p100:2 --mem=24g --cpus-per-task=24 

#----------------------------------------------------------------------------
# ! generate images, using labels indexing
# ! let's try same random vector, but different label label

cd /data/duongdb/stylegan3-syndromic-faces

# @trunc=0.7 is recommended on their face dataset. but we also find 0.6 works well in some cases. 
# low value implies more consistency between morphing/trasnforming, but we may see low variations (less new features appearing)
truncationpsi=0.6 

# ---------------------------------------------------------------------------- #

# ! sublable1 = disease  
# 22q11DS=0,BWS=1,CdLS=2,Down=3,KS=4,NS=5,PWS=6,RSTS1=7,Unaffected=8,WHS=9,WS=10

# ! sublabel2 = age group
# 2y=11,adolescence=12,olderadult=13,youngadult=14,youngchild=15

# ! sublabel3 = gender
# female=16, male=17

for sublabel3 in '16' '17'
do 
  for sublabel2 in '11' '12' '15' # '11' # '5' '6' # '0' '1' '3'
  do 
    for sublabel1 in '4' '5' # '0' '1' '2' '3' '4' '5' '6' '7' '9' '10'
    do 

      label='8,'$sublabel2','$sublabel3 # ! morph disease from "unaffected" (label index = 8) into something else. 
      morph_to_this_label=$sublabel1','$sublabel2','$sublabel3

      # ! download from provided link
      modelname=Res256AlignPix0-NoExternalUp1-4/00001-stylegan2-Res256AlignPix0-NoExternalUp1-4-gpus4-batch64-gamma0.2048-multilabel/network-snapshot-001209.pkl 
      
      outdir=/data/duongdb/ManyFaceConditions08172022/Stylegan3Model/$modelname'Interpolate'
      mkdir $outdir

      model=/data/duongdb/ManyFaceConditions08172022/Stylegan3Model/$modelname

      # @mix_ratio tells us how much do we want to morph label label x into y. 
      # ! this step will produce static images without transformation at mix_ratio=0 and mix_ratio=1
      for mix_ratio in .75 .5 .25 1 0 
      do 
        python3 generate_images.py --outdir=$outdir/$label$morph_to_this_label'T'$truncationpsi'M'$mix_ratio --trunc=$truncationpsi --seeds=0-150 --label=$label --morph-to-this-label=$morph_to_this_label --network $model --mix-ratio $mix_ratio
      done 

      # ! put all images into a single image strip
      python3 concat_generated_img.py --path $outdir --folder_prefix $label$morph_to_this_label'T'$truncationpsi --interval '1 .75 .5 .25 0' --seed_range '0,150'
      echo $outdir/$label$morph_to_this_label'T'$truncationpsi

    done 
  done 
done


# ! manual eval show these were best 
# random seed number is in the middle (e.g., _95_ or _78_), truncation setting is 0.6 or 0.7
# For Noonan Syndrome: YoungChildGirl_95_0.6, YoungChildBoy_78_0.6, YoungChildGirl_113_0.6, 2yBoy_121_0.6, and YoungChildGirl_126_0.6.
# For Kabuki: YoungChildGirl_141_0.6, 2yGirl_117_0.7, 2yBoy_38_0.6, 2yGirl_66_0.7, and 2yGirl_60_0.7

