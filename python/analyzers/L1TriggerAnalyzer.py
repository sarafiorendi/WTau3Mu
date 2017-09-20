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
        else: collection = ('gmtStage2Digis', 'Muon', 'RECO')
        #self.handles[Stage2L1ObjEnum.Muon] = AutoHandle( collection, 'BXVector<l1t::Muon>' )

        self.handles[Stage2L1ObjEnum.Muon]    = AutoHandle( collection, 
                                    'BXVector<l1t::Muon>' 
        )        
        self.handles['extMuonsBB']         = AutoHandle( 
                                    ('extrapolator', 'MB2extrap', 'EXTRAP'), 
                                    'vector<pair<edm::Ptr<pat::Muon>,TLorentzVector> >' 
        ) #muoni estrapolati (BARREL)
        self.handles['extMuonsEP']         = AutoHandle( 
                                    ('extrapolator', 'ME2Pextrap', 'EXTRAP'), 
                                    'vector<pair<edm::Ptr<pat::Muon>,TLorentzVector> >' 
        ) #muoni estrapolati (ENDCAP+)
        self.handles['extMuonsEM']         = AutoHandle( 
                                    ('extrapolator', 'ME2Mextrap', 'EXTRAP'), 
                                    'vector<pair<edm::Ptr<pat::Muon>,TLorentzVector> >' 
        ) #muoni estrapolati (ENDCAP-)

    def isSameMu (self, mu1, mu2):
        if mu1.pt() == mu2.pt() and mu1.phi() == mu2.phi() and mu1.eta() == mu2.eta():
            return True
        else:
            return False
        
    def process(self, event):
        self.readCollections(event.input)
        
        muons      = [event.tau3mu.mu1(), event.tau3mu.mu2(), event.tau3mu.mu3()]
        #muons = self.cfg_ana.getter(event)
        self.counters.counter('L1TriggerAnalyzer').inc('all events')
        dRmax = 0.3
        if hasattr(self.cfg_ana, 'dR'):
            dRmax = self.cfg_ana.dR        
        event.dRmax = 10.*dRmax
        
        for mu in muons:
            mu.L1matches = []

        L1muons   = self.handles[Stage2L1ObjEnum.Muon].product()
        extMuonsBB= self.handles['extMuonsBB'].product()
        extMuonsEP= self.handles['extMuonsEP'].product()
        extMuonsEM= self.handles['extMuonsEM'].product()

        # match offline muons with extrap
        for mu in muons:
            listaBB=[]
            listaEP=[]
            listaEM=[]
            for i in range(extMuonsBB.size()):
                mBB = extMuonsBB[i].second; mBB.dP = abs(mBB.Pt()-mu.pt())
                mEP = extMuonsEP[i].second; mEP.dP = abs(mEP.Pt()-mu.pt())
                mEM = extMuonsEM[i].second; mEM.dP = abs(mEM.Pt()-mu.pt())                
                listaBB.append(mBB)
                listaEP.append(mEP)
                listaEM.append(mEM)
            listaBB.sort(key = lambda exm: exm.dP, reverse=False)
            listaEM.sort(key = lambda exm: exm.dP, reverse=False)
            listaEP.sort(key = lambda exm: exm.dP, reverse=False)
            mu.extBB = listaBB[0]
            mu.extEP = listaEP[0]
            mu.extEM = listaEM[0]
            
        allL1objects = []
        for i in range(L1muons.size(0)):
            l1 = L1muons.at(0, i)
            l1.bx    = 0                
            l1.index = i             
            link = 36 + int(l1.tfMuonIndex()/3.)
            if (36 <= link <=41) or (66<=link<=71):
                if l1.eta() < 0: l1.pos = -1  #endcap -
                if l1.eta() > 0: l1.pos = +1  #endcap +
            else: l1.pos = 0                  #barrel     
            allL1objects.append(l1)
        event.allL1objects = allL1objects
                    
        for mu, l1 in product(muons, allL1objects):
            if l1.pos == 0 : dR = deltaR(l1.eta(), l1.phi(), mu.extBB.Eta(), mu.extBB.Phi()); dPt = abs(l1.pt() - mu.extBB.Pt())  #barrel matching
            if l1.pos == -1: dR = deltaR(l1.eta(), l1.phi(), mu.extEM.Eta(), mu.extEM.Phi()); dPt = abs(l1.pt() - mu.extEM.Pt())  #endcap- matching
            if l1.pos == +1: dR = deltaR(l1.eta(), l1.phi(), mu.extEP.Eta(), mu.extEP.Phi()); dPt = abs(l1.pt() - mu.extEP.Pt())  #endcap+ matching
            myL1        = L1Candidate(l1)
            myL1.type   = Stage2L1ObjEnum.Muon 
            myL1.bx     = l1.bx
            myL1.dR     = dR   
            myL1.goodID = isinstance(l1, self.types[type(mu)])          
            if dR < dRmax:
                mu.L1matches.append(myL1)

        for mu in muons:
            if len(mu.L1matches):
                mu.L1matches.sort(key = lambda l1 : (l1.goodID, -l1.dR, l1.pt()), reverse = True)
                mu.L1 = mu.L1matches[0]

        return True                


setattr(L1TriggerAnalyzer, 'defaultConfig', 
    cfg.Analyzer(
        class_object=L1TriggerAnalyzer,
        getter = lambda event : [event.tau3muRefit.mu1(), event.tau3muRefit.mu2(), event.tau3muRefit.mu3()],
        dR=0.3
    )
)
