from __future__ import division  # (for python 2/3 support)

'''
Weighed 2-sided KS test!
https://stackoverflow.com/questions/40044375/how-to-calculate-the-kolmogorov-smirnov-statistic-between-two-weighted-samples
'''

import ROOT
import numpy as np
import pandas 
import root_numpy
import root_pandas
from scipy.stats import ks_2samp
import matplotlib.pyplot as plt
# from skgof import ks_test, cvm_test, ad_test


def ks_w2(data1, data2, wei1, wei2):
    ix1 = np.argsort(data1)
    ix2 = np.argsort(data2)
    data1 = data1[ix1]
    data2 = data2[ix2]
    wei1 = wei1[ix1]
    wei2 = wei2[ix2]
    data = np.concatenate([data1, data2])
    cwei1 = np.hstack([0, np.cumsum(wei1)/sum(wei1)])
    cwei2 = np.hstack([0, np.cumsum(wei2)/sum(wei2)])
    cdf1we = cwei1[[np.searchsorted(data1, data, side='right')]]
    cdf2we = cwei2[[np.searchsorted(data2, data, side='right')]]
    return np.max(np.abs(cdf1we - cdf2we))

print 'importing dataset...'
data = root_pandas.read_root('data2016v4_enriched_16oct2017_v4.root')
# data = root_pandas.read_root('signal2016v4_enriched_16oct2017_v4.root')
print '...done'

# slices = np.arange(0,1.05,0.05)
slices = np.array([0., 0.01, 0.03, 0.06, 0.1, 0.2, 0.4, 0.7, 1.])
bins   = np.arange(1.6,2,0.01)

skimmed = data[np.array(data.cand_refit_tau_mass>1.6) * np.array(data.cand_refit_tau_mass<2.0) ]

totalmass = np.array(skimmed.cand_refit_tau_mass)
totalmass_w = np.ones_like(totalmass) * 1./len(totalmass)

plt.hist(totalmass, bins)
plt.savefig('mass_hist_bdt_inclusive.pdf')
plt.close()

for i, _ in enumerate(slices[:-1]):
    min = slices[i]
    max = slices[i+1]
    mass = np.array(skimmed.cand_refit_tau_mass)[np.array(skimmed.bdt_proba_v2>min) * np.array(skimmed.bdt_proba_v2<max)]
        
    #import pdb ; pdb.set_trace()
    plt.hist(mass, bins)
    plt.savefig('mass_hist_bdt_%s_%s.pdf' %(str(min).replace('.', 'p')[:4], str(max).replace('.', 'p')[:4]))
    plt.close()
    #print 'slice bdt: %.2f - %.2f' %(min, max),'\tKS p-value: ', ks_2samp(bdt, totalbdt).pvalue
    
    mass_w = np.ones_like(mass) * 1./len(mass)
    prob = ks_w2(mass, totalmass, mass_w, totalmass_w)
    print 'slice bdt: %.2f - %.2f' %(min, max),'\t\tKS p-value on the 3mu mass: %.2f%s' %(100.*prob, '%')



'''
# signal MC
slice bdt: 0.00 - 0.05 		KS p-value on the 3mu mass: 7.75%
slice bdt: 0.05 - 0.10 		KS p-value on the 3mu mass: 10.33%
slice bdt: 0.10 - 0.15 		KS p-value on the 3mu mass: 7.50%
slice bdt: 0.15 - 0.20 		KS p-value on the 3mu mass: 11.91%
slice bdt: 0.20 - 0.25 		KS p-value on the 3mu mass: 15.15%
slice bdt: 0.25 - 0.30 		KS p-value on the 3mu mass: 11.13%
slice bdt: 0.30 - 0.35 		KS p-value on the 3mu mass: 12.84%
slice bdt: 0.35 - 0.40 		KS p-value on the 3mu mass: 7.36%
slice bdt: 0.40 - 0.45 		KS p-value on the 3mu mass: 11.41%
slice bdt: 0.45 - 0.50 		KS p-value on the 3mu mass: 12.05%
slice bdt: 0.50 - 0.55 		KS p-value on the 3mu mass: 9.68%
slice bdt: 0.55 - 0.60 		KS p-value on the 3mu mass: 12.81%
slice bdt: 0.60 - 0.65 		KS p-value on the 3mu mass: 8.60%
slice bdt: 0.65 - 0.70 		KS p-value on the 3mu mass: 10.33%
slice bdt: 0.70 - 0.75 		KS p-value on the 3mu mass: 8.55%
slice bdt: 0.75 - 0.80 		KS p-value on the 3mu mass: 13.52%
slice bdt: 0.80 - 0.85 		KS p-value on the 3mu mass: 5.09%
slice bdt: 0.85 - 0.90 		KS p-value on the 3mu mass: 3.23%
slice bdt: 0.90 - 0.95 		KS p-value on the 3mu mass: 2.51%
slice bdt: 0.95 - 1.00 		KS p-value on the 3mu mass: 4.98%
'''

