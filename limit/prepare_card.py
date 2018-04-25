#! /bin/env python

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--basedir'   , dest='basedir'   , default='../cfgPython')
parser.add_argument('--jobid'     , dest='jobid'     , default='')
parser.add_argument('--selection' , dest='selection' , default='bdt_proba>0.5')
parser.add_argument('--signalnorm', dest='signalnorm', default=33183./20000.*21490.9*1E-7) # normalize to BR = 1E-7. In this formula: lumi / ngen events * pp->W, BR W->taunu * BR tau->3mu
parser.add_argument('--category'  , dest='category'  , default='')
parser.add_argument('--datafile'  , dest='datafile'  , default=None)
parser.add_argument('--sigfile'   , dest='sigfile'   , default=None)
args = parser.parse_args() 

import ROOT
import os
from math import pi, sqrt
from glob import glob
from pdb import set_trace

ROOT.gROOT.SetBatch()
ROOT.gStyle.SetOptStat(False)
ROOT.TH1.SetDefaultSumw2()
 
##########################################################################################
##      Fit the signal mass distribution
##      - chi2 fit
##      - weighted mass distribution
##########################################################################################

# Load MC file
if not args.sigfile:
    mc_file = '%s/%s/WToTauTo3Mu/WTau3MuTreeProducer/tree.root' % (args.basedir, args.jobid)
    if not os.path.isfile(mc_file):
       raise IOError('I could not find the input MC file: %s' % mc_file)
else:
    mc_file = args.sigfile

if len(args.category)>0:
    args.category = '_'+args.category

gaus = ROOT.TF1('signalgaus', 'gaus', 1.7, 1.86)
   
mc_file = ROOT.TFile.Open(mc_file)
mc_file.cd()
mc_tree = mc_file.Get('tree')

mass_histo_mc = ROOT.TH1F('mass_histo_mc', 'mass_histo_mc', 40, 1.6, 2.)
mc_tree.Draw('cand_refit_tau_mass>>mass_histo_mc', '(' + args.selection + ') * weight * %f' %args.signalnorm)

# make this compatible with different ROOT versions
fit_result_mc = getattr(mass_histo_mc.Fit(gaus, 'RSIQ'), 'Get()', mass_histo_mc.Fit(gaus, 'RSIQ'))

mass_histo_mc.SetMinimum(0.)
mass_histo_mc.Draw('EP')
gaus.Draw('LSAME')
ROOT.gPad.SaveAs('signal%s.pdf' %args.category)

amplitude  = fit_result_mc.Parameter(0)
mean       = fit_result_mc.Parameter(1)
sigma      = fit_result_mc.Parameter(2)

print 'fitted signal gaussian'
print '\tmean  %.3f GeV' %mean
print '\tsigma %.2f MeV' %(sigma*1000.)

##########################################################################################
##      Pick up the observed distribution
##########################################################################################

# Load data files
if not args.datafile:
    data_files = glob('%s/%s/DoubleMuonLowMass_*/WTau3MuTreeProducer/tree.root'% (args.basedir, args.jobid))
    if not data_files:
       raise IOError('I could not find any data file in the %s/%s directory' % (args.basedir, args.jobid))
else:
    data_files = [args.datafile]
print 'found %d input files' % len(data_files)

data_tree = ROOT.TChain('tree')
for fname in data_files:
   data_tree.AddFile(fname)

##########################################################################################
##      Add everything into the workspace
##########################################################################################

# create output file
output = ROOT.TFile.Open('datacard%s.root' %args.category, 'recreate')

# create workspace
print 'creating workspace'
w = ROOT.RooWorkspace('t3m_shapes')

# dump linear parametrization of bkg
# peek at the factory syntax
# https://agenda.infn.it/getFile.py/access?contribId=15&resId=0&materialId=slides&confId=5719
w.factory('mass[%f, %f]' % (1.61, 1.99))
w.factory('a0%s[3]' %(args.category))
w.factory('a1%s[0]' %(args.category))
w.factory('RooPolynomial::bkg(mass,{a0%s, a1%s})' %(args.category, args.category))

# dump signal with fixed shape (the final fit will only vary the normalisation
w.factory('mean[%f]'  % mean)
w.factory('sigma[%f]' % sigma)
w.factory('RooGaussian::sig(mass, mean, sigma)')

# in order to fix the shape, loop over the variables and fix mean and sigma 
it = w.allVars().createIterator()
all_vars = [it.Next() for _ in range( w.allVars().getSize())]
for var in all_vars:
    if var.GetName() in ['mean', 'sigma']:
        var.setConstant()

# dump data
print 'getting data'
selected_tree = data_tree.CopyTree('(' + args.selection + ') & cand_refit_tau_mass>1.61 & cand_refit_tau_mass<1.99')

print 'dumping data'
data =  ROOT.RooDataSet(
    'data_obs', 
    'data_obs',
    selected_tree, 
    ROOT.RooArgSet(w.var('mass'))
)

# import pdb ; pdb.set_trace()

getattr(w,'import')(data)
w.Write()
output.Close()

# dump the datacard
with open('datacard%s.txt' %args.category, 'w') as card:
   card.write(
'''
imax 1 number of bins
jmax * number of processes minus 1
kmax * number of nuisance parameters
--------------------------------------------------------------------------------
shapes background    Wtau3mu{cat}       datacard{cat}.root t3m_shapes:bkg
shapes signal        Wtau3mu{cat}       datacard{cat}.root t3m_shapes:sig
shapes data_obs      Wtau3mu{cat}       datacard{cat}.root t3m_shapes:data_obs
--------------------------------------------------------------------------------
bin               Wtau3mu{cat}
observation       -1
--------------------------------------------------------------------------------
bin                                     Wtau3mu{cat}        Wtau3mu{cat}
process                                 signal              background
process                                 0                   1
rate                                    {signal:.4f}            {bkg:.4f}
--------------------------------------------------------------------------------
bkgNorm{cat}  lnU                       -                   4.00
a0{cat}       flatParam
a1{cat}       flatParam
--------------------------------------------------------------------------------
'''.format(
         cat    = args.category,
         signal = sqrt(2.*pi) * sigma * amplitude / 0.01, # area under the normal divided by the bin width (10 MeV)
         bkg    = data.numEntries()
         )
)

