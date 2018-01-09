import json
import ROOT
from itertools import product

from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle
from CMGTools.WTau3Mu.analyzers.ParticleSFgetter import ParticleSFgetter

import PhysicsTools.HeppyCore.framework.config as cfg

class DsPhiMuMuPiTriggerWeighter (Analyzer):

    def __init__(self, *args, **kwargs):
        super(DsPhiMuMuPiTriggerWeighter, self).__init__(*args, **kwargs)

    def beginLoop(self, setup):
        super(DsPhiMuMuPiTriggerWeighter, self).beginLoop(setup)
        self.jsonFile = self.cfg_ana.sffile

    def process(self, event):
        self.readCollections(event.input)

        Ds = event.ds
        jsonGetter = ParticleSFgetter(jsonFile = self.jsonFile[0], SFname = "tight2016_muonID", SFbins = "pt_abseta", usePtOnly = self.jsonFile[1])

        sf = jsonGetter.getSF(Ds)
        Ds.idweight    = sf['value'] if sf['value'] is not None else 1
        Ds.idweightunc = sf['error'] if sf['error'] is not None else 1

        if hasattr(Ds, 'weight'):
            Ds.weight *= Ds.idweight
        else:
            Ds.weight  = Ds.idweight

        if getattr(self.cfg_ana, 'multiplyEventWeight', True):
            if hasattr(event, 'eventWeight'):
                event.eventWeight *= Ds.idweight
            else:
                event.eventWeight  = Ds.idweight

        return True
    def endloop (self, setup):
        super(DsPhiMuMuPiTriggerWeighter, self).endLoop(setup)

setattr(DsPhiMuMuPiTriggerWeighter, 'defaultConfig', 
    cfg.Analyzer(
        class_object=DsPhiMuMuPiTriggerWeighter,
    )
)
