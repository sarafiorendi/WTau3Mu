import os
import pickle

import ROOT
from ROOT import gSystem, gROOT

from CMGTools.H2TauTau.proto.plotter.PlotConfigs import SampleCfg
from CMGTools.WTau3Mu.samples.mc_2016            import WToTauTo3Mu
from CMGTools.WTau3Mu.samples.data_2016          import datasamplesDoubleMuLowMass, DoubleMuonLowMass_Run2016Bv1_03Feb2017, DoubleMuonLowMass_Run2016Bv2_03Feb2017, DoubleMuonLowMass_Run2016C_03Feb2017, DoubleMuonLowMass_Run2016D_03Feb2017, DoubleMuonLowMass_Run2016E_03Feb2017, DoubleMuonLowMass_Run2016F_03Feb2017, DoubleMuonLowMass_Run2016G_03Feb2017, DoubleMuonLowMass_Run2016Hv2_03Feb2017, DoubleMuonLowMass_Run2016Hv3_03Feb2017

def createSampleLists(analysis_dir = '/afs/cern.ch/user/s/steggema/work/public/mt/NewProd',
                      signal_scale = 1.,
                      no_data      = False):
    
    tree_prod_name = 'WTau3MuTreeProducer'

    samples_mc = [
        SampleCfg(name           = 'Signal', 
                  dir_name       = 'WToTauTo3Mu', 
                  ana_dir        = analysis_dir, 
                  tree_prod_name = tree_prod_name,
                  xsec           = WToTauTo3Mu.xSection, 
                  sumweights     = WToTauTo3Mu.nGenEvents, 
                  weight_expr    = '1.',
                  is_signal      = True,),
    ]

    samples_data = [
        SampleCfg(name           = 'data_obs', 
                  dir_name       = 'DoubleMuonLowMass_Run2016Bv2_03Feb2017', 
                  ana_dir        = analysis_dir, 
                  tree_prod_name = tree_prod_name, 
                  is_data        = True),
        SampleCfg(name           = 'data_obs', 
                  dir_name       = 'DoubleMuonLowMass_Run2016C_03Feb2017', 
                  ana_dir        = analysis_dir, 
                  tree_prod_name = tree_prod_name, 
                  is_data        = True),
        SampleCfg(name           = 'data_obs', 
                  dir_name       = 'DoubleMuonLowMass_Run2016D_03Feb2017', 
                  ana_dir        = analysis_dir, 
                  tree_prod_name = tree_prod_name, 
                  is_data        = True),
        SampleCfg(name           = 'data_obs', 
                  dir_name       = 'DoubleMuonLowMass_Run2016E_03Feb2017', 
                  ana_dir        = analysis_dir, 
                  tree_prod_name = tree_prod_name, 
                  is_data        = True),
        SampleCfg(name           = 'data_obs', 
                  dir_name       = 'DoubleMuonLowMass_Run2016F_03Feb2017', 
                  ana_dir        = analysis_dir, 
                  tree_prod_name = tree_prod_name, 
                  is_data        = True),
        SampleCfg(name           = 'data_obs', 
                  dir_name       = 'DoubleMuonLowMass_Run2016G_03Feb2017', 
                  ana_dir        = analysis_dir, 
                  tree_prod_name = tree_prod_name, 
                  is_data        = True),
        SampleCfg(name           = 'data_obs', 
                  dir_name       = 'DoubleMuonLowMass_Run2016Hv2_03Feb2017', 
                  ana_dir        = analysis_dir, 
                  tree_prod_name = tree_prod_name, 
                  is_data        = True),
        SampleCfg(name           = 'data_obs', 
                  dir_name       = 'DoubleMuonLowMass_Run2016Hv3_03Feb2017', 
                  ana_dir        = analysis_dir, 
                  tree_prod_name = tree_prod_name, 
                  is_data        = True),
    ]

    all_samples = samples_mc + samples_data

    sampleDict = {}
    for sample in all_samples:
        sampleDict[sample.name] = sample
        if sample.is_signal:
            sample.scale = sample.scale * signal_scale

    return samples_mc, samples_data, all_samples, sampleDict
