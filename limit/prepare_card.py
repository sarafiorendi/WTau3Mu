#! /bin/env python

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--basedir'  , dest='basedir'  , default='../cfgPython')
parser.add_argument('--jobid'    , dest='jobid'    , default='')
parser.add_argument('--selection', dest='selection', default='bdt_proba>0.5')
args = parser.parse_args() 

import ROOT
import os
from pdb import set_trace

#Load MC file
mc_file = '%s/%s/WToTauTo3Mu/WTau3MuTreeProducer/tree.root' % (args.basedir, args.jobid)
if not os.path.isfile(mc_file):
   raise IOError('I could not find the input MC file: %s' % mc_file)

mc_file = ROOT.TFile.Open(mc_file)
mc_tree = mc_file.Get('tree').CopyTree(args.selection)

#dump tree into a RooDataset
mass = ROOT.RooRealVar(
   'cand_refit_tau_mass', 'cand_refit_tau_mass', 
   1.61, 2
#    1.7, 1.86
   )

mc_data =  ROOT.RooDataSet(
   'mc_data', 'mc_data',
   mc_tree, ROOT.RooArgSet(mass)
)

#fit gaussian to signal
mean = ROOT.RooRealVar(
   'mean_mc', 'mean_mc', 
   1.78, 1.7, 1.85
   )
sigma = ROOT.RooRealVar(
   'sigma_mc', 'sigma_mc', 
   0.2, 0, 1
)
gauss = ROOT.RooGaussian(
   'signal', 'signal',
   mass, mean, sigma
)
fit_result = gauss.fitTo(mc_data)

#plot
canvas = ROOT.TCanvas(
   "asdf", "asdf", 
   800, 800
   )
canvas.Draw()

frame = mass.frame(
   ROOT.RooFit.Title("Efficiency"),
   ROOT.RooFit.Range(mass.getMin(), mass.getMax())
)

gauss.plotOn(
   frame,
   ROOT.RooFit.LineColor(ROOT.kBlue),
#    ROOT.RooFit.VisualizeError(fit_result, 1.0),
#    ROOT.RooFit.FillColor(ROOT.kAzure - 9)
   )
mc_data.plotOn(frame)

frame.GetYaxis().SetTitle("Efficiency")
frame.GetXaxis().SetTitle('Mass [GeV]')
frame.Draw()
# canvas.SetLogy(True)
plot_name = 'signal_shape.png'
print "Saving fit plot in %s" % plot_name
canvas.SaveAs(plot_name)
canvas.SaveAs(plot_name.replace('.png', '.pdf'))

#Load data files
from glob import glob
data_files = glob(
   '%s/%s/DoubleMuonLowMass_*/WTau3MuTreeProducer/tree.root'% (args.basedir, args.jobid)
   )
if not data_files:
   raise IOError('I could not find any data file in the %s/%s directory' % (args.basedir, args.jobid))
else:
   print 'found %d input files' % len(data_files)

data_tree = ROOT.TChain('tree')
for fname in data_files:
   data_tree.AddFile(fname)

#create output file
output = ROOT.TFile.Open('datacard.root', 'recreate')

#create workspace
print 'creating workspace'
w = ROOT.RooWorkspace('t3m_shapes')

#dump linear parametrization of bkg
# peek at the factory syntax
# https://agenda.infn.it/getFile.py/access?contribId=15&resId=0&materialId=slides&confId=5719
w.factory('mass[%f, %f]' % (mass.getMin(), mass.getMax()))
# w.factory('slope[0]')
# w.factory('intercept[0]')
w.factory('a0[3]')
w.factory('a1[0]')
w.factory('RooPolynomial::bkg(mass,{a0, a1})')

# w.factory('RooPolynomial::bkg(mass, slope)')
# w.factory('expr::bkg("@0+@1*@2", intercept, slope, mass)')

#dump signal with fixed shape
w.factory('mean[%f]' % mean.getVal())
w.factory('sigma[%f]' % sigma.getVal())
w.factory('RooGaussian::sig(mass, mean, sigma)')

it = w.allVars().createIterator()
all_vars = [it.Next() for _ in range( w.allVars().getSize())]
for var in all_vars:
    if var.GetName() != 'mass':
       var.setConstant()

#dump data
print 'getting data'
selected_tree = data_tree.CopyTree(args.selection)

print 'dumping data'
data =  ROOT.RooDataSet(
   'data_obs', 'data_obs',
   selected_tree, ROOT.RooArgSet(w.var('mass'))
)
getattr(w,'import')(data)
w.Write()
output.Close()

with open('datacard.txt', 'w') as card:
   card.write(
'''
imax 1 number of bins
jmax * number of processes minus 1
kmax * number of nuisance parameters
--------------------------------------------------------------------------------
shapes background    Wtau3mu      datacard.root t3m_shapes:bkg
shapes signal        Wtau3mu      datacard.root t3m_shapes:sig
shapes data_obs      Wtau3mu      datacard.root t3m_shapes:data_obs
--------------------------------------------------------------------------------
bin               Wtau3mu
observation       -1
--------------------------------------------------------------------------------
bin                                     Wtau3mu             Wtau3mu
process                                 signal              background
process                                 0                   1
rate                                    {signal:.4f}            {bkg:.4f}
--------------------------------------------------------------------------------
bkgNorm       lnU                       -                   4.00
a0            flatParam
a1            flatParam
--------------------------------------------------------------------------------
'''.format(
         signal=mc_data.numEntries(),
         bkg=data.numEntries()
         )
)

# slope         flatParam
# intercept     flatParam
