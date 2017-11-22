import PhysicsTools.HeppyCore.framework.config as cfg
import os

#####COMPONENT CREATOR

from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator

creator = ComponentCreator()

DsPhiPiMuFilter = creator.makeMCComponent(
    "DsPhiPiMuFilter", 
    "/DsToPhiPi_MuFilter_TuneCUEP8M1_13TeV-pythia8/RunIISummer17MiniAOD-NZSFlatPU28to62_92X_upgrade2017_realistic_v10-v1/MINIAODSIM", 
    "CMS", 
    ".*root", 
    1.0,
    useAAA=True,
)






# https://cmsweb.cern.ch/das/request?view=list&limit=50&instance=prod%2Fglobal&input=dataset%3D%2FDsToPhiPi*13TeV-pythia*%2F*%2FMINIAODSIM

# /DsToPhiPi_TuneCUEP8M1_13TeV-pythia8-evtGen/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM
# /DsToPhiPi_MuFilter_TuneCUEP8M1_13TeV-pythia8/RunIISummer17MiniAOD-NZSFlatPU28to62_92X_upgrade2017_realistic_v10-v1/MINIAODSIM
# /DsToPhiPi_TuneCUEP8M1_13TeV-pythia8-evtGen/RunIIFall15MiniAODv1-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM
# /DsToPhiPi_TuneCUEP8M1_13TeV-pythia8-evtGen/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM
# /DsToPhiPi_TuneCUEP8M1_13TeV-pythia8-evtGen/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM
