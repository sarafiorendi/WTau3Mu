Limit Computation
=================

To prepare the datacards (the format used in CMS to compute the expected and observed limit) run

```
./create_datacards.sh
```

this script will internally run 

```
./prepare_card.py
```

for two categories, ```barrel``` and ```endcap```.  
The script will produce four files: ```datacard_{barrel|endcap}.txt``` and ```datacard_{barrel|endcap}.root```.  
You can change the sample location and selection to apply in ```create_datacards.sh``` in fact.  

Once the cards are ready you need to move a different CMSSW following the prescriptions and the installation recipes of the [Higgs Combine twiki](https://twiki.cern.ch/twiki/bin/viewauth/CMS/SWGuideHiggsAnalysisCombinedLimit).
There you need to copy (or symlink) this directory with the datacards in it.

The script ```make_limits.sh``` will first combine thw two categories into one and then compute the 90% and 95% expected limits and create 6 txt file (and a bunch of root files) containing the logs and the final results.


## Installing the appropriate `combine`

Stick to 747, 810 crashes.  
https://twiki.cern.ch/twiki/bin/viewauth/CMS/SWGuideHiggsAnalysisCombinedLimit#ROOT6_SLC6_release_CMSSW_7_4_X

```
cmsrel CMSSW_7_4_7
cd CMSSW_7_4_7/src 
cmsenv
git clone https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit
cd HiggsAnalysis/CombinedLimit
cd $CMSSW_BASE/src/HiggsAnalysis/CombinedLimit
git fetch origin
git checkout v6.3.1
scramv1 b clean; scramv1 b # always make a clean build, as scram doesn't always see updates to src/LinkDef.h
```

