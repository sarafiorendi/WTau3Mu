import json
import ROOT
from itertools import product

from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle
from CMGTools.WTau3Mu.analyzers.ParticleSFgetter import ParticleSFgetter

import PhysicsTools.HeppyCore.framework.config as cfg

class MuonWeighterAnalyzer(Analyzer):

    def __init__(self, *args, **kwargs):
        super(MuonWeighterAnalyzer, self).__init__(*args, **kwargs)

    def beginLoop(self, setup):
        super(MuonWeighterAnalyzer, self).beginLoop(setup)
        self.jsonFile = self.cfg_ana.sffile

    def process(self, event):
        self.readCollections(event.input)
        
        muons = self.cfg_ana.getter(event)        

        ## init SF getter
        jsonGetter = ParticleSFgetter(self.jsonFile)
        
        for imu in muons:
            ## get the SF
            sf = jsonGetter.getSF(imu)
            imu.idweight    = sf['value']
            imu.idweightunc = sf['error']
            if hasattr(imu, 'weight'):
                imu.weight *= imu.idweight
            else:
                imu.weight = imu.idweight

            if getattr(self.cfg_ana, 'multiplyEventWeight', True):
                if hasattr(event, 'eventWeight'):
                    event.eventWeight *= imu.idweight
                else:
                    event.eventWeight = imu.idweight

        return True        
        
#     def endLoop(self, setup):
#         super(MuonWeighterAnalyzer, self).endLoop(setup)
#         import pdb ; pdb.set_trace()
#         self.sffile.close()


setattr(MuonWeighterAnalyzer, 'defaultConfig', 
    cfg.Analyzer(
        class_object=MuonWeighterAnalyzer,
        getter = lambda event : [event.tau3muRefit.mu1(), event.tau3muRefit.mu2(), event.tau3muRefit.mu3()],
    )
)
