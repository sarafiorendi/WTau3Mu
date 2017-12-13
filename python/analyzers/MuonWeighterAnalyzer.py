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
        self.jsonFileTIH = self.cfg_ana.sffileTIH
        self.jsonFileMNT = self.cfg_ana.sffileMNT
        self.jsonFileLNM = self.cfg_ana.sffileLNM
        self.jsonFileSNL = self.cfg_ana.sffileSNL

    def process(self, event):
        self.readCollections(event.input)
        
        muons = self.cfg_ana.getter(event)        

        ## init SF getters for each ID
        jsonGetterTIH = ParticleSFgetter(jsonFile = self.jsonFileTIH[0], SFname = "tight2016_muonID"          , SFbins = "pt", usePtOnly = self.jsonFileTIH[1])
        jsonGetterMNT = ParticleSFgetter(jsonFile = self.jsonFileMNT[0], SFname = "mediumNOTtight2016_muonID" , SFbins = "pt", usePtOnly = self.jsonFileMNT[1])
        jsonGetterLNM = ParticleSFgetter(jsonFile = self.jsonFileLNM[0], SFname = "looseNOTmedium_muonID"     , SFbins = "pt", usePtOnly = self.jsonFileLNM[1])
        jsonGetterSNL = ParticleSFgetter(jsonFile = self.jsonFileSNL[0], SFname = "soft2016NOTloose_muonID"   , SFbins = "pt", usePtOnly = self.jsonFileSNL[1])
        
        for imu in muons:
            ## get the SF based in the ID
            if   imu.muonID('POG_ID_Tight') :   sf = jsonGetterTIH.getSF(imu)
            elif imu.muonID('POG_ID_Medium'):   sf = jsonGetterMNT.getSF(imu)
            elif imu.muonID('POG_ID_Loose') :   sf = jsonGetterLNM.getSF(imu)
            else:                               sf = jsonGetterSNL.getSF(imu)

            imu.idweight    =  sf['value']
            imu.idweightunc =  sf['error']
            
            if hasattr(imu, 'weight'):
                imu.weight *= imu.idweight
            else:
                imu.weight  = imu.idweight

            if getattr(self.cfg_ana, 'multiplyEventWeight', True):
                if hasattr(event, 'eventWeight'):
                    event.eventWeight *= imu.idweight
                else:
                    event.eventWeight  = imu.idweight

        return True        
        
    def endLoop(self, setup):
        super(MuonWeighterAnalyzer, self).endLoop(setup)


setattr(MuonWeighterAnalyzer, 'defaultConfig', 
    cfg.Analyzer(
        class_object=MuonWeighterAnalyzer,
        getter = lambda event : [event.tau3muRefit.mu1(), event.tau3muRefit.mu2(), event.tau3muRefit.mu3()],
    )
)
