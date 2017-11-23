from copy import deepcopy as dc
import ROOT

from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.HeppyCore.utils.deltar        import deltaR, bestMatch

from CMGTools.WTau3Mu.physicsobjects.DsPhiMuMuPi  import DsPhiMuMuPi

class DsPhiMuMuPiGenMatcherAnalyzer(Analyzer):
    '''
    '''
    def process(self, event):
        if event.input.eventAuxiliary().isRealData():
            return True
        
        # match the ds to gen ds
        dsphimumupi = self.cfg_ana.getter(event)
        
        # get all Ds in the event
        gends = [pp for pp in event.genParticles if abs(pp.pdgId())==431]
        
        # restrict to only those that decay into phi pi
        gends = [pp for pp in gends if pp.numberOfDaughters()==2 and (len(set([333, 211]) & set([abs(pp.daughter(0).pdgId()), abs(pp.daughter(1).pdgId())]))==2)]
        
        # append to the event the gen level Ds Phi Mu Mu Phi with the highest momentum
        gends.sort(key = lambda x : x.pt(), reverse=True)
        mygends = gends[0]  
        mygends.phip = [dau for dau in [mygends.daughter(ii)      for ii in range(mygends.numberOfDaughters())     ] if abs(dau.pdgId())==333][0]  
        mygends.pi   = [dau for dau in [mygends.daughter(ii)      for ii in range(mygends.numberOfDaughters())     ] if abs(dau.pdgId())==211][0]  
        mygends.mum  = [mu  for mu  in [mygends.phip.daughter(ii) for ii in range(mygends.phip.numberOfDaughters())] if     mu .pdgId() == 13][0]  
        mygends.mup  = [mu  for mu  in [mygends.phip.daughter(ii) for ii in range(mygends.phip.numberOfDaughters())] if     mu .pdgId() ==-13][0]  
        event.gends  = DsPhiMuMuPi([mygends.mum, mygends.mup], mygends.pi)
        event.ngends = len(gends)
                
        # match the reco candidate to the gen Ds
        best_match, dRmin = bestMatch(dsphimumupi, gends)
        ds_match = best_match if dRmin < 0.3 else None
        if ds_match:
            ds_match.phip = [pp for pp in [ds_match.daughter(0), ds_match.daughter(1)] if pp.pdgId()==333][0]
                    
        muons = [dsphimumupi.mu1(), dsphimumupi.mu2()]          
        
        # now match the two muons and the pion: 
        #    first try to match to any stable gen particle
        stableGenParticles = [pp for pp in event.genParticles if pp.status()==1]
        for mu in muons + [dsphimumupi.pi()]:
            best_match, dRmin = bestMatch(mu, stableGenParticles)
            if dRmin < 0.1:
                mu.genp = best_match
            
        #     then match to phi daughters
        #     but only if the reco ds is matched to a gen ds itself
        if ds_match:
            # append the gen ds to the event
            event.ds.genp = ds_match
            muons_from_phi = [mu for mu in [ds_match.phip.daughter(ii) for ii in range(ds_match.phip.numberOfDaughters())] if abs(mu.pdgId())==13]
            for mu in muons_from_phi:
                best_match, dRmin = bestMatch(mu, muons)
                if dRmin < 0.1:
                    best_match.genp = mu
        
        neutrinos = [pp for pp in event.genParticles if abs(pp.pdgId()) in [12, 14, 16] and pp.status()==1]
        
        for i, nn in enumerate(neutrinos):
            if i==0:
                event.genmet = nn.p4()
            else:
                event.genmet += nn.p4()
        
        return True
    
    @staticmethod
    def finalDaughters(gen, daughters=None):
        if daughters is None:
            daughters = []
        for i in range(gen.numberOfDaughters()):
            daughter = gen.daughter(i)
            if daughter.numberOfDaughters() == 0:
                daughters.append(daughter)
            else:
                DsPhiMuMuPiGenMatcherAnalyzer.finalDaughters(daughter, daughters)
        return daughters



