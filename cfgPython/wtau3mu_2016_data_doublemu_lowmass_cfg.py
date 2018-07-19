# heppy_batch.py -o /eos/cms/store/group/phys_tau/WTau3Mu/mvamet2016/prod_v5 wtau3mu_2016_data_doublemu_cfg.py -b 'bsub -u hjkagsdjhga -q 8nh < ./batchScript.sh'
from collections import OrderedDict, Counter

import PhysicsTools.HeppyCore.framework.config as cfg
from PhysicsTools.HeppyCore.framework.config     import printComps
from PhysicsTools.HeppyCore.framework.heppy_loop import getHeppyOption
from PhysicsTools.Heppy.utils.cmsswPreprocessor import CmsswPreprocessor
from CMGTools.RootTools.utils.splitFactor import splitFactor

# import all analysers:
# Heppy analyzers
from PhysicsTools.Heppy.analyzers.core.JSONAnalyzer                 import JSONAnalyzer
from PhysicsTools.Heppy.analyzers.core.SkimAnalyzerCount            import SkimAnalyzerCount
from PhysicsTools.Heppy.analyzers.core.EventSelector                import EventSelector
from PhysicsTools.Heppy.analyzers.objects.VertexAnalyzer            import VertexAnalyzer
from PhysicsTools.Heppy.analyzers.core.PileUpAnalyzer               import PileUpAnalyzer
from PhysicsTools.Heppy.analyzers.gen.GeneratorAnalyzer             import GeneratorAnalyzer
from PhysicsTools.Heppy.analyzers.gen.LHEWeightAnalyzer             import LHEWeightAnalyzer
        
# Tau-tau analysers        
from CMGTools.H2TauTau.proto.analyzers.TriggerAnalyzer              import TriggerAnalyzer
from CMGTools.H2TauTau.proto.analyzers.METFilter                    import METFilter
from CMGTools.H2TauTau.proto.analyzers.FileCleaner                  import FileCleaner
from CMGTools.H2TauTau.proto.analyzers.JetAnalyzer                  import JetAnalyzer

#WTau3Mu analysers
from CMGTools.WTau3Mu.analyzers.Tau3MuAnalyzer                      import Tau3MuAnalyzer
from CMGTools.WTau3Mu.analyzers.WTau3MuTreeProducer                 import WTau3MuTreeProducer
from CMGTools.WTau3Mu.analyzers.Tau3MuKalmanVertexFitterAnalyzer    import Tau3MuKalmanVertexFitterAnalyzer
from CMGTools.WTau3Mu.analyzers.Tau3MuKinematicVertexFitterAnalyzer import Tau3MuKinematicVertexFitterAnalyzer
from CMGTools.WTau3Mu.analyzers.Tau3MuIsolationAnalyzer             import Tau3MuIsolationAnalyzer
from CMGTools.WTau3Mu.analyzers.GenMatcherAnalyzer                  import GenMatcherAnalyzer
from CMGTools.WTau3Mu.analyzers.L1TriggerAnalyzer                   import L1TriggerAnalyzer
from CMGTools.WTau3Mu.analyzers.BDTAnalyzer                         import BDTAnalyzer
from CMGTools.WTau3Mu.analyzers.MVAMuonIDAnalyzer                   import MVAMuonIDAnalyzer
from CMGTools.WTau3Mu.analyzers.RecoilCorrector                     import RecoilCorrector

# import samples
from CMGTools.WTau3Mu.samples.data_2016                             import datasamplesDoubleMuLowMass03Feb2017 as samples

puFileMC   = '$CMSSW_BASE/src/CMGTools/H2TauTau/data/MC_Moriond17_PU25ns_V1.root'
puFileData = '/afs/cern.ch/user/a/anehrkor/public/Data_Pileup_2016_271036-284044_80bins.root'

###################################################
###                   OPTIONS                   ###
###################################################
# Get all heppy options; set via "-o production" or "-o production=True"
# production = True run on batch, production = False (or unset) run locally
production         = getHeppyOption('production'        , True )
pick_events        = getHeppyOption('pick_events'       , False)
kin_vtx_fitter     = getHeppyOption('kin_vtx_fitter'    , True )
extrap_muons_to_L1 = getHeppyOption('extrap_muons_to_L1', False)
compute_mvamet     = getHeppyOption('compute_mvamet'    , True )
###################################################
###               HANDLE SAMPLES                ###
###################################################
for sample in samples:
    # triggers you want in DoubleMuonLowMass
    sample.triggers     = ['HLT_DoubleMu3_Trk_Tau3mu_v%d'                      %i for i in range(1, 12)]

