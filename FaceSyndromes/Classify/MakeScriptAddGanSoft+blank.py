import re,sys,os,pickle
from datetime import datetime
import time

# sbatch --partition=gpu --time=1-00:00:00 --gres=gpu:p100:2 --mem=12g --cpus-per-task=24
# sbatch --partition=gpu --time=4:00:00 --gres=gpu:p100:1 --mem=16g --cpus-per-task=24
# sbatch --partition=gpu --time=1-00:00:00 --gres=gpu:p100:2 --mem=10g --cpus-per-task=20
# sbatch --time=12:00:00 --mem=100g --cpus-per-task=24
# sinteractive --time=1:00:00 --gres=gpu:p100:1 --mem=12g --cpus-per-task=12

script = """#!/bin/bash

source /data/$USER/conda/etc/profile.d/conda.sh
conda activate py37
module load CUDA/11.0 # ! newest version at the time
module load cuDNN/8.0.3/CUDA-11.0
module load gcc/8.3.0

# ! check model name

weight=WEIGHT # ! don't need to write out weight, the X1 X10 will give us idea of size ??

learningrate=LEARNRATE
imagesize=IMAGESIZE
schedulerscaler=ScheduleScaler 
dropout=DROPOUT

batchsize=64 # 64 ... 64 doesn't work with new pytorch 1.7 ?? why ?? we were using 1.6 

ntest=1 # ! we tested 1, and it looks fine at 1, don't need data aug during testing

kernel_type=9c_b4ns_$imagesize'_30ep' # ! this is experiment name

suffix=NUM_TIME_MIX # ! now many times we do style mix

outdim=4

NUMFC=numberoflayers # ! final layer, should it be complicated or simple linear?? 

# suffix2=T0.6WS+22q11DS+Control+Normal+kimg10+target0.6+TransA+blankcenter
# model_folder_name=b4ns$imagesize$imagetype'WlWEIGHTss'$schedulerscaler'lr'$learningrate'dp'$dropout'b'$batchsize'ntest'$ntest$suffix2 # ! NOTICE "WL" IS CAP IN SOME CASES...

suffix2=WS+22q11DS+Control+Normal+Whole+blankcenter
model_folder_name=b4ns$imagesize$imagetype'wlWEIGHTss'$schedulerscaler'lr'$learningrate'dp'$dropout'b'$batchsize'ntest'$ntest$suffix2 # ! NOTICE "WL" IS CAP IN SOME CASES...


cd /data/duongdb/ClassifyFaceConditions

maindir=/data/duongdb/WS22qOther_08102021/Classify

modeldir=$maindir/$model_folder_name 
mkdir $modeldir

logdir=$maindir/$model_folder_name 
oofdir=$maindir/$model_folder_name/EvalDev 

fold=FOLD


# ! eval

# stylegan_mod=Res256WS22qOther10kNormalGenderNpr0/00000-stylegan2-Res256WS22qOther10kNormalGenderNpr0-gpus4-batch64-gamma0.2048-multilabel/network-snapshot-008064.pkl
# do_test_manual_name=Res256WS22qOther10kNormalGenderNpr0-Normal

# stylegan_mod=Res256WS22qOther10kNormalGenderNpr2/00000-stylegan2-Res256WS22qOther10kNormalGenderNpr2-gpus4-batch64-gamma0.2048-multilabel/network-snapshot-004233.pkl
# do_test_manual_name=Res256WS22qOther10kNormalGenderNpr2

# stylegan_mod=Res256WS22qOther2500NormalGenderNpr0Up2/00000-stylegan2-Res256WS22qOther2500NormalGenderNpr0Up2-gpus4-batch64-gamma0.2048-multilabel/network-snapshot-007862.pkl
# do_test_manual_name=Res256WS22qOther2500NormalGenderNpr0Up2

# stylegan_mod=Res256WS22qOther2500NormalGenderNpr2Up2/00000-stylegan2-Res256WS22qOther2500NormalGenderNpr2Up2-gpus4-batch64-gamma0.2048-multilabel/network-snapshot-006249.pkl 
# do_test_manual_name=Res256WS22qOther2500NormalGenderNpr2Up2

# stylegan_mod=TfStyleGAN3LabelRes256Up10+Gender/00002-stylegan2-TfStyleGAN3LabelRes256Up10+Gender-gpus2-batch32-gamma0.4096-multilabel/network-snapshot-003000.pkl 
# do_test_manual_name=TfStyleGAN3LabelRes256Up10+Gender

# stylegan_mod=Res256WS22qOther2500NormalGenderNpr2Up5/00000-stylegan2-Res256WS22qOther2500NormalGenderNpr2Up5-gpus4-batch64-gamma0.2048-multilabel/network-snapshot-003830.pkl
# do_test_manual_name=Res256WS22qOther2500NormalGenderNpr2Up5

# stylegan_mod=TfStyleGAN3LabelRes256Up5Frac50Normal+Gender/00000-stylegan2-TfStyleGAN3LabelRes256Up5Frac50Normal+Gender-gpus4-batch64-gamma0.2048-multilabel/network-snapshot-001411.pkl
# do_test_manual_name=fStyleGAN3LabelRes256Up5Frac50Normal+Gender-Static

stylegan_mod=Res1024WS22qOther10kNormalGenderNpr0Up10/00000-stylegan2-Res1024WS22qOther10kNormalGenderNpr0Up10-gpus4-batch16-gamma5-multilabel/network-snapshot-005200.pkl
do_test_manual_name=Res1024WS22qOther10kNormalGenderNpr0Up10Sg2-StaticT0.8

# stylegan_mod=Res1024WS22qOther10kNormalGenderNpr0Up10/00001-stylegan3-t-Res1024WS22qOther10kNormalGenderNpr0Up10-gpus4-batch16-gamma6.6-multilabel/network-snapshot-004560.pkl 
# do_test_manual_name=Res1024WS22qOther10kNormalGenderNpr0Up10Sg3-Static


imagecsv=/data/duongdb/WS22qOther_12082021/Stylegan3Model/$stylegan_mod'Interpolate'/FakeStaticTestT0.8.csv

python evaluate.py --image-csv $imagecsv --kernel-type $kernel_type --model-dir $modeldir --log-dir $logdir --image-size $imagesize --enet-type tf_efficientnet_b4_ns --oof-dir $oofdir --batch-size 64 --num-workers 4 --fold 'FOLD' --out-dim $outdim --CUDA_VISIBLE_DEVICES 0 --dropout $dropout --do_test_manual_name $do_test_manual_name --n-test $ntest 

done 



"""

path = '/data/duongdb/WS22qOther_08102021'
os.chdir(path)

NUM_TIME_MIX='X1'

LABELUP = '22q11DS,WS,Controls'

# LABELUP = '22q11DS2y,22q11DSadolescence,22q11DSolderadult,22q11DSyoungadult,22q11DSyoungchild,Controls2y,Controlsadolescence,Controlsolderadult,Controlsyoungadult,Controlsyoungchild,WS2y,WSadolescence,WSolderadult,WSyoungadult,WSyoungchild'

counter=0

numberoflayers=0

# for ATTRIBUTELABEL in '22q11DS,WS,Controls,Normal2y,Normaladolescence,Normalolderadult,Normalyoungadult,Normalyoungchild'.split(','): 
for fold in [0,1,2,3,4]: #  
  for imagesize in [448]: # 448 512 768 640
    for weight in ['10']: # 5,10, '5;10' # ! always use weight 1 ? # can take string a;b
      for schedulerscaler in [10]:
        for learn_rate in [0.00003]:  # 0.00001,0.00003  # we used this too, 0.0001
          for dropout in [0.2]:
            script2 = re.sub('WEIGHT',str(weight),script)
            script2 = re.sub('IMAGESIZE',str(imagesize),script2)
            script2 = re.sub('numberoflayers',str(numberoflayers),script2)
            script2 = re.sub('LABELUP',str(LABELUP),script2)
            script2 = re.sub('LEARNRATE',str(learn_rate),script2)
            script2 = re.sub('ScheduleScaler',str(schedulerscaler),script2)
            script2 = re.sub('FOLD',str(fold),script2)
            script2 = re.sub('DROPOUT',str(dropout),script2)
            script2 = re.sub('NUM_TIME_MIX',str(NUM_TIME_MIX),script2)
            # script2 = re.sub('ATTRIBUTELABEL',str(ATTRIBUTELABEL),script2)
            now = datetime.now() # current date and time
            scriptname = 'script'+str(counter)+'-'+now.strftime("%m-%d-%H-%M-%S")+'.sh'
            fout = open(scriptname,'w')
            fout.write(script2)
            fout.close()
            # 
            time.sleep(1)
            # os.system('sbatch --partition=gpu --time=30:00:00 --gres=gpu:p100:2 --mem=12g --cpus-per-task=16 ' + scriptname )
            os.system('sbatch --partition=gpu --time=00:20:00 --gres=gpu:p100:1 --mem=8g --cpus-per-task=8 ' + scriptname )
            # os.system('sbatch --time=24:00:00 --mem=8g --cpus-per-task=20 ' + scriptname )
            counter = counter + 1 


#

# exit()

