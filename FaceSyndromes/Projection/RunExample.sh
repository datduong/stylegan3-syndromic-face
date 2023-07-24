#!/bin/bash

source /data/$USER/conda/etc/profile.d/conda.sh
conda activate py37
module load CUDA/11.0
module load cuDNN/8.0.3/CUDA-11.0
module load gcc/8.3.0

# sinteractive --time=2:00:00 --gres=gpu:p100:1 --mem=4g --cpus-per-task=4
# sbatch --partition=gpu --time=2-00:00:00 --gres=gpu:p100:2 --mem=24g --cpus-per-task=24 

#----------------------------------------------------------------------------
# ! project images into W space (or W+ space)

cd /data/duongdb/stylegan3-FaceSyndromes

workdir=/data/duongdb/ManyFaceConditions01312022

outdir=$workdir/ExampleProjection

target=$workdir/RmBgAlign9Cond+WS22qTest/NSSlide29.png # takes png, not path

network=$workdir/Stylegan3Model/Res256ManyCondition-Normal-Other-RmBgUp1-4/00000-stylegan2-Res256ManyCondition-Normal-Other-RmBgUp1-4-gpus4-batch64-gamma0.2048-multilabel/network-snapshot-001129.pkl

python3 projector.py --target=$target --project-in-wplus \
--num-steps=1000 \
--outdir $outdir \
--network=$network \
--class-str='5,15,17' --class-len=18
cd $outdir
