#!/bin/bash

source /data/$USER/conda/etc/profile.d/conda.sh # activate your own conda... you need to change to your own path
conda activate py37 # activate the version of your conda 

module load CUDA/11.0 # load your proper cuda and gcc version
module load cuDNN/8.0.3/CUDA-11.0
module load gcc/8.3.0


# run e4e to get latent W for many images in bulk... run on GPU 
images_dir=somepath 
save_dir=somepath 
ckpt=your_pretrained_e4e
# use --batch 64 to run 64 images at once on GPU 
python3 e4e/inference.py ckpt $ckpt --images_dir $images_dir --save_dir $save_dir --batch 64 --align 


# run inferfacegan to get boundary at different settings. 

chosen_num_or_ratio=.9 # use 90% of data (80% of this 90% will be train set, 20% of this 90% will be evaluation set), the leftover 10% will be test set. 
scores_path=somepath 
latent_codes_path=somepath 

for split_ratio in 0.7 0.8 0.9 # run different split ratio. 
do

  # run svm to get boundary 
  output_dir=somepath/BoundaryAtSplitRatio$split_ratio
  mkdir $output_dir
  python3 interfacegan/train_boundary.py --split_ratio $split_ratio --chosen_num_or_ratio $chosen_num_or_ratio --output_dir $output_dir --latent_codes_path $latent_codes_path --scores_path $scores_path

  # run face edit of e4e after you get boundary 
  # see their google colab for example. 
  
done 

