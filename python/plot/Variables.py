from CMGTools.H2TauTau.proto.plotter.PlotConfigs import VariableCfg as VCfg

generic_vars = [
    VCfg(name='cand_refit_tau_mass'                          , binning={'nbinsx':50, 'xmin': 1.6  , 'xmax':  2.   }, unit='GeV', xtitle='m_{#mu#mu#mu}'),
#     VCfg(name='cand_refit_tau_pt'                            , binning={'nbinsx':50, 'xmin': 0.   , 'xmax': 50.   }, unit='GeV', xtitle='#tau p_{T}'   ),
#     VCfg(name='cand_refit_tau_eta'                           , binning={'nbinsx':50, 'xmin':-3.   , 'xmax':  3.   }            , xtitle='#tau #eta'    ),
#     VCfg(name='cand_refit_tau_phi'                           , binning={'nbinsx':50, 'xmin':-3.14 , 'xmax':  3.14 }            , xtitle='#tau #phi'    ),
                                                  
#     VCfg(name='mu1_refit_pt'                                 , binning={'nbinsx':50, 'xmin': 0.   , 'xmax': 50.   }, unit='GeV', xtitle='refit #mu_{1} p_{T}'  ),
#     VCfg(name='mu1_refit_eta'                                , binning={'nbinsx':50, 'xmin':-3.   , 'xmax':  3.   }            , xtitle='refit #mu_{1} #eta'   ),
#     VCfg(name='mu1_refit_phi'                                , binning={'nbinsx':50, 'xmin':-3.14 , 'xmax':  3.14 }            , xtitle='refit #mu_{1} #phi'   ),
#                           
#     VCfg(name='mu2_refit_pt'                                 , binning={'nbinsx':50, 'xmin': 0.   , 'xmax': 50.   }, unit='GeV', xtitle='refit #mu_{2} p_{T}'  ),
#     VCfg(name='mu2_refit_eta'                                , binning={'nbinsx':50, 'xmin':-3.   , 'xmax':  3.   }            , xtitle='refit #mu_{2} #eta'   ),
#     VCfg(name='mu2_refit_phi'                                , binning={'nbinsx':50, 'xmin':-3.14 , 'xmax':  3.14 }            , xtitle='refit #mu_{2} #phi'   ),
#                           
#     VCfg(name='mu3_refit_pt'                                 , binning={'nbinsx':50, 'xmin': 0.   , 'xmax': 50.   }, unit='GeV', xtitle='refit #mu_{3} p_{T}'  ),
#     VCfg(name='mu3_refit_eta'                                , binning={'nbinsx':50, 'xmin':-3.   , 'xmax':  3.   }            , xtitle='refit #mu_{3} #eta'   ),
#     VCfg(name='mu3_refit_phi'                                , binning={'nbinsx':50, 'xmin':-3.14 , 'xmax':  3.14 }            , xtitle='refit #mu_{3} #phi'   ),
                         
#     VCfg(name='met_pt'                                       , binning={'nbinsx':50, 'xmin': 0.   , 'xmax':100.   }, unit='GeV', xtitle='E_{T}^{miss}'         ),
#     VCfg(name='met_phi'                                      , binning={'nbinsx':50, 'xmin':-3.14 , 'xmax':  3.14 }            , xtitle='E_{T}^{miss} #phi'    ),

#     VCfg(name='tau_sv_prob'                                  , binning={'nbinsx':50, 'xmin': 0.   , 'xmax':  1.   }            , xtitle='secondary vertex prob'    ),
#     VCfg(name='tau_sv_cos'                                   , binning={'nbinsx':50, 'xmin': 0.95 , 'xmax':  1.   }            , xtitle='cosine of pointing angle' ),
#     VCfg(name='tau_sv_ls'                                    , binning={'nbinsx':50, 'xmin': 0.   , 'xmax': 10.   }            , xtitle='displacement L/#sigma'    ),
#     VCfg(name='cand_refit_tau_dBetaIsoCone0p8strength0p2_rel', binning={'nbinsx':50, 'xmin': 0.   , 'xmax':  1.   }            , xtitle='#tau isolation'           ),
#     VCfg(name='cand_refit_dRtauMuonMax'                      , binning={'nbinsx':50, 'xmin': 0.   , 'xmax':  1.   }            , xtitle='max dR(#tau, #mu_{i}'     ),
#     VCfg(name='cand_refit_mttau'                             , binning={'nbinsx':50, 'xmin': 0.   , 'xmax':100.   }            , xtitle='m_{T}(#tau, E_{T}^{miss})'),
#     VCfg(name='cand_refit_tau_pt'                            , binning={'nbinsx':50, 'xmin': 0.   , 'xmax': 80.   }            , xtitle='#tau p_{T}'               ),
#     VCfg(name='mu1_refit_reliso05'                           , binning={'nbinsx':50, 'xmin': 0.   , 'xmax':  1.   }            , xtitle='#mu_{1} isolation'        ),
#     VCfg(name='mu2_refit_reliso05'                           , binning={'nbinsx':50, 'xmin': 0.   , 'xmax':  1.   }            , xtitle='#mu_{2} isolation'        ),
#     VCfg(name='mu3_refit_reliso05'                           , binning={'nbinsx':50, 'xmin': 0.   , 'xmax':  1.   }            , xtitle='#mu_{3} isolation'        ),
]


all_vars = generic_vars 

dict_all_vars = {}
for v in all_vars:
    dict_all_vars[v.name] = v

def getVars(names):
    return [dict_all_vars[n] for n in names]
    
