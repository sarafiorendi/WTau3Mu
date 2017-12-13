import os
# import dill # needed in order to serialise lambda functions, need to be installed by the user. See http://stackoverflow.com/questions/25348532/can-python-pickle-lambda-functions
from collections import OrderedDict

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
from CMGTools.WTau3Mu.analyzers.MuonWeighterAnalyzer                import MuonWeighterAnalyzer
from CMGTools.WTau3Mu.analyzers.RecoilCorrector                     import RecoilCorrector
from CMGTools.WTau3Mu.analyzers.MuonWeighterAnalyzer                import MuonWeighterAnalyzer

# import samples, signal
from CMGTools.WTau3Mu.samples.mc_2016 import WToTauTo3Mu

puFileMC   = '$CMSSW_BASE/src/CMGTools/H2TauTau/data/MC_Moriond17_PU25ns_V1.root'
puFileData = '/afs/cern.ch/user/a/anehrkor/public/Data_Pileup_2016_271036-284044_80bins.root'

###################################################
###                   OPTIONS                   ###
###################################################
# Get all heppy options; set via "-o production" or "-o production=True"
# production = True run on batch, production = False (or unset) run locally
production         = getHeppyOption('production'        , False)
pick_events        = getHeppyOption('pick_events'       , False)
kin_vtx_fitter     = getHeppyOption('kin_vtx_fitter'    , True )
extrap_muons_to_L1 = getHeppyOption('extrap_muons_to_L1', False)
compute_mvamet     = getHeppyOption('compute_mvamet'    , False)
###################################################
###               HANDLE SAMPLES                ###
###################################################
samples = [WToTauTo3Mu]

for sample in samples:
    sample.triggers  = ['HLT_DoubleMu3_Trk_Tau3mu_v%d'                      %i for i in range(4, 5)]
    sample.triggers += ['HLT_IsoMu24_v%d'                                   %i for i in range(4, 5)]
    sample.triggers += ['HLT_IsoTkMu24_v%d'                                 %i for i in range(4, 5)]
    sample.triggers += ['HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_v%d'           %i for i in range(7, 8)]
    sample.triggers += ['HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ_v%d'         %i for i in range(6, 7)]
    sample.triggers += ['HLT_TkMu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ_v%d'       %i for i in range(3, 4)]
    sample.triggers += ['HLT_DoubleMu4_LowMassNonResonantTrk_Displaced_v%d' %i for i in range(7, 8)]
    sample.triggers += ['HLT_TripleMu_12_10_5_v%d'                          %i for i in range(4, 5)]

    sample.splitFactor = splitFactor(sample, 1e5)
    sample.puFileData = puFileData
    sample.puFileMC   = puFileMC

selectedComponents = samples