#     # triggers you want in SingleMuon
#     sample.triggers     = ['HLT_IsoMu24_v%d'                                   %i for i in range(1, 12)]
#     sample.triggers    += ['HLT_IsoTkMu24_v%d'                                 %i for i in range(1, 12)]
# 
#     # triggers you want in DoubleMuon
#     sample.triggers     = ['HLT_IsoMu24_v%d'                                   %i for i in range(1, 12)]
#     sample.triggers    += ['HLT_IsoTkMu24_v%d'                                 %i for i in range(1, 12)]
# 
#     # triggers you don't, suppose you run on two different datasets
#     sample.vetoTriggers = ['HLT_DoubleMu3_Trk_Tau3mu_v%d'                      %i for i in range(1, 12)]


#     sample.triggers += ['HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_v%d'           %i for i in range(1, 12)]
#     sample.triggers += ['HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ_v%d'         %i for i in range(1, 12)]
#     sample.triggers += ['HLT_TkMu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ_v%d'       %i for i in range(1, 12)]
#     sample.triggers += ['HLT_DoubleMu4_LowMassNonResonantTrk_Displaced_v%d' %i for i in range(1, 12)]
#     sample.triggers += ['HLT_TripleMu_12_10_5_v%d'                          %i for i in range(1, 12)]


    sample.splitFactor = splitFactor(sample, 5e4)
    sample.json = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/Final/Cert_271036-284044_13TeV_PromptReco_Collisions16_JSON.txt'

selectedComponents = samples

###################################################
###                  ANALYSERS                  ###
###################################################
eventSelector = cfg.Analyzer(
    EventSelector,
    name='EventSelector',
    toSelect=[
        119409188,
        118275827,
    ]
)

lheWeightAna = cfg.Analyzer(
    LHEWeightAnalyzer, name="LHEWeightAnalyzer",
    useLumiInfo=False
)

jsonAna = cfg.Analyzer(
    JSONAnalyzer,
    name='JSONAnalyzer',
)

skimAna = cfg.Analyzer(
    SkimAnalyzerCount,
    name='SkimAnalyzerCount'
)

triggerAna = cfg.Analyzer(
    TriggerAnalyzer,
    name='TriggerAnalyzer',
    addTriggerObjects=True,
    requireTrigger=True,
    usePrescaled=False
)

vertexAna = cfg.Analyzer(
    VertexAnalyzer,
    name='VertexAnalyzer',
    fixedWeight=1,
    keepFailingEvents=True,
    verbose=False
)

pileUpAna = cfg.Analyzer(
    PileUpAnalyzer,
    name='PileUpAnalyzer',
    true=True
)

# for each path specify which filters you want the muons to match to
triggers_and_filters = OrderedDict()
triggers_and_filters['HLT_DoubleMu3_Trk_Tau3mu'                     ] = (['hltTau3muTkVertexFilter'                              , 'hltTau3muTkVertexFilter'                             , 'hltTau3muTkVertexFilter'                             ], Counter({83:2, 91:1}))
# triggers_and_filters['HLT_IsoMu24'                                  ] = (['hltL3crIsoL1sMu22L1f0L2f10QL3f24QL3trkIsoFiltered0p09'                                                                                                                ], Counter({83:1      }))
# triggers_and_filters['HLT_IsoTkMu24'                                ] = (['hltL3fL1sMu22L1f0Tkf24QL3trkIsoFiltered0p09'                                                                                                                          ], Counter({83:1      }))
# triggers_and_filters['HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ'          ] = (['hltDiMuonGlb17Glb8RelTrkIsoFiltered0p4DzFiltered0p2'  , 'hltDiMuonGlb17Glb8RelTrkIsoFiltered0p4DzFiltered0p2'                                                         ], Counter({83:2      }))
# triggers_and_filters['HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ'        ] = (['hltDiMuonGlb17Trk8RelTrkIsoFiltered0p4DzFiltered0p2'  , 'hltDiMuonGlb17Trk8RelTrkIsoFiltered0p4DzFiltered0p2'                                                         ], Counter({83:2      }))
# triggers_and_filters['HLT_TkMu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ'      ] = (['hltDiMuonTrk17Trk8RelTrkIsoFiltered0p4DzFiltered0p2'  , 'hltDiMuonTrk17Trk8RelTrkIsoFiltered0p4DzFiltered0p2'                                                         ], Counter({83:2      }))
# triggers_and_filters['HLT_DoubleMu4_LowMassNonResonantTrk_Displaced'] = (['hltLowMassNonResonantTkVertexFilter'                  , 'hltLowMassNonResonantTkVertexFilter'                 , 'hltLowMassNonResonantTkVertexFilter'                 ], Counter({83:2, 91:1}))
# triggers_and_filters['HLT_TripleMu_12_10_5'                         ] = (['hltL1TripleMu553L2TriMuFiltered3L3TriMuFiltered12105' , 'hltL1TripleMu553L2TriMuFiltered3L3TriMuFiltered12105', 'hltL1TripleMu553L2TriMuFiltered3L3TriMuFiltered12105'], Counter({83:3      }))

