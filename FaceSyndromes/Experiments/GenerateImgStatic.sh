#!/bin/bash

source /data/$USER/conda/etc/profile.d/conda.sh
conda activate py37
module load CUDA/11.0
module load cuDNN/8.0.3/CUDA-11.0
module load gcc/8.3.0

# sinteractive --time=2:00:00 --gres=gpu:p100:1 --mem=4g --cpus-per-task=4
# sbatch --partition=gpu --time=2-00:00:00 --gres=gpu:p100:2 --mem=24g --cpus-per-task=24 

#----------------------------------------------------------------------------
# ! generate images, using labels indexing
# ! let's try same random vector, but different label class

cd /data/duongdb/stylegan3-FaceSyndromes

# truncationpsi=.7 # @trunc=0.7 is recommended on their face dataset. 

for truncationpsi in .6
do 
for class3 in '9' '10'
do
  for class2 in '7' '8' # '7' '8' '4' '5' '6' 
  do 
    for class1 in '0' '3' # '5' '6' '7' '8'
    do 

      class=$class1','$class2','$class3

      for modelname in Res256WS22qOther10kNormalGenderNpr0/00000-stylegan2-Res256WS22qOther10kNormalGenderNpr0-gpus4-batch64-gamma0.2048-multilabel/network-snapshot-008064.pkl
      do

        outdir=/data/duongdb/WS22qOther_12082021/Stylegan3Model/$modelname'Interpolate'
        mkdir $outdir

        model=/data/duongdb/WS22qOther_12082021/Stylegan3Model/$modelname

        python3 generate_images.py --outdir=$outdir/$class'T'$truncationpsi'Static' --trunc=$truncationpsi --seeds=0-200 --class=$class --network $model 

      done 
    done 
  done 
done 
done 




# 22qOldAdultMorphGirlBoy
# 22qOldAdultMorphNormalGirl
# 22qOldAdultMorphNormalBoy
22q
22q2yGirl
22q2yBoy
22q
22qAdolesGirl
22qAdolesBoy
22q
22qOldestGirl
22qOldestBoy

WSYoungAdultGirl
WSYoungAdultBoy
WSYoungChildGirl
WSYoungChildBoy


WSGirl
WSBoy