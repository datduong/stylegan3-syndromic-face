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

# {"label1":[0,11],"label2":[11,16],"label3":[16,18]}

for truncationpsi in .8
do 
  for class1 in '0' '1' '2' '3' '4' '5' '6' '7' '8' '9' '10'  # '0' '1' '2' '3' '4' '5' '6' '7' '8' '9' '10' 
  do 

    class=$class1

    for modelname in Res256AlignPix255-0Normal-SkipAgeUp1-5/00000-stylegan2-Res256AlignPix255-0Normal-SkipAgeUp1-5-gpus2-batch64-gamma0.2048/network-snapshot-000887.pkl
  
    do

      outdir=/data/duongdb/ManyFaceConditions05092022/Stylegan3Model/$modelname'Interpolate'
      mkdir $outdir

      model=/data/duongdb/ManyFaceConditions05092022/Stylegan3Model/$modelname

      python3 gen_images.py --outdir=$outdir/$class'T'$truncationpsi'Static' --trunc=$truncationpsi --seeds=0-20 --class=$class --network $model --prefix-dict '22q11DS,BWS,CdLS,Down,KS,NS,Unaffected,PWS,RSTS1,WHS,WS'

    done 
  done 
done 


# Res256ManyCondition+10kNormal-OtherUp4-20/00001-stylegan2-Res256ManyCondition+10kNormal-OtherUp4-20-gpus4-batch64-gamma0.2048-multilabel/network-snapshot-003145.pkl
# Res256ManyCondition+10kNormal-OtherUp4-20/00000-stylegan2-Res256ManyCondition+10kNormal-OtherUp4-20-gpus4-batch64-gamma0.2048-multilabel/network-snapshot-004112.pkl
# Res256ManyCondition+10kNormal-Other-SkipAgeUp2-10/00001-stylegan2-Res256ManyCondition+10kNormal-Other-SkipAgeUp2-10-gpus2-batch64-gamma0.2048-multilabel/network-snapshot-001693.pkl

# Res256ManyCondition+10kNormal-OtherUp2-10/00000-stylegan2-Res256ManyCondition+10kNormal-OtherUp2-10-gpus2-batch64-gamma0.2048-multilabel/network-snapshot-003064.pkl

# Res256ManyCondition+10kNormal-Other-SkipAge-SkipGenderUp2-10/00001-stylegan2-Res256ManyCondition+10kNormal-Other-SkipAge-SkipGenderUp2-10-gpus2-batch64-gamma0.2048/network-snapshot-000685.pkl
