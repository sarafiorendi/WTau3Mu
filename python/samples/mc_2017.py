import PhysicsTools.HeppyCore.framework.config as cfg
import os

#####COMPONENT CREATOR

from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator
kreator = ComponentCreator()

'''
# TSG 20176 production, w/ new tracking
WToTauTo3Mu = kreator.makeMyPrivateMCComponent(
    'WToTauTo3Mu'  , 
#     '/WToTauNu_TauTo3Mu_MadGraph_13TeV/manzoni-WTau3Mu2017V1-10585ddae7927f5a25730c0c14632ac5/USER', # missing track extra...
    '/WToTauNu_TauTo3Mu_MadGraph_13TeV/manzoni-WTau3Mu2017EnrichedV2-10585ddae7927f5a25730c0c14632ac5/USER', #with track extra
    'PRIVATE', 
    '.*root', 
    dbsInstance='phys03', 
    xSec=20508.9 * 1.e-7, # W to lep nu / 3.[pb] x BR
    useAAA=True,
)
'''

WToTauTo3Mu = kreator.makeMCComponent(
    name       = 'WToTauTo3Mu',
    dataset    = '/WToTauNu_TauTo3Mu_MadGraph_13TeV/PhaseIFall16MiniAOD-FlatPU28to62HcalNZSRAW_PhaseIFall16_90X_upgrade2017_realistic_v6_C1-v1/MINIAODSIM',
    user       = 'CMS',
    pattern    = '.*root',
    xSec       = 20508.9 * 1.e-7, # W to lep nu / 3.[pb] x BR
    useAAA     = True,
)
