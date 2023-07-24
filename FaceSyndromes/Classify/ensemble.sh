
# z = """
# b4ns448wl10ss10lr3e-05dp0.2b64ntest1WS+22q11DS+Control+Normal+Whole+blankcenter                       
# b4ns448Wl10ss10lr3e-05dp0.2b64ntest1T0.6WS+22q11DS+Control+Normal+kimg10+target0.6+TransA+blankcenter 
# b4ns448Wl10ss10lr3e-05dp0.2b64ntest1T0.6WS+22q11DS+Control+Normal+kimg10+target0.6+DiscA+blankcenter
# b4ns448Wl10ss10lr3e-05dp0.2b64ntest1M1T0.6WS+22q11DS+Control+Normal+kimg10+target0.6+blankcenter   
# b4ns448Wl10ss10lr3e-05dp0.2b64ntest1M0.75T0.6WS+22q11DS+Control+Normal+kimg10+target0.6+blankcenter
# b4ns448Wl10ss10lr3e-05dp0.2b64ntest1M0.55T0.6AveWS+22q11DS+Control+Normal+kimg10+target0.6+blankcenter
# b4ns448Wl10ss10lr3e-05dp0.2b64ntest1M0.75T0.6AveWS+22q11DS+Control+Normal+kimg10+target0.6+blankcenter
# b4ns448Wl10ss10lr3e-05dp0.2b64ntest1M1T0.6AveWS+22q11DS+Control+Normal+kimg10+target0.6+blankcenter""".split()
# ' '.join(s.strip() for s in z)

# ! not split by age group 

source /data/$USER/conda/etc/profile.d/conda.sh
conda activate py37

cd /data/duongdb/ClassifyFaceConditions

for modelname in b4ns448wl10ss10lr3e-05dp0.2b64ntest1WS+22q11DS+Control+Normal+Whole+blankcenter 
do
cd /data/duongdb/ClassifyFaceConditions
output_name='Res1024WS22qOther10kNormalGenderNpr0Up10Sg2-StaticT0.8'
keyword=$output_name'_from_fold'
modeldir="/data/duongdb/WS22qOther_08102021/Classify/"$modelname
labels='22q11DS,Controls,Normal,WS' # '22q11DS,Controls,WS' # '22q11DS,Controls,Normal,WS' 'Controls,Normal,WS' 
python3 ensemble_our_classifier.py --model-dir $modeldir --labels $labels --output_name $output_name --keyword $keyword
done 
cd $modeldir

# ----------------------------------------------------------------------------------------------------------------



# ! copy to local pc

mkdir /cygdrive/c/Users/duongdb/Documents/WS22qOther_08102021/Classify/
for modelname in b4ns448Wl10ss10lr3e-05dp0.2b64ntest1T0.6WS+22q11DS+Control+Normal+kimg10+target0.6+TransA+blankcenter 
do
mkdir /cygdrive/c/Users/duongdb/Documents/WS22qOther_08102021/Classify/$modelname
cd /cygdrive/c/Users/duongdb/Documents/WS22qOther_08102021/Classify/$modelname
scp -r $biowulf:/data/duongdb/WS22qOther_08102021/Classify/$modelname/*png .
scp -r $biowulf:/data/duongdb/WS22qOther_08102021/Classify/$modelname/final*csv .
done 

M6Rs5pMgooNi3bie
