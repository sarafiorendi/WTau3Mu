import ROOT
import numpy as np
import xgboost as xgb
import pandas, root_numpy
from sklearn.externals import joblib
from sklearn import preprocessing
import matplotlib.pyplot as plt 

# tag = '13oct2017'
tag = '16oct2017_v4'

ifile = 'data2016v4.root'

file = ROOT.TFile.Open(ifile, 'read')
file.cd()
tree = file.Get('tree')

# classifier = joblib.load('classifier_new.pkl')
classifier = joblib.load('classifier_%s.pkl' %tag)


# earlier in October
# feat_names =[
#     'cand_refit_mttau', 
#     'cand_refit_mass12', 
#     'cand_refit_mass13', 
#     'cand_refit_mass23', 
#     'cand_refit_tau_pt', 
#     'cand_refit_tau_eta', 
#     'cand_refit_dRtauMET', 
#     'cand_refit_dPhitauMET', 
#     'cand_refit_dRtauMuonMax', 
#     'cand_refit_tau_dBetaIsoCone0p8strength0p2_rel',
#     'tau_sv_prob', 
#     'tau_sv_ls', 
#     'tau_sv_cos',
#     'mu1_refit_reliso05', 
#     'mu2_refit_reliso05', 
#     'mu3_refit_reliso05', 
#     'mu1_refit_muonid_BDT',
#     'mu2_refit_muonid_BDT',
#     'mu3_refit_muonid_BDT',
#     'n_taus',
#     'n_muons',
#     'n_electrons',
#     'mu1_jet_pt', 
#     'mu2_jet_pt', 
#     'mu3_jet_pt', 
#     'mu1_jet_eta', 
#     'mu2_jet_eta', 
#     'mu3_jet_eta', 
#     'mu1_jet_mass', 
#     'mu2_jet_mass', 
#     'mu3_jet_mass', 
#     'mu1_jet_charge', 
#     'mu2_jet_charge', 
#     'mu3_jet_charge', 
#     'mu1_refit_pt', 
#     'mu2_refit_pt', 
#     'mu3_refit_pt', 
#     'cand_refit_met_pt',
#     'abs(cand_refit_me_eta_1)+abs(cand_refit_me_eta_2)',
#     'cand_refit_me_eta_1',
#     'cand_refit_me_eta_2',
#     'cand_refit_mez_1',
#     'cand_refit_mez_2',
#     'cand_refit_w_isgood',
#     'cand_refit_w_pt',
#     'HTjets',
#     'HTbjets',
#     'njets',
#     'nbjets',
#     'cand_refit_charge12',
#     'cand_refit_charge13',
#     'cand_refit_charge23',
# ]

