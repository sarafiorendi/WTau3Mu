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

# WTau3Mu analysers
from CMGTools.WTau3Mu.analyzers.DsPhiMuMuPiAnalyzer                      import DsPhiMuMuPiAnalyzer
from CMGTools.WTau3Mu.analyzers.DsPhiMuMuPiGenMatcherAnalyzer            import DsPhiMuMuPiGenMatcherAnalyzer
from CMGTools.WTau3Mu.analyzers.L1TriggerAnalyzer                        import L1TriggerAnalyzer
from CMGTools.WTau3Mu.analyzers.MuonWeighterAnalyzer                     import MuonWeighterAnalyzer
from CMGTools.WTau3Mu.analyzers.DsPhiMuMuPiTreeProducer                  import DsPhiMuMuPiTreeProducer
from CMGTools.WTau3Mu.analyzers.DsPhiMuMuPiKinematicVertexFitterAnalyzer import DsPhiMuMuPiKinematicVertexFitterAnalyzer

# import samples, signal
from CMGTools.WTau3Mu.samples.ds_mc import DsPhiMuMuPi

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
compute_mvamet     = getHeppyOption('compute_mvamet'    , False)
###################################################
###               HANDLE SAMPLES                ###
###################################################
samples = [DsPhiMuMuPi]

for sample in samples:
    sample.triggers  = ['HLT_Dimuon0_Phi_Barrel_v%d'   %i for i in range(1,  8)]
    sample.triggers += ['HLT_DoubleMu3_Trk_Tau3mu_v%d' %i for i in range(1, 12)]
    sample.splitFactor = splitFactor(sample, 2e5)
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
    requireTrigger=False,
    usePrescaled=True,
    triggerResultsHandle=('TriggerResults', '', 'HLT'),
    triggerObjectsHandle=('selectedPatTrigger', '', 'PAT'),
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
triggers_and_filters['HLT_Dimuon0_Phi_Barrel'  ] = ['hltDisplacedmumuFilterDimuon0PhiBarrel', 'hltDisplacedmumuFilterDimuon0PhiBarrel']
triggers_and_filters['HLT_DoubleMu3_Trk_Tau3mu'] = ['hltTau3muTkVertexFilter', 'hltTau3muTkVertexFilter', 'hltTau3muTkVertexFilter']

dsAna = cfg.Analyzer(
    DsPhiMuMuPiAnalyzer,
    name='DsPhiMuMuPiAnalyzer',
    trigger_match=triggers_and_filters,
    trigger_flag=True, # save all events, even those that don't pass the trigger but save also a flag as to whether the trigger was fired
)

genMatchAna = cfg.Analyzer(
    DsPhiMuMuPiGenMatcherAnalyzer,
    name='DsPhiMuMuPiGenMatcherAnalyzer',
    getter = lambda event : event.ds,
)

kinFitAnalyzer = cfg.Analyzer(
    DsPhiMuMuPiKinematicVertexFitterAnalyzer,
    name='DsPhiMuMuPiKinematicVertexFitterAnalyzer',
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

muonWeightAna = cfg.Analyzer(
    MuonWeighterAnalyzer,
    name   = 'MuonWeighterAnalyzer',
    sffile = '/afs/cern.ch/cms/Physics/muon/ReferenceEfficiencies/Run2015/25ns/SingleMuonTrigger_Z_RunD_Reco74X_Nov20.json',
    sfname  = 'Mu45_eta2p1',
    getter = lambda event : [event.ds.mu1(), event.ds.mu2()],
    multiplyEventWeight = True,
)

treeProducer = cfg.Analyzer(
    DsPhiMuMuPiTreeProducer,
    name = 'DsPhiMuMuPiTreeProducer'
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
    jsonAna,
    skimAna,
    genAna,
    triggerAna, # First analyser that applies selections
    vertexAna,
    pileUpAna,
    dsAna,
    kinFitAnalyzer,
    jetAna,
#     genMatchAna,
#     muonWeightAna,
    treeProducer,
])

###################################################
###            SET BATCH OR LOCAL               ###
###################################################
if not production:
    comp                 = DsPhiMuMuPi
    selectedComponents   = [comp]
    comp.splitFactor     = 1
    comp.fineSplitFactor = 1
    comp.files           = comp.files[:1]
#     comp.files = [
#        'file:/afs/cern.ch/work/m/manzoni/diTau2015/CMSSW_9_2_2_minimal_recipe/src/RecoMET/METPUSubtraction/test/output.root',
#        'root://xrootd.unl.edu//store/data/Run2016B/SingleMuon/MINIAOD/PromptReco-v1/000/272/760/00000/68B88794-7015-E611-8A92-02163E01366C.root',
#     ]

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
