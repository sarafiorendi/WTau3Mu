# WTau3Mu

## follow CMGTools installation, then clone this package into `$CMSSW_BASE/src/CMGTools`  

## install a recent version of scikit learn  
You may need to override CMSSW's version of scikit learn in order to evaluate the BDT.  
To do so:  
```
cd CMSSW_8_0_25
cmsenv                                             # this is meant to have CMSSW's python version handy
cd                                                 # go back to your home
python -m pip install --upgrade --user sklearn     # do a local installation of the most recent scikit learn *against the correct python version!!*
```  

Now you only have to import the correct scikit learn module:
* modules are imported ordered as they appear in `sys.path`
* put the path to your local installation *first*, that is `sys.path.insert(0, os.environ['HOME'] + '/.local/lib/python2.7/site-packages')` 
