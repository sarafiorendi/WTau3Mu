from copy import deepcopy as dc
import ROOT

from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.HeppyCore.utils.deltar        import deltaR, bestMatch

class GenMatcherAnalyzer(Analyzer):
    '''
    '''
    def process(self, event):
        if event.input.eventAuxiliary().isRealData():
            return True
        
        # match the tau to gen tau
        tau3mu = self.cfg_ana.getter(event)
        tau = tau3mu.p4Muons()
        best_match, dRmin = bestMatch(tau, event.gentaus)
        tau_match = best_match if dRmin < 0.3 else None
                    
        muons = [tau3mu.mu1(), tau3mu.mu2(), tau3mu.mu3()]          
        
        # now match the three muons: 
        #    first try to match to any stable gen particle
        stableGenParticles = [pp for pp in event.genParticles if pp.status()==1]
        for mu in muons:
            best_match, dRmin = bestMatch(mu, stableGenParticles)
            if dRmin < 0.1:
                mu.genp = best_match
            
        #     then match to tau daughters
        #     but only if the reco tau is matched to a gen tau itself
        if tau_match:
            # append the gen tau to the event
            event.gentau = tau_match
            tau_daughters = self.finalDaughters(event.gentau)
            muons_from_tau = [mu for mu in tau_daughters if abs(mu.pdgId())==13]
            for mu in muons_from_tau:
                best_match, dRmin = bestMatch(mu, muons)
                if dRmin < 0.1:
                    best_match.genp = mu
            # check if the tau comes from a w
            tau_genw = [pp for pp in list(tau_match.motherRefVector()) if abs(pp.pdgId())==24]
            if tau_genw:
                event.genw = tau_genw[0]
        
        neutrinos = [pp for pp in event.genParticles if abs(pp.pdgId()) in [12, 14, 16] and pp.status()==1]
        
        for i, nn in enumerate(neutrinos):
            if i==0:
                event.genmet = nn.p4()
            else:
                event.genmet += nn.p4()

#         if not hasattr(muons[0], 'genp') or (hasattr(muons[0], 'genp') and abs(muons[0].genp.pdgId())!=13):
#             import pdb ; pdb.set_trace()

#         print '\n==========================================================================='
#         print bestMatch(tau, event.gentaus)
#         print tau.pt(), tau.eta(), tau.phi()
#         print event.gentaus[0].pt(), event.gentaus[0].eta(), event.gentaus[0].phi()
#         print ''
#         for mm in event.muons: print mm.pt(), mm.eta(), mm.phi(), mm.charge()
#         print ''
#         for mm in event.allmuons: print mm.pt(), mm.eta(), mm.phi(), mm.charge()
#         import pdb ; pdb.set_trace()
        
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
                GenMatcherAnalyzer.finalDaughters(daughter, daughters)
        return daughters



