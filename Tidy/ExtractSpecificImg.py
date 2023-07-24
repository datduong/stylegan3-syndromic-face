import os,sys,re,pickle 

main_data_dir = '/data/duongdb/ManyFaceConditions08172022/Stylegan3Model/Res256AlignPix0-NoExternalUp1-4/00001-stylegan2-Res256AlignPix0-NoExternalUp1-4-gpus4-batch64-gamma0.2048-multilabel/network-snapshot-001209.pklInterpolate/'
add_name = ''
source = os.path.join(main_data_dir,'8,11,174,11,17T0.6')
output_dir = os.path.join(main_data_dir,'Selected_KS')
if not os.path.exists(output_dir):
  os.mkdir(output_dir)

# 2yBoy_38_0.6
#  '8,15,164,15,16T0.6': 'YoungChildGirlUnaffKS_unaffSetting0.6',
   
list_img = ['seed0038.png']

for img in list_img: 
  for M in ['M0','M.25','M.5','M.75','M1']: # get each mix-ratio 
    source_img = os.path.join(source+M,img)
    output_img = os.path.join(output_dir,M+add_name + img)
    os.system ('scp ' + source_img + ' ' + output_img)

  

