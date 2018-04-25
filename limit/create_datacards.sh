#! /bin/bash

data="/eos/user/m/manzoni/WTau3Mu/ntuples_16_4_2018/data_enriched_16apr2018v16.root"
mc="/eos/user/m/manzoni/WTau3Mu/ntuples_16_4_2018/signal_enriched_16apr2018v16.root"
# wps='0.65 0.70 0.75 0.80 0.85 0.90 0.92'
wps='0.65 0.70 0.75 0.80 0.82 0.84 0.86 0.88 0.89 0.90 0.91 0.92 0.94'

for wp in $wps
    do
    selection='bdt>'$wp
    ./prepare_card.py --selection=$selection'& abs(cand_charge)==1 & abs(cand_refit_tau_eta)<1.6'  --category='barrel'$wp --datafile=$data --sigfile=$mc 
    ./prepare_card.py --selection=$selection'& abs(cand_charge)==1 & abs(cand_refit_tau_eta)>=1.6' --category='endcap'$wp --datafile=$data --sigfile=$mc
    done

# for wp in $wps
#     do
#     selection='bdt>'$wp
#     ./prepare_card.py --selection=$selection'& abs(cand_charge)==1 & & abs(cand_refit_tau_eta)<1.6  & (!(cand_refit_charge12==0 & abs(cand_refit_mass12-1.0195)<0.014) & !(cand_refit_charge13==0 & abs(cand_refit_mass13-1.0195)<0.014) & !(cand_refit_charge23==0 & abs(cand_refit_mass23-1.0195)<0.014))'  --category='barrel'$wp --datafile=$data --sigfile=$mc 
#     ./prepare_card.py --selection=$selection'& abs(cand_charge)==1 & & abs(cand_refit_tau_eta)>=1.6 & (!(cand_refit_charge12==0 & abs(cand_refit_mass12-1.0195)<0.014) & !(cand_refit_charge13==0 & abs(cand_refit_mass13-1.0195)<0.014) & !(cand_refit_charge23==0 & abs(cand_refit_mass23-1.0195)<0.014))' --category='endcap'$wp --datafile=$data --sigfile=$mc
#     done

