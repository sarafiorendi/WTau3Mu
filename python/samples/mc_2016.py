import PhysicsTools.HeppyCore.framework.config as cfg
import os

#####COMPONENT CREATOR

from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator
kreator = ComponentCreator()

# first private production
WToTauTo3Mu = cfg.MCComponent(
    dataset       = 'WToTauTo3Mu',
    name          = 'WToTauTo3Mu',
    files         = [
        '/afs/cern.ch/work/m/mverzett/public/perRic/t3mMINIAODSIM/t3mu_MINIAODSIM_0.root',
#         '/afs/cern.ch/work/m/mverzett/public/perRic/t3mMINIAODSIM/t3mu_MINIAODSIM_1.root',
#         '/afs/cern.ch/work/m/mverzett/public/perRic/t3mMINIAODSIM/t3mu_MINIAODSIM_2.root',
#         '/afs/cern.ch/work/m/mverzett/public/perRic/t3mMINIAODSIM/t3mu_MINIAODSIM_3.root',
#         '/afs/cern.ch/work/m/mverzett/public/perRic/t3mMINIAODSIM/t3mu_MINIAODSIM_4.root',
#         '/afs/cern.ch/work/m/mverzett/public/perRic/t3mMINIAODSIM/t3mu_MINIAODSIM_5.root',
#         '/afs/cern.ch/work/m/mverzett/public/perRic/t3mMINIAODSIM/t3mu_MINIAODSIM_6.root',
#         '/afs/cern.ch/work/m/mverzett/public/perRic/t3mMINIAODSIM/t3mu_MINIAODSIM_7.root',
#         '/afs/cern.ch/work/m/mverzett/public/perRic/t3mMINIAODSIM/t3mu_MINIAODSIM_8.root',
#         '/afs/cern.ch/work/m/mverzett/public/perRic/t3mMINIAODSIM/t3mu_MINIAODSIM_9.root',
          #### with MVA MET computed
#           '/afs/cern.ch/work/m/manzoni/diTau2015/CMSSW_9_2_2_minimal_recipe/src/RecoMET/METPUSubtraction/test/output.root',
    ],
    xSection      = 21490.9, # this uses the correct tau BR from the PDG # 20508.9 * 1.e-7, # W to lep nu / 3.[pb] x BR
#     xSection      = 20508.9 * 0.005, # W to lep nu / 3.[pb] x BR
    nGenEvents    = 20000.,
    triggers      = ['HLT_DoubleMu3_Trk_Tau3mu_v%d' %i for i in range(1, 5)],
    effCorrFactor = 1,
)

