import ROOT
from CMGTools.WTau3Mu.analyzers.DsPhiMuMuPiTreeProducerBase import DsPhiMuMuPiTreeProducerBase
from PhysicsTools.HeppyCore.utils.deltar import deltaR

global muon_mass
muon_mass = 0.1056583745

class DsPhiMuMuPiTreeProducer(DsPhiMuMuPiTreeProducerBase):

    '''
    '''

    def declareVariables(self, setup):
        '''
        '''
        self.bookEvent(self.tree)
        self.bookDs(self.tree, 'ds')
        self.bookMuon(self.tree, 'mu1')
        self.bookMuon(self.tree, 'mu2')
        self.bookChargedCandidate(self.tree, 'pi')

        self.bookDs(self.tree, 'ds_refit')
        self.bookMuon(self.tree, 'mu1_refit')
        self.bookMuon(self.tree, 'mu2_refit')
        self.bookChargedCandidate(self.tree, 'pi_refit')
        self.bookVertex(self.tree, 'sv')

        # generator information
        self.bookGenParticle(self.tree, 'ds_gen')
        self.bookGenParticle(self.tree, 'ds_phi_gen')
        self.bookGenParticle(self.tree, 'mu1_gen')
        self.bookGenParticle(self.tree, 'mu2_gen')
        self.bookGenParticle(self.tree, 'pi_gen')
        self.bookParticle(self.tree, 'gen_met')
        self.bookDs(self.tree, 'gen_ds')
        self.bookParticle(self.tree, 'gen_ds_mu1')
        self.bookParticle(self.tree, 'gen_ds_mu2')
        self.bookParticle(self.tree, 'gen_ds_pi' )
        self.var(self.tree, 'n_gen_ds')

        self.var(self.tree, 'hlt_doublemu3_trk_tau3mu')

    def process(self, event):
        '''
        '''
        self.readCollections(event.input)
        self.tree.reset()

        if not eval(self.skimFunction):
            return False

        self.fillEvent(self.tree, event)
        
        self.fillDs(self.tree, 'ds', event.ds)        
        self.fillMuon(self.tree, 'mu1', event.ds.mu1())
        self.fillMuon(self.tree, 'mu2', event.ds.mu2())
        self.fillChargedCandidate(self.tree, 'pi', event.ds.pi())

        self.fillDs(self.tree, 'ds_refit', event.dsRefit)        
        self.fillMuon(self.tree, 'mu1_refit', event.dsRefit.mu1())
        self.fillMuon(self.tree, 'mu2_refit', event.dsRefit.mu2())
        self.fillChargedCandidate(self.tree, 'pi_refit', event.dsRefit.pi())

        self.fillVertex(self.tree, 'sv', event.dsRefit.refittedVertex)

        if hasattr(event.ds, 'genp'):
            self.fillGenParticle(self.tree, 'ds_gen'    , event.ds.genp     )
            self.fillGenParticle(self.tree, 'ds_phi_gen', event.ds.genp.phip)
        if hasattr(event.ds.mu1(), 'genp'):
            self.fillGenParticle(self.tree, 'mu1_gen', event.ds.mu1().genp)
        if hasattr(event.ds.mu2(), 'genp'):
            self.fillGenParticle(self.tree, 'mu2_gen', event.ds.mu2().genp)
        if hasattr(event.ds.pi(), 'genp'):
            self.fillGenParticle(self.tree, 'pi_gen', event.ds.pi().genp)
        if hasattr(event, 'genmet') and event.genmet is not None: 
            self.fillParticle(self.tree, 'gen_met', event.genmet)
        if hasattr(event, 'gends') and event.gends is not None: 
            self.fillDs(self.tree, 'gen_ds', event.gends)
            self.fillParticle(self.tree, 'gen_ds_mu1', event.gends.mu1())
            self.fillParticle(self.tree, 'gen_ds_mu2', event.gends.mu2())
            self.fillParticle(self.tree, 'gen_ds_pi' , event.gends.pi())
            self.fill(self.tree, 'n_gen_ds', event.ngends)
        
        # HLT bits & matches
        
        # 2016 data can be efficiently trigger matched, 2017 MC has a problem with unpackFilterLabels
        if event.input.eventAuxiliary().isRealData():
            self.fill(self.tree, 'hlt_doublemu3_trk_tau3mu', any('HLT_DoubleMu3_Trk_Tau3mu' in name for name in event.ds.hltmatched))

        else:
            # matching is broken here, revert back to simple trigger being fired or not
            fired_triggers = [info.name for info in getattr(event, 'trigger_infos', []) if info.fired]
            self.fill(self.tree, 'hlt_doublemu3_trk_tau3mu', any('HLT_DoubleMu3_Trk_Tau3mu' in name for name in fired_triggers))

#         import pdb ; pdb.set_trace()
        
        self.fillTree(event)

