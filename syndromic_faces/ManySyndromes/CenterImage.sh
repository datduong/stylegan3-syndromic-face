
source /data/$USER/conda/etc/profile.d/conda.sh
conda activate py37
module load CUDA/11.0
module load cuDNN/8.0.3/CUDA-11.0
module load gcc/8.3.0


# sbatch --partition=gpu --time=2-00:00:00 --gres=gpu:v100x:2 --mem=24g --cpus-per-task=24 
# sbatch --partition=gpu --time=2:30:00 --gres=gpu:p100:1 --mem=8g --cpus-per-task=8 
# sinteractive --time=1:30:00 --gres=gpu:p100:1 --mem=4g --cpus-per-task=4


# ! crop, zoom a little bit, and no background 
for type in BWS CdLS Down KS NS PWS RSTS1 WHS        
do 
rm /data/duongdb/ManyFaceConditions01312022/$type/Slide1.PNG
done 

# ! cut out white space. 
headfolder=/data/duongdb/ManyFaceConditions01312022
mkdir $headfolder/TrimImg # ! all images will be in same folder, we need to run the @extract_code 
outfolder_name=/data/duongdb/ManyFaceConditions01312022/TrimImg
codepath=$datadir/stylegan3-FaceSyndromes/syndromic_faces/ManySyndromes # ! 
cd $codepath
for type in KS # Unaffected # BWS CdLS Down KS NS PWS RSTS1 WHS 
do 
  datapath=$headfolder/$type
  python3 CropWhiteSpace.py --folder_name $datapath --padding 0 --outformat png --label $type --outfolder_name $outfolder_name > $type'trim_log.txt' # ! @png is probably best for ffhq style @'dummy' is a hack
done 
cd $headfolder/TrimImg


# ! cut out white space ---- specialized powerpoint 
headfolder=/data/duongdb/ManyFaceConditions01312022
mkdir $headfolder/TrimImgQualtricExample # ! all images will be in same folder, we need to run the @extract_code 
outfolder_name=/data/duongdb/ManyFaceConditions01312022/TrimImgQualtricExample
codepath=$datadir/stylegan3-FaceSyndromes/syndromic_faces/ManySyndromes # ! 
cd $codepath
for type in ExampleSurveyIRB01312022 
do 
  datapath=$headfolder/$type
  python3 CropWhiteSpace.py --folder_name $datapath --padding 0 --outformat png --label ExampleSurveyIRB01312022 --outfolder_name $outfolder_name > $type'trim_log.txt' # ! @png is probably best for ffhq style @'dummy' is a hack
done 
cd $headfolder/TrimImgExampleSurveyIRB01312022

resolution=512
datapath=/data/duongdb/ManyFaceConditions01312022/
codepath=$datadir/stylegan3-FaceSyndromes/syndromic_faces/ManySyndromes # ! 
cd $codepath
python3 AlignImage.py --input_file_path $datapath/TrimImgExampleSurveyIRB01312022 --output_file_path $datapath/Align$resolution'ExampleSurveyIRB01312022' --output_size $resolution --centerface '0,0,512,512' --notblur > $codepath/ExampleSurveyIRB01312022.txt # --whitebackground



# ! align images into ffhq format # this has to be done so we can greatly leverage transfer-ability of ffhq
resolution=512
datapath=/data/duongdb/ManyFaceConditions01312022/
codepath=$datadir/stylegan3-FaceSyndromes/syndromic_faces/ManySyndromes # ! 
cd $codepath
python3 AlignImage.py --input_file_path $datapath/TrimImg --output_file_path $datapath/Align$resolution'Center' --output_size $resolution --centerface '0,0,512,512' --notblur > $codepath/align_log_background_many_conditions.txt
# '50,50,974,974'

# ! remove background 
python3 RemoveBackground.py --imagepath $datapath/Align$resolution'Center' --foutpath $datapath/Align$resolution'CenterRmBg' --colorcode 0 

# ! need to realign WS and 22q? remove background of WS and 22q? 
resolution=1024
datapath=/data/duongdb/ManyFaceConditions01312022/
codepath=$datadir/stylegan3-FaceSyndromes/syndromic_faces/ManySyndromes # ! 
cd $codepath
python3 AlignImage.py --input_file_path $datapath/TrimImg --output_file_path $datapath/Align$resolution'BlankBackgroundCenter' --output_size $resolution --centerface '50,50,974,974' --notblur > $codepath/align_log_background_many_conditions.txt
# '50,50,974,974'

python3 RemoveBackground.py --imagepath $datapath/Align$resolution'BlankBackgroundCenter' --foutpath $datapath/Align$resolution'RmBgCenter' --colorcode 0 


# ! make csv 
datapath=/data/duongdb/ManyFaceConditions01312022/
codepath=$datadir/stylegan3-FaceSyndromes/syndromic_faces/ManySyndromes # ! 
extracsv=/data/duongdb/WS22qOther_12082021/WS22qOther10kNormalGenderNpr0.csv # ! add more images 
cd $codepath
python3 MakeCsv.py --outputname $datapath/'ManyCondition+10kNormal.csv' --imagepath $datapath/Align1024BlankBackgroundCenter --extracsv $extracsv --headfolder '/data/duongdb/ManyFaceConditions01312022'



