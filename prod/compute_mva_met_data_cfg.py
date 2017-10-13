import sys
import FWCore.ParameterSet.Config as cms
from FWCore.ParameterSet.VarParsing import VarParsing
from PhysicsTools.PatAlgos.tools.tauTools import *
from RecoMET.METPUSubtraction.MVAMETConfiguration_cff import runMVAMET

process = cms.Process('MVAMET')

process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
jetCollection = 'slimmedJets'

process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')
process.GlobalTag.globaltag = '80X_dataRun2_2016SeptRepro_v7' # adjust this appropriately!

from RecoMET.METPUSubtraction.jet_recorrections import reapplyPUJetID
reapplyPUJetID(process)

from RecoMET.METPUSubtraction.jet_recorrections import recorrectJets
recorrectJets(process, True)
jetCollection = 'patJetsReapplyJEC'

from PhysicsTools.PatUtils.tools.runMETCorrectionsAndUncertainties import runMetCorAndUncFromMiniAOD
runMetCorAndUncFromMiniAOD(process, isData=True, jetCollUnskimmed=jetCollection )

from PhysicsTools.PatAlgos.slimming.puppiForMET_cff import makePuppiesFromMiniAOD
makePuppiesFromMiniAOD( process );
runMetCorAndUncFromMiniAOD(
    process,
    isData          = True,
    metType         = 'Puppi',
    pfCandColl      = cms.InputTag('puppiForMET'),
    recoMetFromPFCs = True,
    reclusterJets   = True,
    jetFlavor       = 'AK4PFPuppi',
    postfix         = 'Puppi'
)

getattr(process, jetCollection).userData.userFloats.src += ['pileupJetIdUpdated:fullDiscriminant']

# configure MVA MET
runMVAMET( process, jetCollectionPF = jetCollection, debug=False)

process.slimmedMuonsLoose = cms.EDProducer('patMuonIDIsoSelector',
    charged_hadron_iso = cms.InputTag(''),
    etaCut = cms.double(2.5),
    neutral_hadron_iso = cms.InputTag(''),
    photon_iso = cms.InputTag(''),
    ptCut = cms.double(0.8),
    relativeIsolationCut = cms.double(999.),
    rho = cms.InputTag('fixedGridRhoFastjetAll'),
    src = cms.InputTag('slimmedMuons'),
    typeID = cms.string('Loose'),
    typeIso = cms.string('dBeta'),
    vertex = cms.InputTag('offlineSlimmedPrimaryVertices')
)

##########################################################################################
srcMuons   = 'slimmedMuons' ## inputMuonCollection
muonTypeID = '' ## type of muon ID to be applied                                                                                                   
# muonTypeID = 'Loose' ## type of muon ID to be applied                                                                                                   
process.MVAMET.combineNLeptons = cms.int32(3)
process.MVAMET.requireOS = cms.bool(False)
process.MVAMET.srcLeptons  = cms.VInputTag(srcMuons+muonTypeID)

## set input files
process.source = cms.Source('PoolSource')
# process.source.fileNames = cms.untracked.vstring(options.inputFile)
process.source.fileNames = cms.untracked.vstring(
#  'root://cms-xrd-global.cern.ch//store/data/Run2016H/DoubleMuonLowMass/MINIAOD/03Feb2017_ver3-v1/110000/38124D4E-C8EB-E611-875F-0025905A6088.root',
#  'root://cms-xrd-global.cern.ch//store/data/Run2016H/DoubleMuonLowMass/MINIAOD/03Feb2017_ver3-v1/110000/40663461-86EB-E611-954A-0CC47A74525A.root',
#  'root://cms-xrd-global.cern.ch//store/data/Run2016H/DoubleMuonLowMass/MINIAOD/03Feb2017_ver3-v1/110000/683A5D5F-86EB-E611-B96F-0025905A60A8.root',
#  'root://cms-xrd-global.cern.ch//store/data/Run2016H/DoubleMuonLowMass/MINIAOD/03Feb2017_ver3-v1/110000/CA9E265B-C8EB-E611-B9FB-0CC47A4D7634.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2016E/DoubleMuonLowMass/MINIAOD/23Sep2016-v1/50000/C881EEF5-8590-E611-91F6-0CC47AD98A92.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2016E/DoubleMuonLowMass/MINIAOD/23Sep2016-v1/50000/C8AC428A-8190-E611-B72D-003048F5B614.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2016E/DoubleMuonLowMass/MINIAOD/23Sep2016-v1/50000/CE53955B-A393-E611-B340-0242AC130002.root',
)

## logger
process.load('FWCore.MessageLogger.MessageLogger_cfi')
process.MessageLogger.cerr.FwkReport.reportEvery = 100

#! Output and Log                                                                                                                                                            
process.options   = cms.untracked.PSet(wantSummary = cms.untracked.bool(True))
#  in >= 910 this is irrelevant https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideUnscheduledExecution
# process.options.allowUnscheduled = cms.untracked.bool(True)
# process.options.allowUnscheduled = cms.untracked.bool(False)


##########################################################################################
# configure the unscheduled mode appropriately in >= 910
# combine all this info
# https://hypernews.cern.ch/HyperNews/CMS/get/edmFramework/3787.html
# https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideAboutPythonConfigFile#Task_Objects
# https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideUnscheduledExecution
# dump the full cfg in 8026
process.MVAMETtask = cms.Task(
    process.egmGsfElectronIDTask,
    process.slimmedMuonsTight,
    process.slimmedMuonsLoose,
    process.slimmedElectronsTight,
    process.slimmedTausLoose,
    process.slimmedTausLooseCleaned,
    process.tausSignificance,
    process.tauMET,
    process.tauPFMET,
    process.allDecayProducts,
    process.tauDecayProducts,
    process.patpfTrackMET,
    process.pfTrackMET,
    process.pfTrackMETCands,
    process.pfChargedPV,
    process.patpfNoPUMET,
    process.pfNoPUMET,
    process.pfNoPUMETCands,
    process.neutralInJets,
    process.patJetsReapplyJEC,
    process.patJetCorrFactorsReapplyJEC,
    process.pileupJetIdUpdated,
    process.pfNeutrals,
    process.patpfPUCorrectedMET,
    process.pfPUCorrectedMET,
    process.pfPUCorrectedMETCands,
    process.patpfPUMET,
    process.pfPUMET,
    process.pfPUMETCands,
    process.pfChargedPU,
    process.MVAMET
)

process.p = cms.Path(
    process.MVAMETtask
)

process.MVAMETSchedule = cms.Schedule(
    process.p
)
##########################################################################################

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
) 


process.output = cms.OutputModule('PoolOutputModule',
                                  fileName = cms.untracked.string('output_mvamet.root'),
                                  outputCommands = cms.untracked.vstring(
#                                                                          'keep patMETs_slimmedMETs_*_MVAMET',
#                                                                          'keep patMETs_slimmedMETsPuppi_*_MVAMET',
#                                                                          'keep patMETs_MVAMET_*_MVAMET',
#                                                                          'keep *_patJetsReapplyJEC_*_MVAMET',
                                                                         'keep *',
                                                                         ),        
#                                   SelectEvents = cms.untracked.PSet(  SelectEvents = cms.vstring('p'))
                                 )

process.out = cms.EndPath(process.output)






##########################################################################################
# process.source.eventsToProcess = cms.untracked.VEventRange('1:1:42')
# process.MVAMET.srcMuons = cms.InputTag('slimmedMuons')