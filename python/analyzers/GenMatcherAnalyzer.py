import ROOT

from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.HeppyCore.utils.deltar        import deltaR, bestMatch

class GenMatcherAnalyzer(Analyzer):
    '''
    '''
    def process(self, event):
        if event.input.eventAuxiliary().isRealData():
            return True
        
        # match the refitted tau to gen tau
        tau = event.tau3muRefit.p4Muons()
        best_match, dRmin = bestMatch(tau, event.gentaus)
        tau_match = best_match if dRmin < 0.3 else None
                    
        muons = [event.tau3muRefit.mu1(), event.tau3muRefit.mu2(), event.tau3muRefit.mu3()]          
        
        # now match the three muons: 
        #    first try to match to any stable gen particle
        stableGenParticles = [pp for pp in event.genParticles if pp.status()==2]
        for mu in muons:
            best_match, dRmin = bestMatch(mu, stableGenParticles)
            if dRmin < 0.1:
                mu.genp = best_match
            
        #     then match to tau daughters
        #     but only if the reco tau is matched to a gen tau itself
        if tau_match:
            # append the gen tau to the event
            event.gentau = tau_match
            tau_daughters = list(tau_match.daughterRefVector())
            for mu in muons:
                best_match, dRmin = bestMatch(mu, tau_daughters)
                if dRmin < 0.1:
                    mu.genp = best_match
            # check if the tau comes from a w
            tau_genw = [pp for pp in list(tau_match.motherRefVector()) if abs(pp.pdgId())==24]
            if tau_genw:
                event.genw = tau_genw[0]
        
        neutrinos = [pp for pp in event.genParticles if abs(pp.pdgId()) in [12, 14, 16]]
        
        for i, nn in enumerate(neutrinos):
            if i==0:
                event.genmet = nn.p4()
            else:
                event.genmet += nn.p4()

#         import pdb ; pdb.set_trace()
        
        return True




