#! /bin/bash

# wps='0.65 0.70 0.75 0.80 0.82 0.84 0.86 0.88 0.89 0.90 0.91 0.92 0.94'
wps='0.89'
for wp in $wps
    do
    echo "WP "$wp
    echo "combining cards: datacard_endcap.txt + datacard_endcap.txt"
    datacard='datacard_endcap'$wp'.txt'
    model='model'$wp'_endcap.root'

    echo "creating model"
    text2workspace.py $datacard -o $model 
    
    echo 'computing the 95% limit'
    combine -M HybridNew --testStat=LHC --frequentist $model -T 2000 --expectedFromGrid 0.5 &> central_0.95_endcap_WP$wp.txt
    combine -M HybridNew --testStat=LHC --frequentist $model -T 2000 --expectedFromGrid 0.16 &> minus_one_sigma_0.95_endcap_WP$wp.txt
    combine -M HybridNew --testStat=LHC --frequentist $model -T 2000 --expectedFromGrid 0.84 &> plus_one_sigma_0.95_endcap_WP$wp.txt
    
#     echo 'computing the 90% limit'
#     combine -M HybridNew --testStat=LHC --frequentist $model -T 2000 --expectedFromGrid 0.5  -C 0.9 &> central_0.90_endcap_WP$wp.txt
#     combine -M HybridNew --testStat=LHC --frequentist $model -T 2000 --expectedFromGrid 0.16 -C 0.9 &> minus_one_sigma_0.90_endcap_WP$wp.txt
#     combine -M HybridNew --testStat=LHC --frequentist $model -T 2000 --expectedFromGrid 0.84 -C 0.9 &> plus_one_sigma_0.90_endcap_WP$wp.txt

    done



