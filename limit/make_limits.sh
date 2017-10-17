#! /bin/bash

echo "combining cards: datacard_barrel.txt + datacard_endcap.txt"
combineCards.py barrel=datacard_barrel.txt endcap=datacard_endcap.txt > datacard.txt 

echo "creating model"
text2workspace.py datacard.txt -o model.root

echo 'computing the 95% limit'
combine -M HybridNew --testStat=LHC --frequentist model.root -T 2000 --expectedFromGrid 0.5 &> central_0.95.txt
combine -M HybridNew --testStat=LHC --frequentist model.root -T 2000 --expectedFromGrid 0.16 &> plus_one_sigma_0.95.txt
combine -M HybridNew --testStat=LHC --frequentist model.root -T 2000 --expectedFromGrid 0.84 &> minus_one_sigma_0.95.txt

echo 'computing the 90% limit'
combine -M HybridNew --testStat=LHC --frequentist model.root -T 2000 --expectedFromGrid 0.5  -C 0.9 &> central_0.90.txt
combine -M HybridNew --testStat=LHC --frequentist model.root -T 2000 --expectedFromGrid 0.16 -C 0.9 &> plus_one_sigma_0.90.txt
combine -M HybridNew --testStat=LHC --frequentist model.root -T 2000 --expectedFromGrid 0.84 -C 0.9 &> minus_one_sigma_0.90.txt

