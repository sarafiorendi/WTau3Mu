import numpy as np
import matplotlib as mpl
from scipy.stats import ks_2samp
mpl.use('Agg')
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve
from sklearn.model_selection import train_test_split
import pandas, root_numpy
from sklearn.ensemble import GradientBoostingClassifier
import sklearn
from pdb import set_trace
from sklearn.externals import joblib
import argparse
from xgboost import XGBClassifier, plot_importance

tag = '16oct2017_v4'

parser = argparse.ArgumentParser()
parser.add_argument('--load', help='load pkl instead of training')

args = parser.parse_args()

features = [
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

#     'abs(mu1_refit_dxy-mu2_refit_dxy)',
#     'abs(mu1_refit_dxy-mu3_refit_dxy)',
#     'abs(mu2_refit_dxy-mu3_refit_dxy)',

    'abs(mu1_refit_dz-mu2_refit_dz)',
    'abs(mu1_refit_dz-mu3_refit_dz)',
    'abs(mu2_refit_dz-mu3_refit_dz)',

    'tau_sv_ls',
    'tau_sv_prob',
    'tau_sv_cos',

    'HTjets',
    'HTbjets',
]

branches = features + [
    'cand_refit_charge',
    'cand_refit_tau_mass',
    'cand_refit_dRtauMuonMax',
    'mu1_refit_muonid_soft', 'mu1_refit_muonid_loose', 'mu1_refit_muonid_medium', 'mu1_refit_muonid_tight', 'mu1_refit_muonid_tightnovtx', 
    'mu2_refit_muonid_soft', 'mu2_refit_muonid_loose', 'mu2_refit_muonid_medium', 'mu2_refit_muonid_tight', 'mu2_refit_muonid_tightnovtx', 
    'mu3_refit_muonid_soft', 'mu3_refit_muonid_loose', 'mu3_refit_muonid_medium', 'mu3_refit_muonid_tight', 'mu3_refit_muonid_tightnovtx', 
]

sig_selection = '(cand_refit_tau_mass > 1.6 & cand_refit_tau_mass < 2.0 & abs(cand_refit_charge) == 1 & cand_refit_gen_pt>0)'
# bkg_selection = '( ((cand_refit_tau_mass > 1.6 & cand_refit_tau_mass < 1.75) | (cand_refit_tau_mass > 1.82 & cand_refit_tau_mass < 2.0)) & abs(cand_refit_charge)==1 ) | '\
#                 '(   cand_refit_tau_mass > 1.6                                                             & cand_refit_tau_mass < 2.0   & abs(cand_refit_charge)==3)'
bkg_selection = '( ((cand_refit_tau_mass > 1.6 & cand_refit_tau_mass < 1.72) | (cand_refit_tau_mass > 1.84 & cand_refit_tau_mass < 2.0)) & abs(cand_refit_charge)==1 )'\

sig = pandas.DataFrame(
    root_numpy.root2array(
        'signal2016v4.root',
        'tree',
        branches  = branches + ['puweight'],
        selection = sig_selection,
    )
)

sig['normfactor'] = sig.puweight

bkg = pandas.DataFrame(
    root_numpy.root2array(
        'data2016v4.root',
        'tree',
        branches  = branches,
        selection = bkg_selection
    )
)

bkg['normfactor'] = 1.

sig['target'] = np.ones (sig.shape[0]).astype(np.int)
bkg['target'] = np.zeros(bkg.shape[0]).astype(np.int)

data = pandas.concat([sig, bkg])
train, test = train_test_split(data, test_size=0.12, random_state=42)

if args.load:
    clf = joblib.load(args.load)
else:
    clf = XGBClassifier(#silent = False)
        max_depth        = 6,
        learning_rate    = 0.01,
        n_estimators     = 10000,
        silent           = False,
        subsample        = 0.7,
        colsample_bytree = 0.7,
        nthread          = -1,
        min_child_weight = 4.,
        gamma            = 0.8,
        seed             = 1986,
    )
    clf.fit(
        train[features], 
        train.target,
        eval_set              = [(train[features], train.target), (test[features], test.target)],
        early_stopping_rounds = 30,
        eval_metric           = 'auc',
        verbose               = True,
        sample_weight         = train['normfactor'],
    )
        
    joblib.dump(clf, 'classifier_%s.pkl' %tag, compress=True)


print 'Summary:'
print '# sig:', sig.shape[0]
print '# bkg:', bkg.shape[0]

