#! /bin/bash

# wps='0.65 0.70 0.75 0.80 0.82 0.84 0.86 0.88 0.89 0.90 0.91 0.92 0.94'
wps='0.89'
for wp in $wps
    do
    echo "WP "$wp
    echo "combining cards: datacard_barrel.txt + datacard_endcap.txt"
    barrel='datacard_barrel'$wp'.txt'
    endcap='datacard_endcap'$wp'.txt'
    datacard='datacard'$wp'.txt'
    model='model'$wp'.root'
    combineCards.py barrel=$barrel endcap=$endcap > $datacard

    echo "creating model"
    text2workspace.py $datacard -o $model 
    
    echo 'computing the 95% limit'
    combine -M HybridNew --testStat=LHC --frequentist $model -T 2000 --expectedFromGrid 0.5  --plot=limit_scan_central_0.95_WP$wp.png --rMin 1 --rMax 3 &> central_0.95_WP$wp.txt
    combine -M HybridNew --testStat=LHC --frequentist $model -T 2000 --expectedFromGrid 0.16 --plot=limit_scan_minus_0.95_WP$wp.png   --rMin 1 --rMax 3 &> plus_one_sigma_0.95_WP$wp.txt
    combine -M HybridNew --testStat=LHC --frequentist $model -T 2000 --expectedFromGrid 0.84 --plot=limit_scan_plus_0.95_WP$wp.png    --rMin 1 --rMax 3 &> minus_one_sigma_0.95_WP$wp.txt
    
    echo 'computing the 90% limit'
    combine -M HybridNew --testStat=LHC --frequentist $model -T 2000 --expectedFromGrid 0.5  -C 0.9 --plot=limit_scan_central_0.90_WP$wp.png --rMin 1 --rMax 3 &> central_0.90_WP$wp.txt
    combine -M HybridNew --testStat=LHC --frequentist $model -T 2000 --expectedFromGrid 0.16 -C 0.9 --plot=limit_scan_minus_0.90_WP$wp.png   --rMin 1 --rMax 3 &> minus_one_sigma_0.90_WP$wp.txt
    combine -M HybridNew --testStat=LHC --frequentist $model -T 2000 --expectedFromGrid 0.84 -C 0.9 --plot=limit_scan_plus_0.90_WP$wp.png    --rMin 1 --rMax 3 &> plus_one_sigma_0.90_WP$wp.txt

    done



# combine central_0.90_WP0.89.txt -M HybridNew --LHCmode LHC-limits


#     combine -M HybridNew --testStat=LHC --frequentist model0.89.root -T 2000 --expectedFromGrid 0.5  -C 0.9 --plot=limit_scan.png --rMin=0 --rMax=4 &> central_0.90_WP_test.txt



# ombine -M HybridNew --testStat=LHC --frequentist model0.89.root -T 6000 --expectedFromGrid 0.5 -C 0.9 --rMin 1 --rMax 8