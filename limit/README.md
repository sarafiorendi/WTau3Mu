Limit Computation
=================

To prepare the datacards (the format used in CMS to compute the expected and observed limit) run

```
./prepare_card.py $JOBID $CUT
```

Where $JOBID is the name of the production you want to use, which is also the name of the directory in ```../cfgPython/```. $CUT is the usual ROOT string selection you want to apply to the ROOT trees produced in your job directory.

The script will produce two files: ```datacard.txt``` and ```datacard.root```.

Once the cards are ready you need to move a different CMSSW following the prescriptions and the installation recipes of the [Higgs Combine twiki](https://twiki.cern.ch/twiki/bin/viewauth/CMS/SWGuideHiggsAnalysisCombinedLimit).
There you need to copy (or symlink) this directory with the datacards in it.

The script ```make_limits.sh``` will compute the 90% and 95% expected limits and create 6 txt file (and a bunch of root files) containing the logs and the final results.