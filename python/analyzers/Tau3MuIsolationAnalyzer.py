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


    def declareHandles(self):
        super(Tau3MuIsolationAnalyzer, self).declareHandles()
       
        self.handles['pf'] = AutoHandle(
            'packedPFCandidates', 
            'std::vector<pat::PackedCandidate>'
        )
       
        self.dBetaCone  = self.cfg_ana.dBetaCone  if hasattr(self.cfg_ana, 'dBetaCone')  else 0.8
        self.dBetaValue = self.cfg_ana.dBetaValue if hasattr(self.cfg_ana, 'dBetaValue') else 0.2       
        self.isoRadius  = self.cfg_ana.isoRadius  if hasattr(self.cfg_ana, 'isoRadius')  else 0.4       

        # instantiate the isolation computer (by default with delta beta cone 0.8)
        self.IsolationComputer = heppy.IsolationComputer(self.dBetaCone) # keyword arguments not supported, sigh...

    def attachTauIsolation(self, tau):
        '''
        check PhysicsTools/Heppy/interface/IsolationComputer.h
        Not sure everythin is consistent at the moment...
        '''
        tau.absChargedFromPV  = self.IsolationComputer.chargedAbsIso        (tau, self.isoRadius) # already muon subtracted
        tau.absChargedFromPU  = self.IsolationComputer.puAbsIso             (tau, self.dBetaCone)
        tau.absPhotonRaw      = self.IsolationComputer.photonAbsIsoRaw      (tau, self.dBetaCone)

#     # useful to understand the heppy code
#     def altAttachTauIsolation(self, tau, pf_cands):
# 
#         tau.altAbsChargedFromPV = sum([pf.pt() for pf in pf_cands if deltaR(tau, pf)<self.isoRadius and pf.charge()!=0 and pf.fromPV()>1]   ) # check pv condition...
#         tau.altAbsChargedFromPU = sum([pf.pt() for pf in pf_cands if deltaR(tau, pf)<self.dBetaCone and pf.charge()!=0 and abs(pf.dz())>0.2]) # check pv condition...
#         tau.altAbsPhotonRaw     = sum([pf.pt() for pf in pf_cands if deltaR(tau, pf)<self.dBetaCone and pf.pdgId()==22]                     )
        

    def process(self, event):
        self.readCollections(event.input)

        pf_cands = self.handles['pf'].product()
        self.IsolationComputer.setPackedCandidates(pf_cands)

        muons = [event.tau3mu.mu1(), event.tau3mu.mu2(), event.tau3mu.mu3()]
        
        tau_charge = sum([mu.charge() for mu in muons])
        tau_lvP4   = event.tau3mu.p4Muons()
        tau_vtx    = event.tau3mu.refittedVertex.position() if hasattr(event.tau3mu, 'refittedVertex') else None
        tau_pdg    = (tau_charge>0) * 15 - (tau_charge<0) * 15
                
        tau = ROOT.reco.RecoChargedCandidate( tau_charge, tau_lvP4, tau_vtx, tau_pdg) 

        # compute and attach the different isolation components
        self.attachTauIsolation(tau)
#         self.altAttachTauIsolation(tau, pf_cands)

#         # remove muons from charged isolation
#         muonSumPt = sum([mu.pt() for mu in muons if deltaR(tau, mu)<self.isoRadius])
        
#         tau.absChargedFromPVnoMuons = tau.absChargedFromPV - (muonSumPt>0)*muonSumPt

        # compute delta beta isolation
        dBetaIso = tau.absChargedFromPV + max(0., tau.absPhotonRaw - self.dBetaValue * tau.absChargedFromPU)

#         import pdb ; pdb.set_trace()

        # attach isolation to the to tau3mu object
        setattr(event.tau3mu, 'tau_dBetaIsoCone%sstrength%s_abs' %(str(self.dBetaCone).replace('.','p'), str(self.dBetaValue).replace('.','p')), dBetaIso)
        setattr(event.tau3mu, 'tau_dBetaIsoCone%sstrength%s_rel' %(str(self.dBetaCone).replace('.','p'), str(self.dBetaValue).replace('.','p')), dBetaIso/tau.pt())

        #import pdb ; pdb.set_trace()

        return True
        


