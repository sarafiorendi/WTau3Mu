#! /bin/env python

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--basedir'   , dest='basedir'   , default='../cfgPython')
parser.add_argument('--jobid'     , dest='jobid'     , default='')
parser.add_argument('--selection' , dest='selection' , default='bdt_proba>0.5')
# parser.add_argument('--signalnorm', dest='signalnorm', default=33183./20000.*21490.9*1E-7) # normalize to BR = 1E-7. In this formula: lumi / ngen events * pp->W, BR W->taunu * BR tau->3mu

# http://inspirehep.net/record/1404393/files/SMP-15-004-pas.pdf
# measured cross section multiplied by BR(W->taunu) / BR(W->munu)
parser.add_argument('--signalnorm', dest='signalnorm', default=33183./20000.*(8580+11370)*0.1138/0.1063*1E-7)
parser.add_argument('--category'  , dest='category'  , default='')
parser.add_argument('--datafile'  , dest='datafile'  , default=None)
parser.add_argument('--sigfile'   , dest='sigfile'   , default=None)
args = parser.parse_args() 



import ROOT
import os
from math import pi, sqrt
from glob import glob
from pdb import set_trace
from array import array 
import math

# ROOT.gROOT.SetBatch()
ROOT.gStyle.SetOptStat(True)
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

# dump data
print 'getting data'
selected_tree = data_tree.CopyTree('(' + args.selection + ') & cand_refit_tau_mass>1.61 & cand_refit_tau_mass<1.99')

# fix variable name
newtree = ROOT.TTree('newtree','newtree')
imass = array( 'f', [ 0 ] )
newtree.Branch('mass', imass, 'mass/F')

sara = ROOT.TCanvas()
for event in selected_tree:
    imass[0] = event.cand_refit_tau_mass
    newtree.Fill()

mass_histo_data = ROOT.TH1F('mass_histo_data', 'mass_histo_data', 40, 1.6, 2)
newtree.Draw('mass >> mass_histo_data', 'mass<1.72 | mass > 1.84')

def fline(x, par):
    if reject and x[0] > 1.72 and x[0] < 1.84:
        ROOT.TF1.RejectPoint()
        return 0
    return math.exp(par[0] + par[1]*x[0])

expo = ROOT.TF1('expo', fline, 1.61, 1.99, 2)
expo.SetParameters(0,0)
expo.SetLineColor(ROOT.kBlue)
reject = True
fit_result_data = getattr(mass_histo_data.Fit(expo, 'RSIQL'), 'Get()', mass_histo_data.Fit(expo, 'RSIQL')) # we want a likelihood fit because we want to count empty bins too
expo.Draw('SAMEL')
# slope = fit_result_data.Parameter(1)
ROOT.gPad.Update()

sara.SaveAs('bkg%s.pdf'%(args.category))

# final histo
ROOT.gStyle.SetOptStat(0)
mycanvas = ROOT.TCanvas('mycanvas', '', 700, 700)
mycanvas.cd()
expo_tot = ROOT.TF1('fl', 'expo', 1.61, 1.99, 2)
expo_tot.SetParameters(expo.GetParameters())

# area under the expo
def integ(p0, p1, xmin, xmax, binwidth=0.01):
    primitive = lambda x : 1./p1 * math.exp(p0 + p1 * x)
    result = primitive(xmax) - primitive(xmin) 
    return result/binwidth
    
p0 = expo.GetParameter(0)
p1 = expo.GetParameter(1)
total_bkg = integ(p0, p1, 1.61, 1.99)

# import pdb ; pdb.set_trace()

mass_histo_data.GetListOfFunctions().Remove(mass_histo_data.GetListOfFunctions()[0]) # ROOT, what's not to love?

mass_histo_data.SetTitle(args.category)
mass_histo_data.GetXaxis().SetTitle('m_{3#mu} [GeV]')
mass_histo_data.GetYaxis().SetTitle('events / 10 MeV')
mass_histo_data.GetYaxis().SetTitleOffset(1.4)

