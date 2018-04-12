import json

from itertools      import product

from PhysicsTools.Heppy.analyzers.core.Analyzer         import Analyzer
from PhysicsTools.Heppy.analyzers.core.AutoHandle       import AutoHandle
from CMGTools.WTau3Mu.analyzers.ParticleSFgetter        import ParticleSFgetter

import PhysicsTools.HeppyCore.framework.config as cfg

class MuonWeighterAnalyzer(Analyzer):

    def __init__(self, *args, **kwargs):
        super(MuonWeighterAnalyzer, self).__init__(*args, **kwargs)

    def beginLoop(self, setup):
        super(MuonWeighterAnalyzer, self).beginLoop(setup)
        ## muonID jsons
        self.jsonFileID_TIH = self.cfg_ana.jsonFileID_TIH
        self.jsonFileID_MNT = self.cfg_ana.jsonFileID_MNT
        self.jsonFileID_LNM = self.cfg_ana.jsonFileID_LNM
        self.jsonFileID_SNL = self.cfg_ana.jsonFileID_SNL
        ## HLT jsons
        self.jsonFileHLT_MU = self.cfg_ana.jsonFileHLT_MU
        self.jsonFileHLT_TK = self.cfg_ana.jsonFileHLT_TK

    def process(self, event):
        self.readCollections(event.input)
        
        muons = self.cfg_ana.getter(event)    

        ## init SF getters for each ID
        jsonGetterTIH = ParticleSFgetter(jsonFile = self.jsonFileID_TIH[0], SFname = "tight2016_muonID"          , SFbins = self.jsonFileID_TIH[1])
        jsonGetterMNT = ParticleSFgetter(jsonFile = self.jsonFileID_MNT[0], SFname = "mediumNOTtight2016_muonID" , SFbins = self.jsonFileID_MNT[1])
        jsonGetterLNM = ParticleSFgetter(jsonFile = self.jsonFileID_LNM[0], SFname = "looseNOTmedium_muonID"     , SFbins = self.jsonFileID_LNM[1])
        jsonGetterSNL = ParticleSFgetter(jsonFile = self.jsonFileID_SNL[0], SFname = "soft2016NOTloose_muonID"   , SFbins = self.jsonFileID_SNL[1])
        jsonGetterMU = ParticleSFgetter(jsonFile = self.jsonFileHLT_MU[0], SFname = 'RunBH_muonID'  , SFbins = self.jsonFileHLT_MU[1])
        jsonGetterTK = ParticleSFgetter(jsonFile = self.jsonFileHLT_TK[0], SFname = 'HLT_track'     , SFbins = self.jsonFileHLT_TK[1])
        
        ## get the SF for the HLT
        HLTmuons = [ mu for ii, mu in enumerate(muons) if event.tau3mu.best_trig_match[ii+1]['HLT_DoubleMu3_Trk_Tau3mu'] is not None and event.tau3mu.best_trig_match[ii+1]['HLT_DoubleMu3_Trk_Tau3mu'].triggerObjectTypes()[0] == 83]
        HLTtrack = [ tk for ii, tk in enumerate(muons) if event.tau3mu.best_trig_match[ii+1]['HLT_DoubleMu3_Trk_Tau3mu'] is not None and event.tau3mu.best_trig_match[ii+1]['HLT_DoubleMu3_Trk_Tau3mu'].triggerObjectTypes()[0] == 91]

        ## Offline muon ID weight
        for mu in muons:
        ## get the SF for the ID
            if   mu.muonID('POG_ID_Tight') :   sf = jsonGetterTIH.getSF(mu)
            elif mu.muonID('POG_ID_Medium'):   sf = jsonGetterMNT.getSF(mu)
            elif mu.muonID('POG_ID_Loose') :   sf = jsonGetterLNM.getSF(mu)
            elif mu.muonID('POG_ID_Soft')  :   sf = jsonGetterSNL.getSF(mu)
            else                           :   sf = jsonGetterSNL.getNone()

            mu.idweight    =  sf['value'] if sf['value'] is not None else 1
            mu.idweightunc =  sf['error'] if sf['error'] is not None else 1
       
            mu.weight = mu.weight * mu.idweight if hasattr(mu, 'weight') else mu.idweight

        ## HLT muon ID weight
        for mu in HLTmuons: 
            sf = jsonGetterMU.getSF(mu)
            mu.HLTWeightMU    = sf['value'] if sf['value'] is not None else 1
            mu.HLTWeightUncMU = sf['error'] if sf['error'] is not None else 1

            mu.weight = mu.weight * mu.HLTWeightMU if hasattr(mu, 'weight') else mu.HLTWeightMU

        ## HLT track ID weight (assigned on tau)
        tauObject = muons[0].p4() + muons[1].p4() + muons[2].p4()

        sf = jsonGetterTK.getSF(tauObject)

        event.tau3mu.HLTWeightTK    = sf['value'] if sf['value'] is not None else 1
        event.tau3mu.HLTWeightUncTK = sf['error'] if sf['error'] is not None else 1

        event.tau3mu.weight = event.tau3mu.weight * event.tau3mu.HLTWeightTK if hasattr(event.tau3mu, 'weight') else event.tau3mu.HLTWeightTK

        ## define the final event weight
        if not getattr(self.cfg_ana, 'multiplyEventWeight'): event.eventWeight = 1      

        for mu in muons:
            if not hasattr(mu, 'weight'): mu.weight = 1
            event.eventWeight = event.eventWeight * mu.weight if hasattr(event, 'eventWeight') else mu.weight

        event.eventWeight = event.eventWeight * event.tau3mu.weight if hasattr(event, 'eventWeight') else event.tau3mu.weight
        
        return True        
        
setattr(MuonWeighterAnalyzer, 'defaultConfig', 
    cfg.Analyzer(
        class_object=MuonWeighterAnalyzer,
    )
)