tau3MuAna = cfg.Analyzer(
    Tau3MuAnalyzer,
    name='Tau3MuAnalyzer',
#     trigger_match=True,
    trigger_match=triggers_and_filters,
    useMVAmet=True,
    dz_cut=1, # 1 cm
)

treeProducer = cfg.Analyzer(
    WTau3MuTreeProducer,
    name='WTau3MuTreeProducer',
    fillL1=False,
)

metFilter = cfg.Analyzer(
    METFilter,
    name='METFilter',
    processName='RECO',
    triggers=[
        'Flag_HBHENoiseFilter', 
        'Flag_HBHENoiseIsoFilter', 
        'Flag_EcalDeadCellTriggerPrimitiveFilter',
        'Flag_goodVertices',
        'Flag_eeBadScFilter',
        'Flag_globalTightHalo2016Filter'
    ]
)

if kin_vtx_fitter:
    vertexFitter = cfg.Analyzer(
        Tau3MuKinematicVertexFitterAnalyzer,
        name='Tau3MuKinematicVertexFitterAnalyzer',
    )
else:
    vertexFitter = cfg.Analyzer(
        Tau3MuKalmanVertexFitterAnalyzer,
        name='Tau3MuKalmanVertexFitterAnalyzer',
    )
    

isoAna = cfg.Analyzer(
    Tau3MuIsolationAnalyzer,
    name='Tau3MuIsolationAnalyzer',
)

level1Ana = L1TriggerAnalyzer.defaultConfig
level1Ana.process = 'RECO'

bdtAna = cfg.Analyzer(
    BDTAnalyzer,
    name='BDTAnalyzer',
)

muIdAna = cfg.Analyzer(
    MVAMuonIDAnalyzer,
    name='MVAMuonIDAnalyzer',
    xml_pathBB = 'TMVA-muonid-bmm4-B-25.weights.xml',
    xml_pathEC = 'TMVA-muonid-bmm4-E-19.weights.xml',
    useBkgID = False,
    useSigID = True,
    useSideBands = False,
)

recoilAna = cfg.Analyzer(
    RecoilCorrector,
    name='RecoilCorrector',
    pfMetRCFile='CMGTools/WTau3Mu/data/recoilCorrections/TypeI-PFMet_Run2016BtoH.root',
)

# see SM HTT TWiki
# https://twiki.cern.ch/twiki/bin/viewauth/CMS/SMTauTau2016#Jet_Energy_Corrections
jetAna = cfg.Analyzer(
    JetAnalyzer,
    name              = 'JetAnalyzer',
    jetCol            = 'slimmedJets',
    jetPt             = 20.,
    jetEta            = 4.7,
    relaxJetId        = False, # relax = do not apply jet ID
    relaxPuJetId      = True, # relax = do not apply pileup jet ID
    jerCorr           = False,
    puJetIDDisc       = 'pileupJetId:fullDiscriminant',
    recalibrateJets   = True,
    applyL2L3Residual = 'MC',
    mcGT              = '80X_mcRun2_asymptotic_2016_TrancheIV_v8',
    dataGT            = '80X_dataRun2_2016SeptRepro_v7',
    #jesCorr = 1., # Shift jet energy scale in terms of uncertainties (1 = +1 sigma)
)

