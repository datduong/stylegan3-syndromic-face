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
# ! let's try same random vector, but different label class

cd /data/duongdb/stylegan3-FaceSyndromes

truncationpsi=0.6 # @trunc=0.7 is recommended on their face dataset. 

for class3 in '16' '17'
do 
  for class2 in '11' '12' '15' # '11' # '5' '6' # '0' '1' '3'
  do 
    for class1 in '4' '5' # '0' '1' '2' '3' '4' '5' '6' '7' '9' '10'
    do 

      class='8,'$class2','$class3 # ! change disease 
      class_next=$class1','$class2','$class3

      # class='8,'$class2 # ! change disease 
      # class_next=$class1','$class2

      # class=$class1','$class2','$class3 # ! change gender 
      # class_next=$class1','$class2',10'

      # class=$class1','$class2','$class3 # ! change age 
      # class_next=$class1',6,'$class3

      # Res256ManyCondition-Normal-Other-RmBgUp1-4/00000-stylegan2-Res256ManyCondition-Normal-Other-RmBgUp1-4-gpus4-batch64-gamma0.2048-multilabel/network-snapshot-001129.pkl

      # "network-snapshot-001680.pkl" "network-snapshot-001600.pkl"
      # /data/duongdb/ManyFaceConditions01312022/Stylegan3Model/Res1024ManyCondition-Normal-Other-RmBgUp1-4/00000-stylegan2-Res1024ManyCondition-Normal-Other-RmBgUp1-4-gpus4-batch16-gamma13.1072
      # Res1024ManyCondition-Normal-Other-RmBgUp1-4/00000-stylegan2-Res1024ManyCondition-Normal-Other-RmBgUp1-4-gpus4-batch16-gamma13.1072/network-snapshot-001680.pkl
      # Res256AlignPix0-NoExternalUp1-4/00001-stylegan2-Res256AlignPix0-NoExternalUp1-4-gpus4-batch64-gamma0.2048-multilabel/network-snapshot-001209.pkl

      for modelname in Res256AlignPix255-NoExternalUp1-4/00000-stylegan2-Res256AlignPix255-NoExternalUp1-4-gpus4-batch64-gamma0.2048-multilabel/network-snapshot-001330.pkl
      do

        outdir=/data/duongdb/ManyFaceConditions08172022/Stylegan3Model/$modelname'Interpolate'
        mkdir $outdir

        model=/data/duongdb/ManyFaceConditions08172022/Stylegan3Model/$modelname

        for mix_ratio in .75 .5 .25 1 0 # .75 .5 .25
        do 
          python3 gen_images.py --outdir=$outdir/$class$class_next'T'$truncationpsi'M'$mix_ratio --trunc=$truncationpsi --seeds=0-150 --class=$class --class-next=$class_next --network $model --mix-ratio $mix_ratio
        done 

        python3 concat_generated_img.py --path $outdir --folder_prefix $class$class_next'T'$truncationpsi --interval '1 .75 .5 .25 0' --seed_range '0,150'
        echo $outdir/$class$class_next'T'$truncationpsi

      done 

    done 
  done 
done

