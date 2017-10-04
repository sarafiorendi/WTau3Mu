# import dill # needed in order to serialise lambda functions, need to be installed by the user. See http://stackoverflow.com/questions/25348532/can-python-pickle-lambda-functions
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

# import samples, signal
from CMGTools.WTau3Mu.samples.mc_2017 import WToTauTo3Mu

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
###################################################
###               HANDLE SAMPLES                ###
###################################################
samples = [WToTauTo3Mu]

for sample in samples:
#     sample.triggers = ['HLT_DoubleMu3_Trk_Tau3mu_v%d' %i for i in range(1, 5)]
    # specify which muon should match to which filter. 
#     sample.trigger_filters = [
#         (lambda triplet : triplet.mu1(), ['hltTau3muTkVertexFilter']),
#         (lambda triplet : triplet.mu2(), ['hltTau3muTkVertexFilter']),
#         (lambda triplet : triplet.mu3(), ['hltTau3muTkVertexFilter']),
#     ]
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
    requireTrigger=False,
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

tau3MuAna = cfg.Analyzer(
    Tau3MuAnalyzer,
    name='Tau3MuAnalyzer',
    trigger_match=False,
)

treeProducer = cfg.Analyzer(
    WTau3MuTreeProducer,
    name='WTau3MuTreeProducer',
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
level1Ana.collection = ('simGmtStage2Digis', '', 'RAW2DIGI')

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
    name='JetAnalyzer',
    jetCol='slimmedJets',
    jetPt=20.,
    jetEta=4.7,
    relaxJetId=False, # relax = do not apply jet ID
    relaxPuJetId=True, # relax = do not apply pileup jet ID
    jerCorr=False,
    #jesCorr = 1., # Shift jet energy scale in terms of uncertainties (1 = +1 sigma)
    puJetIDDisc='pileupJetId:fullDiscriminant',
    recalibrateJets=True,
    applyL2L3Residual='MC',
    mcGT='80X_mcRun2_asymptotic_2016_TrancheIV_v8',
    dataGT='80X_dataRun2_2016SeptRepro_v7',
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
#     jetAna,
    genMatchAna,
#     recoilAna,
    vertexFitter,
    muIdAna,
    isoAna,
#     level1Ana,
    bdtAna,
    treeProducer,
])

###################################################
###                PICK EVENTS                  ###
###################################################
if pick_events:
    eventSelector.toSelect = [
         5870,
         5900,
         5899,
         5912,
         5927,
         5950,
         5955,
         6000,
        38071,
         6019,
         6025,
         6045,
         6130,
         6160,
         6195,
         9639,
         9702,
         9740,
         9744,
         9780,
        38203,
        38264,
        38281,
        38397,
        59654,
        59695,
        59734,
        59733,
        59737,
        59751,
        59802,
        59944,
        59974,
        59987,
        64309,
        64305,
        64332,
        64429,
        64479,
        80175,
        87267,
        87353,
        87835,
        87852,
        87933,
        87953,
        88084,
         7027,
         7076,
         7079,
         7165,
        28614,
        28718,
        28747,
        28762,
        28792,
        28875,
        28942,
        28946,
        28969,
        28997,
        58073,
        58157,
        62806,
        62826,
        62922,
        63018,
        63041,
        63133,
        63141,
        79022,
        79068,
        79120,
        79161,
        79191,
        78382,
        78407,
        78544,
        83347,
        83370,
        84002,
        84065,
        84079,
        84081,
    ]
    sequence.insert(0, eventSelector)

###################################################
###            SET BATCH OR LOCAL               ###
###################################################
if not production:
    comp                 = WToTauTo3Mu
    selectedComponents   = [comp]
    comp.splitFactor     = 1
    comp.fineSplitFactor = 1
#     comp.files           = comp.files[:1]
#     comp.files = [
#       'file:/afs/cern.ch/work/m/manzoni/tauHLT/2017/CMSSW_9_1_0_pre3/src/Tau3Mu/outputFULL.root',
#       # 'root://xrootd.unl.edu//store/data/Run2016B/SingleMuon/MINIAOD/PromptReco-v1/000/272/760/00000/68B88794-7015-E611-8A92-02163E01366C.root',
#     ]

preprocessor = None

if extrap_muons_to_L1:
    fname = '$CMSSW_BASE/src/CMGTools/WTau3Mu/prod/muon_extrapolator_cfg.py'
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