fileCleaner = cfg.Analyzer(
    FileCleaner,
    name='FileCleaner'
)

###################################################
###                  SEQUENCE                   ###
###################################################
sequence = cfg.Sequence([
#     eventSelector,
    lheWeightAna,
    jsonAna,
    skimAna,
    triggerAna, # First analyser that applies selections
    vertexAna,
    pileUpAna,
    tau3MuAna,
    jetAna,
    vertexFitter,
    muIdAna,
    isoAna,
#     level1Ana,
    bdtAna,
    metFilter,
    treeProducer,
])

###################################################
###            SET BATCH OR LOCAL               ###
###################################################
if not production:
    comp                 = samples[-7]
    selectedComponents   = [comp]
#     selectedComponents   = [samples[-7], samples[-5]]
    comp.splitFactor     = 1
#     comp.fineSplitFactor = 4

#     for comp in selectedComponents:
#         comp.fineSplitFactor = 4
#     comp.files = ['file:/afs/cern.ch/work/m/manzoni/diTau2015/CMSSW_9_2_2_minimal_recipe/src/CMGTools/WTau3Mu/cfgPython/data.root']
    comp.files           = comp.files[:1]
#     comp.files = [
#          'file:/eos/cms/store/group/phys_tau/WTau3Mu/mvamet2016/mvamet_from_cpp_data/DoubleMuonLowMass_Run2016G_23Sep2016/cmsswPreProcessing.root'
#        'root://xrootd.unl.edu//store/data/Run2016B/SingleMuon/MINIAOD/PromptReco-v1/000/272/760/00000/68B88794-7015-E611-8A92-02163E01366C.root'
#        'file:/eos/cms/store/data/Run2016F/DoubleMuonLowMass/MINIAOD/18Apr2017-v1/00000/F0B3AA1B-AA3E-E711-8ED7-008CFA197CD0.root',
#        'file:/eos/cms/store/data/Run2016F/DoubleMuonLowMass/MINIAOD/18Apr2017-v1/00000/08E24010-983E-E711-808A-0CC47A4D764C.root',
#        'file:/eos/cms/store/data/Run2016F/DoubleMuonLowMass/MINIAOD/18Apr2017-v1/00000/E2AEB1A9-A03E-E711-9841-0CC47A745294.root',
#        'file:/eos/cms/store/data/Run2016F/DoubleMuonLowMass/MINIAOD/18Apr2017-v1/00000/9089A434-F43E-E711-9D88-0CC47AA53D68.root',
#         'root://cms-xrd-global.cern.ch//store/data/Run2016E/DoubleMuonLowMass/MINIAOD/23Sep2016-v1/50000/C881EEF5-8590-E611-91F6-0CC47AD98A92.root',
#         'root://cms-xrd-global.cern.ch//store/data/Run2016E/DoubleMuonLowMass/MINIAOD/23Sep2016-v1/50000/C8AC428A-8190-E611-B72D-003048F5B614.root',
#         'root://cms-xrd-global.cern.ch//store/data/Run2016E/DoubleMuonLowMass/MINIAOD/23Sep2016-v1/50000/CE53955B-A393-E611-B340-0242AC130002.root',
#     ]

preprocessor = None

if extrap_muons_to_L1:
    fname = '$CMSSW_BASE/src/CMGTools/WTau3Mu/prod/muon_extrapolator_cfg.py'
    sequence.append(fileCleaner)
    preprocessor = CmsswPreprocessor(fname, addOrigAsSecondary=False)

if compute_mvamet:
    fname = '$CMSSW_BASE/src/CMGTools/WTau3Mu/prod/compute_mva_met_data_cfg.py'
    sequence.append(fileCleaner)
    preprocessor = CmsswPreprocessor(fname, addOrigAsSecondary=False)


# the following is declared in case this cfg is used in input to the
# heppy.py script
from PhysicsTools.HeppyCore.framework.eventsfwlite import Events
config = cfg.Config(
    components   = selectedComponents,
    sequence     = sequence,
    services     = [],
    preprocessor = preprocessor,
    events_class = Events
)

printComps(config.components, True)
