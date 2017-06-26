# Import CMS python class definitions such as Process, Source, and EDProducer
import FWCore.ParameterSet.Config as cms

process = cms.Process('EXTRAP')

process.load('Configuration/StandardSequences/Services_cff')
process.load('FWCore/MessageService/MessageLogger_cfi')
process.load('Configuration.StandardSequences.Reconstruction_cff')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')

process.GlobalTag.globaltag = cms.string( "92X_upgrade2017_TSG_For83XSamples_V4" )

# Configure the object that reads the input file
process.source = cms.Source('PoolSource', 
    fileNames = cms.untracked.vstring(
#         'file:/afs/cern.ch/work/m/manzoni/public/perLuca/outputFULL.root',
        'file:/afs/cern.ch/work/m/manzoni/tauHLT/2017/CMSSW_9_1_0_pre3/src/Tau3Mu/outputFULL.root',
    ),
)

process.extrapolator = cms.EDProducer(
    'L1MuonRecoPropagator',
    patMuonSrc = cms.InputTag('slimmedMuons'),
)

# Configure the object that writes an output file
process.out = cms.OutputModule('PoolOutputModule',
    fileName = cms.untracked.string('output.root'),
)

process.muonPropagatorPath = cms.Path(process.extrapolator)

process.prunedOutput = cms.EndPath( process.out )

# limit the number of events to be processed
process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32( -1 )
)


