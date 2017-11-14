import numpy as np
import matplotlib as mpl
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
import pickle

parser = argparse.ArgumentParser()
parser.add_argument('--load', help='load pkl instead of training')

args = parser.parse_args()


features = [
	'cand_refit_tau_dBetaIsoCone0p8strength0p2_rel', 'cand_refit_mttau', 'cand_refit_tau_pt', 'cand_refit_dRtauMET',
	'cand_refit_dRtauMuonMax', 'tau_sv_prob', 'tau_sv_ls', 'tau_sv_cos',
	'mu1_refit_reliso05', 'mu2_refit_reliso05', 'mu3_refit_reliso05', 'met_pt'
]
sig = pandas.DataFrame(
	root_numpy.root2array(
		'/afs/cern.ch/work/m/manzoni/public/perMauro/Prod_v1p1/WToTauTo3Mu/WTau3MuTreeProducer/tree.root', 'tree',
# 		'signal.root', 'tree',
		branches = [
			'cand_refit_tau_mass', 'cand_refit_tau_dBetaIsoCone0p8strength0p2_rel',
			'cand_refit_mttau', 'cand_refit_tau_pt', 'cand_refit_dRtauMET', 
			'cand_refit_dRtauMuonMax', 'tau_sv_prob', 'tau_sv_ls', 'tau_sv_cos',
			'mu1_refit_muonid_soft', 'mu1_refit_muonid_tight', ##'mu1_refit_muonid_loose', 'mu1_refit_muonid_medium', 
			'mu2_refit_muonid_soft', 'mu2_refit_muonid_tight', ##'mu2_refit_muonid_loose', 'mu2_refit_muonid_medium', 
			'mu3_refit_muonid_soft', 'mu3_refit_muonid_tight', ##'mu3_refit_muonid_loose', 'mu3_refit_muonid_medium', 
			'mu1_refit_reliso05', 'mu2_refit_reliso05', 'mu3_refit_reliso05', 'met_pt'
			],
		selection="cand_refit_tau_mass > 1.6 & cand_refit_tau_mass < 2.0 & abs(cand_refit_charge) == 1"
		)
	)
sig['target'] = np.ones(sig.shape[0])

print 'loaded signal'

bkg = pandas.DataFrame(
	root_numpy.root2array(
		['/afs/cern.ch/work/m/manzoni/public/perMauro/Prod_v1p1/DoubleMuonLowMass*/WTau3MuTreeProducer/tree.root'], 'tree',
# 		'DATI.root', 'tree',
		branches = [
			'cand_refit_massMuons', 'cand_refit_tau_dBetaIsoCone0p8strength0p2_rel',
			'cand_refit_mttau', 'cand_refit_sumPtMuons', 'cand_refit_dRtauMET', 
			'cand_refit_dRtauMuonMax', 'tau_sv_prob', 'tau_sv_ls', 'tau_sv_cos',
			'mu1_refit_muonid_soft', 'mu1_refit_muonid_tight', ##'mu1_refit_muonid_loose', 'mu1_refit_muonid_medium', 
			'mu2_refit_muonid_soft', 'mu2_refit_muonid_tight', ##'mu2_refit_muonid_loose', 'mu2_refit_muonid_medium', 
			'mu3_refit_muonid_soft', 'mu3_refit_muonid_tight', ##'mu3_refit_muonid_loose', 'mu3_refit_muonid_medium', 
			'mu1_refit_reliso05', 'mu2_refit_reliso05', 'mu3_refit_reliso05', 'met_pt'
			],
		selection="((cand_refit_massMuons > 1.6 & cand_refit_massMuons < 1.7) | "
		"(cand_refit_massMuons > 1.85 & cand_refit_massMuons < 2.0))  & abs(cand_refit_charge) == 1"
		)
	)
bkg['target'] = np.zeros(bkg.shape[0])

print 'loaded bkg'

mapping = {
	'cand_refit_massMuons' : 'cand_refit_tau_mass',
	'cand_refit_sumPtMuons' : 'cand_refit_tau_pt',
}
for old, new in mapping.iteritems():
	bkg[new] = bkg[old]

@np.vectorize
def muID(soft, tight):
	if tight > 0.5:
		return 2
	elif soft > 0.5:
		return 1
	else:
		return 0

