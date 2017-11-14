#! /bin/bash

data="/eos/cms/store/group/phys_tau/WTau3Mu/mvamet2016/prod_v4/data2016v4_enriched_16oct2017_v4.root"
mc="/eos/cms/store/group/phys_tau/WTau3Mu/mvamet2016/prod_v4/signal2016v4_enriched_16oct2017_v4.root"
wps='0.65 0.70 0.75 0.80 0.85 0.90 0.92'

for wp in $wps
    do
    selection='bdt_proba_v2>'$wp
    ./prepare_card.py --selection=$selection'& abs(cand_refit_tau_eta)<1.6'  --category='barrel'$wp --datafile=$data --sigfile=$mc 
    ./prepare_card.py --selection=$selection'& abs(cand_refit_tau_eta)>=1.6' --category='endcap'$wp --datafile=$data --sigfile=$mc
    done
