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
process.GlobalTag.globaltag = '80X_mcRun2_asymptotic_2016_TrancheIV_v8' # adjust this appropriately!

from RecoMET.METPUSubtraction.jet_recorrections import reapplyPUJetID
reapplyPUJetID(process)

from RecoMET.METPUSubtraction.jet_recorrections import recorrectJets
recorrectJets(process, False)
jetCollection = 'patJetsReapplyJEC'

from PhysicsTools.PatUtils.tools.runMETCorrectionsAndUncertainties import runMetCorAndUncFromMiniAOD
runMetCorAndUncFromMiniAOD(process, isData=False, jetCollUnskimmed=jetCollection )

from PhysicsTools.PatAlgos.slimming.puppiForMET_cff import makePuppiesFromMiniAOD
makePuppiesFromMiniAOD( process );
runMetCorAndUncFromMiniAOD(
    process,
    isData          = False,
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
    'file:/afs/cern.ch/work/m/mverzett/public/perRic/t3mMINIAODSIM/t3mu_MINIAODSIM_0.root',
    'file:/afs/cern.ch/work/m/mverzett/public/perRic/t3mMINIAODSIM/t3mu_MINIAODSIM_1.root',
    'file:/afs/cern.ch/work/m/mverzett/public/perRic/t3mMINIAODSIM/t3mu_MINIAODSIM_2.root',
    'file:/afs/cern.ch/work/m/mverzett/public/perRic/t3mMINIAODSIM/t3mu_MINIAODSIM_3.root',
    'file:/afs/cern.ch/work/m/mverzett/public/perRic/t3mMINIAODSIM/t3mu_MINIAODSIM_4.root',
    'file:/afs/cern.ch/work/m/mverzett/public/perRic/t3mMINIAODSIM/t3mu_MINIAODSIM_5.root',
    'file:/afs/cern.ch/work/m/mverzett/public/perRic/t3mMINIAODSIM/t3mu_MINIAODSIM_6.root',
    'file:/afs/cern.ch/work/m/mverzett/public/perRic/t3mMINIAODSIM/t3mu_MINIAODSIM_7.root',
    'file:/afs/cern.ch/work/m/mverzett/public/perRic/t3mMINIAODSIM/t3mu_MINIAODSIM_8.root',
    'file:/afs/cern.ch/work/m/mverzett/public/perRic/t3mMINIAODSIM/t3mu_MINIAODSIM_9.root',
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