for mu in [1,2,3]:
	name = 'mu%iID' % mu
	features.append(name)
	sig[name] = muID(
		sig['mu%d_refit_muonid_soft' % mu], 
		sig['mu%d_refit_muonid_tight' % mu]
		)
	bkg[name] = muID(
		bkg['mu%d_refit_muonid_soft' % mu], 
		bkg['mu%d_refit_muonid_tight' % mu]
		)

print 'Summary:'
print '# sig:', sig.shape[0]
print '# bkg:', bkg.shape[0]

tpr = ((sig.tau_sv_prob > 0.10) & (sig.cand_refit_tau_dBetaIsoCone0p8strength0p2_rel < 0.2)  & (sig.cand_refit_dRtauMuonMax < 0.2) & (sig.cand_refit_mttau > 40) & (sig.mu1ID == 2) & (sig.mu2ID == 2) & (sig.mu2ID == 2)).sum()
tpr /= float(sig.shape[0])
fpr = ((bkg.tau_sv_prob > 0.10) & (bkg.cand_refit_tau_dBetaIsoCone0p8strength0p2_rel < 0.2)  & (bkg.cand_refit_dRtauMuonMax < 0.2) & (bkg.cand_refit_mttau > 40) & (bkg.mu1ID == 2) & (bkg.mu2ID == 2) & (bkg.mu2ID == 2)).sum()
fpr /= float(bkg.shape[0])
print 'Default selection -- Signal eff.: %.2f%%, Bkg. eff.: %.2f%%' % (tpr*100, fpr*100)

cutbased_file = open('cut_based.pck', 'w+')
pickle.dump((tpr, fpr), cutbased_file)
cutbased_file.close()

data = pandas.concat([sig, bkg])
train, test = train_test_split(data, test_size=0.33, random_state=42)

if args.load:
	clf = joblib.load(args.load)
else:
	clf = GradientBoostingClassifier(
		learning_rate=0.01, n_estimators=1000, subsample=0.8, random_state=13,
		max_features=len(features), verbose=1,
		min_samples_leaf=int(0.01*len(train)),
		max_depth=5
		)
	clf.fit(train[features], train.target)
	joblib.dump(clf, 'classifier.pkl', compress=True)

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
plt.plot([fpr], [tpr], label='cut based', markerfacecolor='red', marker='o', markersize=10)
	
plt.xscale('log')

fpr, tpr, _ = roc_curve(test.target, pred)
plt.plot(fpr, tpr, label='BDT', color='b')

roc_file = open('roc.pck', 'w+')
pickle.dump((tpr, fpr), roc_file)
roc_file.close()

plt.legend(loc='best')
plt.grid()
plt.title('ROC')
plt.savefig('roc.png')
plt.savefig('roc.pdf')
plt.clf()
	
decisions = []
for X,y in ((train[features], train.target), (test[features], test.target)):
    d1 = clf.decision_function(X[y>0.5]).ravel()
    d2 = clf.decision_function(X[y<0.5]).ravel()
    decisions += [d1, d2]

low = min(np.min(d) for d in decisions)
high = max(np.max(d) for d in decisions)
low_high = (low,high)
bins = 50

plt.hist(decisions[0],
         color='r', alpha=0.5, range=low_high, bins=bins,
         histtype='stepfilled', normed=True,
         label='S (train)')
plt.hist(decisions[1],
         color='b', alpha=0.5, range=low_high, bins=bins,
         histtype='stepfilled', normed=True,
         label='B (train)')

hist, bins = np.histogram(decisions[2],
                          bins=bins, range=low_high, normed=True)
scale = len(decisions[2]) / sum(hist)
err = np.sqrt(hist * scale) / scale

width = (bins[1] - bins[0])
center = (bins[:-1] + bins[1:]) / 2
plt.errorbar(center, hist, yerr=err, fmt='o', c='r', label='S (test)')

hist, bins = np.histogram(decisions[3],
                          bins=bins, range=low_high, normed=True)
scale = len(decisions[2]) / sum(hist)
err = np.sqrt(hist * scale) / scale

plt.errorbar(center, hist, yerr=err, fmt='o', c='b', label='B (test)')

plt.xlabel("BDT output")
plt.ylabel("Arbitrary units")
plt.legend(loc='best')
plt.savefig('overtrain.pdf')
plt.clf()

