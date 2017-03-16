import PhysicsTools.HeppyCore.framework.config as cfg
import os

#####COMPONENT CREATOR

from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator
kreator = ComponentCreator()

# not needed if the sample is not published in DBS
# WToTauTo3Mu = kreator.makeMCComponent(""    , "" , "CMS", ".*root", 1.)


WToTauTo3Mu = cfg.MCComponent(
    dataset       = 'WToTauTo3Mu',
    name          = 'WToTauTo3Mu',
    files         = ['file:/afs/cern.ch/work/m/mverzett/public/t3mu_MINIAODSIM.root'],
    xSection      = 1.,
    nGenEvents    = 10,
    triggers      = ['HLT_DoubleMu3_Trk_Tau3mu_v%d' %i for i in range(1, 5)],
    effCorrFactor = 1,
)
