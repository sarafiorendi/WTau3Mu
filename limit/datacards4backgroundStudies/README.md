Fit bias studies

## as from https://cms-hcomb.gitbooks.io/combine/content/part3/nonstandard.html#roomultipdf-conventional-bias-studies
1. produce datacards with prepare_cards.py
2. install HiggsCombine to have RooMultiPdf.h class
3. run multifit.py to create new workspace with new pdfs
4. copy datacards and backgrounds.root to the release where HiggsCombine is working
5. create toys with 
"
combine datacard_barrel0.89.txt -M GenerateOnly --setParameters pdf_index=0 --toysFrequentist -t 1000 --expectSignal 1.6 --saveToys -m 1.776 --freezeParameters pdf_index
"
6. fit toys with
"
combine datacard_barrel0.89.txt -M FitDiagnostics  --setParameters pdf_index=1 --toysFile higgsCombineTest.GenerateOnly.mH1.776.123456.root  -t 1000 --rMin -10 --rMax 10 --freezeParameters pdf_index
"
