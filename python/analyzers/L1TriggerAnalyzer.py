import ROOT
from itertools import product

from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle
from PhysicsTools.HeppyCore.utils.deltar import deltaR

from PhysicsTools.Heppy.physicsobjects.Tau import Tau
from PhysicsTools.Heppy.physicsobjects.Muon import Muon
from PhysicsTools.Heppy.physicsobjects.Electron import Electron
from PhysicsTools.Heppy.physicsobjects.Jet import Jet

from CMGTools.WTau3Mu.physicsobjects.L1Candidate import L1Candidate

import PhysicsTools.HeppyCore.framework.config as cfg


class Stage2L1ObjEnum:
    EGamma, EtSum, Jet, Tau, Muon = [0, 3, 5, 7, 9] # nor range(5) to keep some compatibility with stage-1 


class L1TriggerAnalyzer(Analyzer):

    def __init__(self, *args, **kwargs):
        super(L1TriggerAnalyzer, self).__init__(*args, **kwargs)
        self.types = {
            Tau      : ROOT.l1t.Tau   ,
            Muon     : ROOT.l1t.Muon  ,
            Electron : ROOT.l1t.EGamma,
            Jet      : ROOT.l1t.Jet   ,
        }
            
    def beginLoop(self, setup):
        super(L1TriggerAnalyzer, self).beginLoop(setup)
        self.counters.addCounter('L1TriggerAnalyzer')
        count = self.counters.counter('L1TriggerAnalyzer')
        count.register('all events')

    def declareHandles(self):
        super(L1TriggerAnalyzer, self).declareHandles()
        
        if hasattr(self.cfg_ana, 'collection'): collection = self.cfg_ana.collection
        else: collection = ('gmtStage2Digis', 'Muon', 'HLT')
                    
        self.handles[Stage2L1ObjEnum.Muon] = AutoHandle( collection, 'BXVector<l1t::Muon>' )
        
    def process(self, event):
        self.readCollections(event.input)
        
        muons = [event.tau3muRefit.mu1(), event.tau3muRefit.mu2(), event.tau3muRefit.mu3()]
                
        dRmax = 0.3
        if hasattr(self.cfg_ana, 'dR'):
            dRmax = self.cfg_ana.dR
        
        muons = self.cfg_ana.getter(event)
        
        for mu in muons:
            mu.L1matches = []
                    
        L1muons = self.handles[Stage2L1ObjEnum.Muon].product()
                                    
        allL1objects = []
        for i in range(L1muons.size(0)):
            l1 = L1muons.at(0, i)
            l1.bx    = 0                
            l1.index = i                
            allL1objects.append(l1)
                    
        for mu, l1 in product(muons, allL1objects):
            dR          = deltaR(l1, mu)
            myL1        = L1Candidate(l1)
            myL1.type   = Stage2L1ObjEnum.Muon 
            myL1.bx     = l1.bx
            myL1.dR     = dR   
            myL1.goodID = isinstance(l1, self.types[type(mu)])          
            if dR < dRmax:
                mu.L1matches.append(myL1)

        for mu in muons:
            if len(mu.L1matches):
                mu.L1matches.sort(key = lambda l1 : (l1.goodID, l1.pt(), -l1.dR), reverse = True)
                mu.L1 = mu.L1matches[0]

#         if not hasattr(muons[0], 'L1'):
#             import pdb ; pdb.set_trace()
            
        return True

setattr(L1TriggerAnalyzer, 'defaultConfig', 
    cfg.Analyzer(
        class_object=L1TriggerAnalyzer,
        getter = lambda event : [event.tau3muRefit.mu1(), event.tau3muRefit.mu2(), event.tau3muRefit.mu3()],
        dR=0.3
    )
)
