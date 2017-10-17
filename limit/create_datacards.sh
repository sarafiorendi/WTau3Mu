#! /bin/bash

echo "preparing datacard_barrel.txt"
./prepare_card.py --datafile="/eos/cms/store/group/phys_tau/WTau3Mu/mvamet2016/prod_v4/data2016v4_enriched_16oct2017_v4.root" --sigfile="/eos/cms/store/group/phys_tau/WTau3Mu/mvamet2016/prod_v4/signal2016v4_enriched_16oct2017_v4.root" --selection='bdt_proba_v2>0.85 & abs(cand_refit_tau_eta)<1.6' --category='barrel'

echo "preparing datacard_endcap.txt"
./prepare_card.py --datafile="/eos/cms/store/group/phys_tau/WTau3Mu/mvamet2016/prod_v4/data2016v4_enriched_16oct2017_v4.root" --sigfile="/eos/cms/store/group/phys_tau/WTau3Mu/mvamet2016/prod_v4/signal2016v4_enriched_16oct2017_v4.root" --selection='bdt_proba_v2>0.85 & abs(cand_refit_tau_eta)>=1.6' --category='endcap'
