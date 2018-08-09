import ROOT
import os
from math import pi, sqrt
from glob import glob
from pdb import set_trace

# ROOT.gROOT.SetBatch()
ROOT.gStyle.SetOptStat(False)
ROOT.TH1.SetDefaultSumw2()

ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit.so");

f = ROOT.TFile.Open("datacard_barrel0.89.root")
w = f.Get("t3m_shapes")

mass    = w.var ("mass");
data    = w.data("data_obs");

pdf_nom  = w.pdf ("bkg");
pdf_pol1 = w.pdf ("bkg_pol1");
pdf_pol2 = w.pdf ("bkg_pol2");


## Fit the functions to the data to set the "prefit" state (note this can and should be redone with combine when doing 
## bias studies as one typically throws toys from the "best-fit"

# mass.setRange(1.61,1.71) ;
mass.setRange('Range1',1.61,1.71) ;
mass.setRange('Range2',1.84,1.99) ;

pdf_nom    .fitTo(data, ROOT.RooFit.Range('Range1,Range2'))    ## index 0
pdf_pol1   .fitTo(data, ROOT.RooFit.Range('Range1,Range2'))    ## index 1
pdf_pol2   .fitTo(data, ROOT.RooFit.Range('Range1,Range2'))    ## index 2 


##  	 // Make a plot (data is a toy dataset)
cc   = ROOT.TCanvas()
plot = mass.frame()
data.plotOn(plot, ROOT.RooFit.Range('Range1,Range2'))
pdf_nom  .plotOn(plot,ROOT.RooFit.LineColor(ROOT.kGreen) )
pdf_pol1 .plotOn(plot,ROOT.RooFit.LineColor(ROOT.kBlue)  , ROOT.RooFit.LineStyle(ROOT.kDashed)  )
pdf_pol2 .plotOn(plot,ROOT.RooFit.LineColor(ROOT.kOrange), ROOT.RooFit.LineStyle(ROOT.kDashed)  )

# plot.SetTitle("PDF fits to toy data");
# plot.Draw();
# cc.SaveAs('fits_barrel_excludeBlind.pdf')

cat = ROOT.RooCategory("pdf_index","Index of Pdf which is active");

## Make a RooMultiPdf object. The order of the pdfs will be the order of their index, ie for below 
## 0 == exponential
## 1 == pol1
## 2 == pol2
mypdfs = ROOT.RooArgList()
mypdfs.add(pdf_nom );
mypdfs.add(pdf_pol1);
mypdfs.add(pdf_pol2);


   
multipdf = ROOT.RooMultiPdf("roomultipdf","All Pdfs",cat,mypdfs);

#  As usual make an extended term for the background with _norm for freely floating yield
norm = ROOT.RooRealVar("roomultipdf_norm","Number of background events",0,100000);
norm.setVal(30);

# Save to a new workspace
fout = ROOT.TFile("background_pdfs.root","RECREATE");
wout = ROOT.RooWorkspace("backgrounds","backgrounds");
getattr(wout, 'import')(cat     )#, ROOT.RooFit.Rename(cat.GetName())      )
getattr(wout, 'import')(norm    )#, ROOT.RooFit.Rename(norm.GetName())     )
getattr(wout, 'import')(multipdf)#, ROOT.RooFit.Rename(multipdf.GetName()) )

wout.Print();
wout.Write();

fout.Close()