'''
# data
slice bdt: 0.00 - 0.05 		KS p-value on the 3mu mass: 0.01%
slice bdt: 0.05 - 0.10 		KS p-value on the 3mu mass: 1.37%
slice bdt: 0.10 - 0.15 		KS p-value on the 3mu mass: 2.01%
slice bdt: 0.15 - 0.20 		KS p-value on the 3mu mass: 4.72%
slice bdt: 0.20 - 0.25 		KS p-value on the 3mu mass: 5.27%
slice bdt: 0.25 - 0.30 		KS p-value on the 3mu mass: 5.99%
slice bdt: 0.30 - 0.35 		KS p-value on the 3mu mass: 5.30%
slice bdt: 0.35 - 0.40 		KS p-value on the 3mu mass: 11.78%
slice bdt: 0.40 - 0.45 		KS p-value on the 3mu mass: 12.82%
slice bdt: 0.45 - 0.50 		KS p-value on the 3mu mass: 20.03%
slice bdt: 0.50 - 0.55 		KS p-value on the 3mu mass: 6.41%
slice bdt: 0.55 - 0.60 		KS p-value on the 3mu mass: 13.24%
slice bdt: 0.60 - 0.65 		KS p-value on the 3mu mass: 15.07%
slice bdt: 0.65 - 0.70 		KS p-value on the 3mu mass: 14.76%
slice bdt: 0.70 - 0.75 		KS p-value on the 3mu mass: 14.83%
slice bdt: 0.75 - 0.80 		KS p-value on the 3mu mass: 22.17%
slice bdt: 0.80 - 0.85 		KS p-value on the 3mu mass: 19.76%
slice bdt: 0.85 - 0.90 		KS p-value on the 3mu mass: 30.57%
slice bdt: 0.90 - 0.95 		KS p-value on the 3mu mass: 30.96%
slice bdt: 0.95 - 1.00 		KS p-value on the 3mu mass: 28.62%

slice bdt: 0.00 - 0.01 		KS p-value on the 3mu mass: 100.00%
slice bdt: 0.01 - 0.03 		KS p-value on the 3mu mass: 0.02%
slice bdt: 0.03 - 0.06 		KS p-value on the 3mu mass: 2.09%
slice bdt: 0.06 - 0.10 		KS p-value on the 3mu mass: 2.44%
slice bdt: 0.10 - 0.20 		KS p-value on the 3mu mass: 1.75%
slice bdt: 0.20 - 0.40 		KS p-value on the 3mu mass: 5.99%
slice bdt: 0.40 - 0.70 		KS p-value on the 3mu mass: 10.47%
slice bdt: 0.70 - 1.00 		KS p-value on the 3mu mass: 20.14%
'''



# class mypdf():
#     def __init__ (self, distribution, weights = None):
#         self.distro  = distribution
#         if weights:
#             self.weights = weights 
#         else:
#             self.weights = np.ones(self.distro.shape[0])
#         
#     def cdf(self, x, *args, **kwds):
#         selection = map(lambda i: i<=x, self.distro)
#         entries = map(lambda i : 1., self.distro)
#         weights = self.weights * selection * entries
#         return np.dot(entries, weights)


# mybdt = mypdf(bdt)
# mybdt.cdf(0.)
# mybdt.cdf(1.)
# mybdt.cdf(0.5)
# cvm_test(bdt, mybdt)