tpr = ((sig.tau_sv_prob > 0.10) & (sig.cand_refit_tau_dBetaIsoCone0p8strength0p2_rel < 0.2)  & (sig.cand_refit_dRtauMuonMax < 0.2) & (sig.cand_refit_mttau > 40) & (sig.mu1_refit_muonid_medium == 1) & (sig.mu2_refit_muonid_medium == 1) & (sig.mu3_refit_muonid_medium == 1)).sum()
tpr /= float(sig.shape[0])
fpr = ((bkg.tau_sv_prob > 0.10) & (bkg.cand_refit_tau_dBetaIsoCone0p8strength0p2_rel < 0.2)  & (bkg.cand_refit_dRtauMuonMax < 0.2) & (bkg.cand_refit_mttau > 40) & (bkg.mu1_refit_muonid_medium == 1) & (bkg.mu2_refit_muonid_medium == 1) & (bkg.mu3_refit_muonid_medium == 1)).sum()
fpr /= float(bkg.shape[0])
print 'Default selection -- Signal eff.: %.2f%%, Bkg. eff.: %.2f%%' % (tpr*100, fpr*100)



pred = clf.predict_proba(test[features])[:, 1]

from scipy.stats import pearsonr
pearson_coeff, p_value = pearsonr(test.cand_refit_tau_mass, pred)
print 'Pearson correlation coefficient:', pearson_coeff, " 2 tailed p-value: ", p_value

#rescale to better compute the pearson coefficient
mass = test.cand_refit_tau_mass.copy()
mass = (mass - mass.mean())/mass.std()
bdt = pred.copy()
bdt = (bdt - bdt.mean())/bdt.std()
pearson_coeff, p_value = pearsonr(mass, bdt)
print 'Pearson correlation coefficient on scaled data:', pearson_coeff, " 2 tailed p-value: ", p_value


import itertools
xy = [i*j for i,j in itertools.product([10.**i for i in range(-8, 0)], [1,2,4,8])]+[1]
plt.plot(xy, xy, color='grey', linestyle='--')
plt.xlim([10**-5, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
    
#draw baseline point
plt.plot([fpr], [tpr], label='baseline', markerfacecolor='red', marker='o', markersize=10)
    
plt.xscale('log')

fpr, tpr, _ = roc_curve(test.target, pred)
plt.plot(fpr, tpr, label='BDT', color='b')

plt.legend(loc='best')
plt.grid()
plt.title('ROC')
plt.savefig('roc_%s.pdf' % tag)
plt.clf()
    

train_sig = clf.predict_proba(train[features][train.target>0.5])[:,1]
train_bkg = clf.predict_proba(train[features][train.target<0.5])[:,1]

test_sig = clf.predict_proba(test[features][test.target>0.5])[:,1]
test_bkg = clf.predict_proba(test[features][test.target<0.5])[:,1]

low  = 0
high = 1
low_high = (low,high)
bins = 50

#################################################
plt.hist(
    train_sig,
    color='r', 
    alpha=0.5, 
    range=low_high, 
    bins=bins,
    histtype='stepfilled', 
    normed=True,
    log=True,
    label='S (train)'
)

#################################################
plt.hist(
    train_bkg,
    color='b', 
    alpha=0.5, 
    range=low_high, 
    bins=bins,
    histtype='stepfilled', 
    normed=True,
    log=True,
    label='B (train)'
)

#################################################
hist, bins = np.histogram(
    test_sig,
    bins=bins, 
    range=low_high, 
    normed=True
)

width  = (bins[1] - bins[0])
center = (bins[:-1] + bins[1:]) / 2
scale  = len(test_sig) / sum(hist)
err    = np.sqrt(hist * scale) / scale

plt.errorbar(
    center, 
    hist, 
    yerr=err, 
    fmt='o', 
    c='r', 
    label='S (test)'
)

#################################################
hist, bins = np.histogram(
    test_bkg,
    bins=bins, 
    range=low_high, 
    normed=True
)

width  = (bins[1] - bins[0])
center = (bins[:-1] + bins[1:]) / 2
scale  = len(test_bkg) / sum(hist)
err    = np.sqrt(hist * scale) / scale

plt.errorbar(
    center, 
    hist, 
    yerr=err, 
    fmt='o', 
    c='b', 
    label='B (test)'
)

#################################################
plt.xlabel('BDT output')
plt.ylabel('Arbitrary units')
plt.legend(loc='best')
ks_sig = ks_2samp(train_sig, test_sig)
ks_bkg = ks_2samp(train_bkg, test_bkg)
plt.suptitle('KS p-value: sig = %.3f%s - bkg = %.2f%s' %(ks_sig.pvalue * 100., '%', ks_bkg.pvalue * 100., '%'))
plt.savefig('overtrain_%s.pdf' %tag)


# importance = clf.get_fscore()

plot_importance(clf)
plt.tight_layout()
plt.savefig('feat_importance_%s.pdf' %tag)

