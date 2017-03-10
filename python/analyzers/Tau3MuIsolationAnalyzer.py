import ROOT
from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle
from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer

from PhysicsTools.HeppyCore.utils.deltar import deltaR

from ROOT import heppy


class Tau3MuIsolationAnalyzer(Analyzer):

    '''
    '''

    def __init__(self, cfg_ana, cfg_comp, looperName):
        super(Tau3MuIsolationAnalyzer, self).__init__(cfg_ana, cfg_comp, looperName)
        self.dBetaCone  = self.cfg_ana.dBetaCone  if hasattr(self.cfg_ana, 'dBetaCone')  else 0.8
        self.dBetaValue = self.cfg_ana.dBetaValue if hasattr(self.cfg_ana, 'dBetaValue') else 0.2       
        self.isoRadius  = self.cfg_ana.isoRadius  if hasattr(self.cfg_ana, 'isoRadius')  else 0.4       

        # instantiate the isolation computer (by default with delta beta cone 0.8)
        self.IsolationComputer = heppy.IsolationComputer(self.dBetaCone) # keyword arguments not supported, sigh...


    def declareHandles(self):
        super(Tau3MuIsolationAnalyzer, self).declareHandles()
       
        self.handles['pf'] = AutoHandle(
            'packedPFCandidates', 
            'std::vector<pat::PackedCandidate>'
        )
       
    def attachTauIsolation(self, tau):
        '''
        check PhysicsTools/Heppy/interface/IsolationComputer.h
        Not sure everythin is consistent at the moment...
        '''
        tau.absChargedFromPV  = self.IsolationComputer.chargedAbsIso        (tau, self.isoRadius) # already muon subtracted
        tau.absChargedFromPU  = self.IsolationComputer.puAbsIso             (tau, self.dBetaCone)
        tau.absPhotonRaw      = self.IsolationComputer.photonAbsIsoRaw      (tau, self.dBetaCone)
        

    def process(self, event):
        self.readCollections(event.input)

        pf_cands = self.handles['pf'].product()
        self.IsolationComputer.setPackedCandidates(pf_cands)

        # if there's a refitted candidate, use it
        if hasattr(event, 'tau3muRefit'):
            candidate = event.tau3muRefit
        else:
            candidate = event.tau3mu

        muons = [candidate.mu1(), candidate.mu2(), candidate.mu3()]
        
        tau_charge = sum([mu.charge() for mu in muons])
        tau_lvP4   = candidate.p4Muons()
        tau_vtx    = candidate.refittedVertex.position() if hasattr(event.tau3mu, 'refittedVertex') else None
        tau_pdg    = (tau_charge>0) * 15 - (tau_charge<0) * 15
                
        tau = ROOT.reco.RecoChargedCandidate( tau_charge, tau_lvP4, tau_vtx, tau_pdg) 

        # compute and attach the different isolation components
        self.attachTauIsolation(tau)

        # compute delta beta isolation
        dBetaIso = tau.absChargedFromPV + max(0., tau.absPhotonRaw - self.dBetaValue * tau.absChargedFromPU)

        # attach isolation to the to tau3mu object
        setattr(event.tau3mu, 'tau_dBetaIsoCone%sstrength%s_abs' %(str(self.dBetaCone).replace('.','p'), str(self.dBetaValue).replace('.','p')), dBetaIso)
        setattr(event.tau3mu, 'tau_dBetaIsoCone%sstrength%s_rel' %(str(self.dBetaCone).replace('.','p'), str(self.dBetaValue).replace('.','p')), dBetaIso/tau.pt())

        return True
        