# ! make json 
datapath=/data/duongdb/ManyFaceConditions01312022/
codepath=$datadir/stylegan3-FaceSyndromes/syndromic_faces/ManySyndromes # ! 
cd $codepath
experimentname=ManyCondition+10kNormal-Other
json_path=$datapath/$experimentname.json
csv_label=$datapath/ManyCondition+10kNormal.csv
new_df_path=$datapath/$experimentname.csv
python3 MakeLabelJson.py --json_path $json_path --csv_label $csv_label --disease 'WS,22q11DS,Normal,BWS,CdLS,Down,KS,NS,PWS,RSTS1,WHS' --gender --skip_controls --new_df_path $new_df_path


# ! make json + skip age, disease label only 
datapath=/data/duongdb/ManyFaceConditions01312022/
codepath=$datadir/stylegan3-FaceSyndromes/syndromic_faces/ManySyndromes # ! 
cd $codepath
experimentname=ManyCondition+10kNormal-Other-SkipAge-SkipGender
json_path=$datapath/$experimentname.json
csv_label=$datapath/ManyCondition+10kNormal.csv
new_df_path=$datapath/$experimentname.csv
python3 MakeLabelJson.py --json_path $json_path --csv_label $csv_label --disease 'WS,22q11DS,Normal,BWS,CdLS,Down,KS,NS,PWS,RSTS1,WHS' --skip_controls --new_df_path $new_df_path --skip_age 

# --gender
# --skip_normal # ! fix @disease if add in normal

# Normal


# 
# ! make json ... skip normal 
datapath=/data/duongdb/ManyFaceConditions01312022/
codepath=$datadir/stylegan3-FaceSyndromes/syndromic_faces/ManySyndromes # ! 
cd $codepath
experimentname=ManyCondition-Normal-Other
json_path=$datapath/$experimentname.json
csv_label=$datapath/ManyCondition+10kNormal.csv
new_df_path=$datapath/$experimentname.csv
python3 MakeLabelJson.py --json_path $json_path --csv_label $csv_label --disease 'WS,22q11DS,BWS,CdLS,Down,KS,NS,PWS,RSTS1,WHS' --gender --skip_controls --new_df_path $new_df_path --skip_normal

# ['22q11DS', 'BWS', 'CdLS', 'Down', 'KS', 'NS', 'Normal', 'PWS', 'RSTS1', 'WHS', 'WS']


# ! make data into pytorch image datast 
datapath=/data/duongdb/

source_in=$datapath/ManyFaceConditions01312022/Align1024BlankBackgroundCenter/

upsample='2-10'

# '{"label1":[0,11],"label2":[11,16],"label3":[16,18]}'


for resolution in 256 # 1024 256
do 

  csvjsonbasename=ManyCondition+10kNormal-Other-SkipAge-SkipGender # ! NAME OF CSV INPUT AND JSON

  dest_folder=$datapath/ManyFaceConditions01312022/Res$resolution$csvjsonbasename'Up'$upsample

  img_csv=$datapath/ManyFaceConditions01312022/$csvjsonbasename.csv
  meta_fname=$datapath/ManyFaceConditions01312022/$csvjsonbasename.json

  cd /data/duongdb/stylegan3-FaceSyndromes
  python dataset_tool.py --source $source_in --dest $dest_folder --resolution=$resolution'x'$resolution --img-csv $img_csv --meta-fname $meta_fname --upsample-label-dict '{"22q11DS":2, "BWS":10, "CdLS":10, "Down":10, "KS":10, "NS":10, "PWS":10, "RSTS1":10, "WHS":10, "WS":2}'

  # '{"22q11DS":1, "BWS":4, "CdLS":4, "Down":4, "KS":4, "NS":4, "PWS":4, "RSTS1":4, "WHS":4, "WS":1}'
  # '{"22q11DS":2, "BWS":10, "CdLS":10, "Down":10, "KS":10, "NS":10, "PWS":10, "RSTS1":10, "WHS":10, "WS":2}'
  # '{"22q11DS":4, "BWS":20, "CdLS":20, "Down":20, "KS":20, "NS":20, "PWS":20, "RSTS1":20, "WHS":20, "WS":4}'
  # python dataset_tool.py --source $source_in --dest $dest_folder --resolution=$resolution'x'$resolution --img-csv $img_csv --meta-fname $meta_fname 

done 

cd $dest_folder



# ! make data into pytorch image datast, single disease, no label 
datapath=/data/duongdb/

source_in=$datapath/ManyFaceConditions01312022/DownSyndromeImg/

for resolution in 256 # 1024 256
do 

  csvjsonbasename=DownSyndromeImg # ! NAME OF CSV INPUT AND JSON

  dest_folder=$datapath/ManyFaceConditions01312022/Res$resolution$csvjsonbasename

  # img_csv=$datapath/ManyFaceConditions01312022/$csvjsonbasename.csv
  # meta_fname=$datapath/ManyFaceConditions01312022/$csvjsonbasename.json

  cd /data/duongdb/stylegan3-FaceSyndromes
  python dataset_tool.py --source $source_in --dest $dest_folder --resolution=$resolution'x'$resolution 

  # '{"22q11DS":1, "BWS":4, "CdLS":4, "Down":4, "KS":4, "NS":4, "PWS":4, "RSTS1":4, "WHS":4, "WS":1}'
  # '{"22q11DS":2, "BWS":10, "CdLS":10, "Down":10, "KS":10, "NS":10, "PWS":10, "RSTS1":10, "WHS":10, "WS":2}'
  # '{"22q11DS":4, "BWS":20, "CdLS":20, "Down":20, "KS":20, "NS":20, "PWS":20, "RSTS1":20, "WHS":20, "WS":4}'
  # python dataset_tool.py --source $source_in --dest $dest_folder --resolution=$resolution'x'$resolution --img-csv $img_csv --meta-fname $meta_fname 

done 

cd $dest_folder


