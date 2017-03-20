from CMGTools.H2TauTau.proto.plotter.PlotConfigs import VariableCfg as VCfg

generic_vars = [
#     VCfg(name='tau_mass'            , binning={'nbinsx':50, 'xmin': 1.6  , 'xmax':  2.   }, unit='GeV', xtitle='m_{#mu#mu#mu}'),
#     VCfg(name='tau_pt'              , binning={'nbinsx':50, 'xmin': 0.   , 'xmax': 50.   }, unit='GeV', xtitle='#tau p_{T}'   ),
#     VCfg(name='tau_eta'             , binning={'nbinsx':50, 'xmin':-3.   , 'xmax':  3.   }            , xtitle='#tau |#eta|'  ),
#     VCfg(name='tau_phi'             , binning={'nbinsx':50, 'xmin':-3.14., 'xmax':  3.14.}            , xtitle='#tau #phi'    ),
#  
    VCfg(name='mu1_pt'              , binning={'nbinsx':50, 'xmin': 0.   , 'xmax': 50.   }, unit='GeV', xtitle='#mu_{1} p_{T}'  ),
#     VCfg(name='mu1_eta'             , binning={'nbinsx':50, 'xmin':-3.   , 'xmax':  3.   }            , xtitle='#mu_{1} |#eta|' ),
#     VCfg(name='mu1_phi'             , binning={'nbinsx':50, 'xmin':-3.14., 'xmax':  3.14.}            , xtitle='#mu_{1} #phi'   ),
 
#     VCfg(name='mu2_pt'              , binning={'nbinsx':50, 'xmin': 0.   , 'xmax': 50.   }, unit='GeV', xtitle='#mu_{2} p_{T}'  ),
#     VCfg(name='mu2_eta'             , binning={'nbinsx':50, 'xmin':-3.   , 'xmax':  3.   }            , xtitle='#mu_{2} |#eta|' ),
#     VCfg(name='mu2_phi'             , binning={'nbinsx':50, 'xmin':-3.14., 'xmax':  3.14.}            , xtitle='#mu_{2} #phi'   ),
 
#     VCfg(name='mu3_pt'              , binning={'nbinsx':50, 'xmin': 0.   , 'xmax': 50.   }, unit='GeV', xtitle='#mu_{3} p_{T}'  ),
#     VCfg(name='mu3_eta'             , binning={'nbinsx':50, 'xmin':-3.   , 'xmax':  3.   }            , xtitle='#mu_{3} |#eta|' ),
#     VCfg(name='mu3_phi'             , binning={'nbinsx':50, 'xmin':-3.14., 'xmax':  3.14.}            , xtitle='#mu_{3} #phi'   ),
#  
#     VCfg(name='mu1_refit_pt'        , binning={'nbinsx':50, 'xmin': 0.   , 'xmax': 50.   }, unit='GeV', xtitle='refit #mu_{1} p_{T}'  ),
#     VCfg(name='mu1_refit_eta'       , binning={'nbinsx':50, 'xmin':-3.   , 'xmax':  3.   }            , xtitle='refit #mu_{1} |#eta|' ),
#     VCfg(name='mu1_refit_phi'       , binning={'nbinsx':50, 'xmin':-3.14., 'xmax':  3.14.}            , xtitle='refit #mu_{1} #phi'   ),
 
#     VCfg(name='mu2_refit_pt'        , binning={'nbinsx':50, 'xmin': 0.   , 'xmax': 50.   }, unit='GeV', xtitle='refit #mu_{2} p_{T}'  ),
#     VCfg(name='mu2_refit_eta'       , binning={'nbinsx':50, 'xmin':-3.   , 'xmax':  3.   }            , xtitle='refit #mu_{2} |#eta|' ),
#     VCfg(name='mu2_refit_phi'       , binning={'nbinsx':50, 'xmin':-3.14., 'xmax':  3.14.}            , xtitle='refit #mu_{2} #phi'   ),
 
#     VCfg(name='mu3_refit_pt'        , binning={'nbinsx':50, 'xmin': 0.   , 'xmax': 50.   }, unit='GeV', xtitle='refit #mu_{3} p_{T}'  ),
#     VCfg(name='mu3_refit_eta'       , binning={'nbinsx':50, 'xmin':-3.   , 'xmax':  3.   }            , xtitle='refit #mu_{3} |#eta|' ),
#     VCfg(name='mu3_refit_phi'       , binning={'nbinsx':50, 'xmin':-3.14., 'xmax':  3.14.}            , xtitle='refit #mu_{3} #phi'   ),

#     VCfg(name='met_pt'       , binning={'nbinsx':50, 'xmin': 0.   , 'xmax':100.   }, unit='GeV', xtitle='refit #mu_3 p_{T}'  ),
#     VCfg(name='met_eta'      , binning={'nbinsx':50, 'xmin':-3.   , 'xmax':  3.   }            , xtitle='refit #mu_3 |#eta|' ),
#     VCfg(name='met_phi'      , binning={'nbinsx':50, 'xmin':-3.14., 'xmax':  3.14.}            , xtitle='refit #mu_3 #phi'   ),

]


all_vars = generic_vars 

dict_all_vars = {}
for v in all_vars:
    dict_all_vars[v.name] = v

def getVars(names):
    return [dict_all_vars[n] for n in names]
    