###################################################
###                  ANALYSERS                  ###
###################################################
eventSelector = cfg.Analyzer(
    EventSelector,
    name='EventSelector',
    toSelect=[]
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

genAna = GeneratorAnalyzer.defaultConfig
genAna.allGenTaus = True # save in event.gentaus *ALL* taus, regardless whether hadronic / leptonic decay

# for each path specify which filters you want the muons to match to
triggers_and_filters = OrderedDict()
triggers_and_filters['HLT_DoubleMu3_Trk_Tau3mu'                     ] = ['hltTau3muTkVertexFilter'                              , 'hltTau3muTkVertexFilter'                             , 'hltTau3muTkVertexFilter'                             ]
triggers_and_filters['HLT_IsoMu24'                                  ] = ['hltL3crIsoL1sMu22L1f0L2f10QL3f24QL3trkIsoFiltered0p09'                                                                                                                ]
triggers_and_filters['HLT_IsoTkMu24'                                ] = ['hltL3fL1sMu22L1f0Tkf24QL3trkIsoFiltered0p09'                                                                                                                          ]
triggers_and_filters['HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ'          ] = ['hltDiMuonGlb17Glb8RelTrkIsoFiltered0p4DzFiltered0p2'  , 'hltDiMuonGlb17Glb8RelTrkIsoFiltered0p4DzFiltered0p2'                                                         ]
triggers_and_filters['HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ'        ] = ['hltDiMuonGlb17Trk8RelTrkIsoFiltered0p4DzFiltered0p2'  , 'hltDiMuonGlb17Trk8RelTrkIsoFiltered0p4DzFiltered0p2'                                                         ]
triggers_and_filters['HLT_TkMu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ'      ] = ['hltDiMuonTrk17Trk8RelTrkIsoFiltered0p4DzFiltered0p2'  , 'hltDiMuonTrk17Trk8RelTrkIsoFiltered0p4DzFiltered0p2'                                                         ]
triggers_and_filters['HLT_DoubleMu4_LowMassNonResonantTrk_Displaced'] = ['hltLowMassNonResonantTkVertexFilter'                  , 'hltLowMassNonResonantTkVertexFilter'                 , 'hltLowMassNonResonantTkVertexFilter'                 ]
triggers_and_filters['HLT_TripleMu_12_10_5'                         ] = ['hltL1TripleMu553L2TriMuFiltered3L3TriMuFiltered12105' , 'hltL1TripleMu553L2TriMuFiltered3L3TriMuFiltered12105', 'hltL1TripleMu553L2TriMuFiltered3L3TriMuFiltered12105']

tau3MuAna = cfg.Analyzer(
    Tau3MuAnalyzer,
    name='Tau3MuAnalyzer',
#     trigger_match=True,
    trigger_match=triggers_and_filters,
    useMVAmet=True,
)

treeProducer = cfg.Analyzer(
    WTau3MuTreeProducer,
    name='WTau3MuTreeProducer',
    fillL1=False,
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

genMatchAna = cfg.Analyzer(
    GenMatcherAnalyzer,
    name='GenMatcherAnalyzer',
    getter = lambda event : event.tau3mu,
)

level1Ana = L1TriggerAnalyzer.defaultConfig

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

weighterAna = cfg.Analyzer(
    MuonWeighterAnalyzer,
    sffileTIH = '%s/src/CMGTools/WTau3Mu/data/SFs/ScaleFactors_tight2016_muonID_updt.json'           % os.path.expandvars('$CMSSW_BASE'),
    sffileMNT = '%s/src/CMGTools/WTau3Mu/data/SFs/ScaleFactors_mediumNOTtight2016_muonID_updt.json'  % os.path.expandvars('$CMSSW_BASE'),
    sffileLNM = '%s/src/CMGTools/WTau3Mu/data/SFs/ScaleFactors_looseNOTmedium_muonID_updt.json'      % os.path.expandvars('$CMSSW_BASE'),
    multiplyEventWeight = True,
    usePtOnly = True,
    getter = lambda event : [event.tau3muRefit.mu1(), event.tau3muRefit.mu2(), event.tau3muRefit.mu3()],
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

muonRefitWeightAna = cfg.Analyzer(
    MuonWeighterAnalyzer,
    name   = 'MuonWeighterAnalyzer',
    sffile = '/afs/cern.ch/cms/Physics/muon/ReferenceEfficiencies/Run2015/25ns/SingleMuonTrigger_Z_RunD_Reco74X_Nov20.json',
    sfname  = 'Mu45_eta2p1',
    getter = lambda event : [event.tau3muRefit.mu1(), event.tau3muRefit.mu2(), event.tau3muRefit.mu3()],
    multiplyEventWeight = True,
)

muonWeightAna = cfg.Analyzer(
    MuonWeighterAnalyzer,
    name   = 'MuonWeighterAnalyzer',
    sffile = '/afs/cern.ch/cms/Physics/muon/ReferenceEfficiencies/Run2015/25ns/SingleMuonTrigger_Z_RunD_Reco74X_Nov20.json',
    sfname  = 'Mu45_eta2p1',
    getter = lambda event : [event.tau3mu.mu1(), event.tau3mu.mu2(), event.tau3mu.mu3()],
    multiplyEventWeight = False,
)

fileCleaner = cfg.Analyzer(
    FileCleaner,
    name='FileCleaner'
)

###################################################
###                  SEQUENCE                   ###
###################################################
sequence = cfg.Sequence([
    lheWeightAna,
    jsonAna,
    skimAna,
    genAna,
    triggerAna, # First analyser that applies selections
    vertexAna,
    pileUpAna,
    tau3MuAna,
    jetAna,
    genMatchAna,
#     recoilAna,
    vertexFitter,
    weighterAna,
    muIdAna,
    isoAna,
#     level1Ana,
    bdtAna,
    treeProducer,
])

###################################################
###            SET BATCH OR LOCAL               ###
###################################################
if not production:
    comp                 = WToTauTo3Mu
    selectedComponents   = [comp]
    comp.splitFactor     = 1
    comp.fineSplitFactor = 1
#     comp.files           = comp.files[:1]
    comp.files = [
       '/afs/cern.ch/work/m/manzoni/public/perLuca/newsignal/output.root'
       #'file:/afs/cern.ch/work/m/manzoni/diTau2015/CMSSW_9_2_2_minimal_recipe/src/RecoMET/METPUSubtraction/test/output.root',
#       'root://xrootd.unl.edu//store/data/Run2016B/SingleMuon/MINIAOD/PromptReco-v1/000/272/760/00000/68B88794-7015-E611-8A92-02163E01366C.root',
    ]

preprocessor = None

if extrap_muons_to_L1:
    fname = '$CMSSW_BASE/src/CMGTools/WTau3Mu/prod/muon_extrapolator_cfg.py'
    sequence.append(fileCleaner)
    preprocessor = CmsswPreprocessor(fname, addOrigAsSecondary=False)

if compute_mvamet:
    fname = '$CMSSW_BASE/src/CMGTools/WTau3Mu/prod/compute_mva_met_mc_cfg.py'
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
