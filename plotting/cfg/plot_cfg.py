from collections import namedtuple
from operator    import itemgetter

from CMGTools.H2TauTau.proto.plotter.PlotConfigs import HistogramCfg
from CMGTools.H2TauTau.proto.plotter.HistCreator import createHistograms
from CMGTools.H2TauTau.proto.plotter.HistDrawer  import HistDrawer
from CMGTools.H2TauTau.proto.plotter.Variables   import getVars
from CMGTools.H2TauTau.proto.plotter.cut         import Cut

from CMGTools.WTau3Mu.plot.Samples      import createSampleLists
from CMGTools.WTau3Mu.plot.Variables    import generic_vars
from CMGTools.WTau3Mu.plot.WTau3MuStyle import histPref

int_lumi     = 35800.
analysis_dir = '/afs/cern.ch/work/m/manzoni/public/perMauro/Prod_v1p1'
verbose      = True
total_weight = '1.'
make_plots   = True

# Infer whether this is mssm
samples_mc, samples_data, all_samples, sampleDict = createSampleLists(
    analysis_dir = analysis_dir, 
    signal_scale = 1.)

# trick to be able to draw the stack at least
samples_mc[0].is_signal = False

myCut = namedtuple('myCut', ['name', 'cut'])
cuts = []

# categories, do not include charge and iso cuts
# cuts.append(myCut('baseline', 'cand_refit_tau_mass > 1.6 & cand_refit_tau_mass < 2.0 & abs(cand_refit_charge) == 1'))
cuts.append(myCut('baseline', 'abs(cand_refit_charge) == 1'))
cuts.append(myCut('tight'   , 'tau_sv_prob > 0.10 & cand_refit_tau_dBetaIsoCone0p8strength0p2_rel < 0.2 & cand_refit_dRtauMuonMax < 0.2 & cand_refit_mttau > 40'))
cuts.append(myCut('final'   , 'tau_sv_prob > 0.10 & cand_refit_tau_dBetaIsoCone0p8strength0p2_rel < 0.2 & cand_refit_dRtauMuonMax < 0.2 & cand_refit_mttau > 40 & mu1_muonid_tight & mu2_muonid_tight & mu3_muonid_tight'))

variables = generic_vars
sample_names = set()

for cut in cuts:
    cfg_total = HistogramCfg(
        name   = cut.name, 
        vars   = variables, 
        cfgs   = all_samples, 
        cut    = str(cut.cut), 
        lumi   = int_lumi, 
        weight = total_weight
    )

    plots = createHistograms(
        cfg_total, 
        verbose=True, 
    )

    for variable in variables:
        if variable == 'cand_refit_tau_mass' or variable == 'cand_refit_massMuons':
             blindxmin = 1.777-0.040
             blindxmax = 1.777+0.040
        else:
             blindxmin = 999.
             blindxmax = -999.
        plot = plots[variable.name]
        # override HTT default style
        plot.histPref = histPref
        plot._ApplyPrefs()
        HistDrawer.draw(plot, channel='', plot_dir='plot_%s' % cut.name, blindxmin=blindxmin, blindxmax=blindxmax)