mass_histo_data.SetLineColor   (ROOT.kBlack)
mass_histo_data.SetMarkerColor(ROOT.kBlack)
mass_histo_data.SetMarkerStyle(8)
mass_histo_mc  .SetLineColor(ROOT.kRed  )
mass_histo_mc  .SetFillColor(ROOT.kRed  )
mass_histo_mc  .SetFillStyle(3004)

mass_histo_data.Draw('EP')
mass_histo_mc  .Draw('HISTSAME')
expo_tot.SetLineColor(ROOT.kBlack)
expo_tot.Draw('SAMEL')
gaus.Draw('SAMEL')

combo = ROOT.TF1('combo', 'expo(0) + gaus(2)', 1.61, 1.99)
combo.SetLineColor(ROOT.kGray+1)
combo.SetLineStyle(2)
combo.SetParameter(0, expo.GetParameter(0))
combo.SetParameter(1, expo.GetParameter(1))
combo.SetParameter(2, gaus.GetParameter(0))
combo.SetParameter(3, gaus.GetParameter(1))
combo.SetParameter(4, gaus.GetParameter(2))
combo.Draw('SAMEL')

mycanvas.Update()

mycanvas.SaveAs('final_mass_plot_%s.pdf'%(args.category))

ROOT.gStyle.SetOptStat(True)

mass = ROOT.RooRealVar('mass','mass',1.61,1.99)

print 'dumping data'
data =  ROOT.RooDataSet(
    'data_obs', 
    'data_obs',
    newtree, 
    ROOT.RooArgSet(mass)
)

# create workspace
print 'creating workspace'
w = ROOT.RooWorkspace('t3m_shapes')

# dump linear parametrization of bkg
# peek at the factory syntax
# https://agenda.infn.it/getFile.py/access?contribId=15&resId=0&materialId=slides&confId=5719

# first order poly
w.factory('mass[%f, %f]' % (1.61, 1.99))
# w.factory('a0%s[%.3f,-10,0.001]' %(args.category, max(slope, 0.)))
# w.factory('a0%s[%.3f,-10,0.001]' %(args.category, slope))
# w.factory('a0%s[%.3f,-10,0.001]' %(args.category, 1))
# w.factory('RooPolynomial::bkg(mass,{a0%s})' %args.category)
w.factory("Exponential::bkg(mass, a0%s[-0.2,-100,100])" %(args.category) )  
# w.var('a0%s' %(args.category)).setError(0.01)

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
rate                                    {signal:.4f}        {bkg:.4f}
--------------------------------------------------------------------------------
bkgNorm{cat}  lnU                       -                   4.00
a0{cat}       flatParam
lumi          lnN                       1.025               -   
xs_W          lnN                       1.037               -   
br_Wtaunu     lnN                       1.0021              -   
br_Wmunu      lnN                       1.0015              -   
mc_stat{cat}  lnN                       {mcstat:.4f}        -   
mu_id{cat}    lnN                       {mu_id:.4f}         -   
mu_hlt{cat}   lnN                       {mu_hlt:.4f}        -   
trk_hlt{cat}  lnN                       {trk_hlt:.4f}       -   
hlt_extrap    lnN                       1.05                -   
--------------------------------------------------------------------------------
'''.format(
         cat    = args.category,
         signal = sqrt(2.*pi) * sigma * amplitude / 0.01, # area under the normal divided by the bin width (10 MeV)
         bkg    = total_bkg, #data.numEntries(),
         mcstat = 1. + sqrt(mass_histo_mc.Integral()/args.signalnorm)/mass_histo_mc.Integral()*args.signalnorm,
         mu_id  = 1.044  if 'barrel' in args.category else 1.078,
         mu_hlt = 1.012  if 'barrel' in args.category else 1.040,
         trk_hlt= 1.0086 if 'barrel' in args.category else 1.0086,
         )
)


# import pdb ; pdb.set_trace()