# 16oct2017
# feat_names = [
#     'cand_refit_mttau',
#     'cand_refit_tau_pt',
#     'cand_refit_tau_eta',
#     'cand_refit_dRtauMET',
#     'abs(cand_refit_dPhitauMET)',
#     'cand_refit_dRtauMuonMax',
#     'cand_refit_tau_dBetaIsoCone0p8strength0p2_rel',
#     'tau_sv_prob',
#     'tau_sv_ls',
#     'tau_sv_cos',
#     'mu1_refit_reliso05',
#     'mu2_refit_reliso05',
#     'mu3_refit_reliso05',
#     'mu1_refit_muonid_BDT',
#     'mu2_refit_muonid_BDT',
#     'mu3_refit_muonid_BDT',
#     'abs(mu1_refit_dz)',
#     'abs(mu1_refit_dxy)',
#     'abs(mu2_refit_dz)',
#     'abs(mu2_refit_dxy)',
#     'abs(mu3_refit_dz)',
#     'abs(mu3_refit_dxy)',
#     'abs(mu1_refit_dz-mu2_refit_dz)',
#     'abs(mu1_refit_dz-mu3_refit_dz)',
#     'abs(mu2_refit_dz-mu3_refit_dz)',
#     'abs(mu1_refit_dxy-mu2_refit_dxy)',
#     'abs(mu1_refit_dxy-mu3_refit_dxy)',
#     'abs(mu2_refit_dxy-mu3_refit_dxy)',
#     'mu1_refit_pt/cand_refit_tau_pt',
#     'mu2_refit_pt/cand_refit_tau_pt',
#     'mu3_refit_pt/cand_refit_tau_pt',
#     'mu2_refit_pt/mu1_refit_pt',
#     'mu3_refit_pt/mu1_refit_pt',
#     'n_taus',
#     'n_candidates',
#     'mu1_jet_pt==mu2_jet_pt',
#     'mu1_jet_pt==mu3_jet_pt',
#     'mu1_jet_pt',
#     'mu1_jet_eta',
#     'mu1_jet_mass',
#     'mu1_refit_pt',
#     'mu2_refit_pt',
#     'mu3_refit_pt',
#     'cand_refit_met_pt',
#     'abs(cand_refit_me_eta_2 + cand_refit_me_eta_1)',
#     'abs(cand_refit_me_eta_2 - cand_refit_me_eta_1)',
#     'abs((cand_refit_mez_2 - cand_refit_mez_1))',
#     'abs((cand_refit_mez_2 + cand_refit_mez_1))',
#     'cand_refit_w_pt',
#     'HTjets',
#     'HTbjets',
#     'njets',
#     'nbjets',
# ]

# 16oct2017_v3
feat_names = [
    'cand_refit_tau_pt',
    'cand_refit_tau_eta',
    'cand_refit_mttau',
    'cand_refit_tau_dBetaIsoCone0p8strength0p2_rel',
    'abs(cand_refit_dPhitauMET)',
    'cand_refit_met_pt',
#     'cand_refit_dRtauMuonMax',
    'cand_refit_w_pt',
    'abs(cand_refit_mez_2-cand_refit_mez_1)',

    'mu1_refit_reliso05',
    'mu2_refit_reliso05',
    'mu3_refit_reliso05',

#     'mu1_refit_pt',
#     'mu2_refit_pt',
#     'mu3_refit_pt',

    'mu1_refit_muonid_BDT',
    'mu2_refit_muonid_BDT',
    'mu3_refit_muonid_BDT',

    'abs(mu1_refit_dz)',
    'abs(mu2_refit_dz)',
    'abs(mu3_refit_dz)',

#     'abs(mu1_refit_dxy)',
#     'abs(mu2_refit_dxy)',
#     'abs(mu3_refit_dxy)',

    'abs(mu1_refit_dz-mu2_refit_dz)',
    'abs(mu1_refit_dz-mu3_refit_dz)',
    'abs(mu2_refit_dz-mu3_refit_dz)',

#     'abs(mu1_refit_dxy-mu2_refit_dxy)',
#     'abs(mu1_refit_dxy-mu3_refit_dxy)',
#     'abs(mu2_refit_dxy-mu3_refit_dxy)',

    'tau_sv_ls',
    'tau_sv_prob',
    'tau_sv_cos',

    'HTjets',
    'HTbjets',
]

print 'loading support dataset...'
dataset_support = pandas.DataFrame(
    root_numpy.root2array(
        ifile,
        'tree',
        branches=feat_names,
    )
)
print '\t...done'

print 'loading dataset...'
dataset = pandas.DataFrame(
    root_numpy.root2array(
        ifile,
        'tree',
    )
)
print '\t...done'

print 'computing probabilities...'
bdt_proba_v2_array = classifier.predict_proba(dataset_support)[:,1]
print '\t...done'


print 'adding new column to the dataset...'
dataset['bdt_proba_v2'] = bdt_proba_v2_array
print '\t...done'

print 'writing out the enriched tree...'
# you'll love it https://github.com/scikit-hep/root_pandas
import root_pandas
dataset.to_root('data2016v4_enriched_%s.root' %tag, key='tree', store_index=False)
print '\t...done'

