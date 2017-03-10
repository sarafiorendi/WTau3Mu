from CMGTools.WTau3Mu.analyzers.WTau3MuTreeProducerBase import WTau3MuTreeProducerBase


class WTau3MuTreeProducer(WTau3MuTreeProducerBase):

    '''
    '''

    def declareVariables(self, setup):
        '''
        '''
        self.bookEvent(self.tree)
        self.bookTriplet(self.tree, 'cand')
        self.bookTriplet(self.tree, 'cand_refit')
        self.bookMuon(self.tree, 'mu1')
        self.bookMuon(self.tree, 'mu2')
        self.bookMuon(self.tree, 'mu3')
        self.bookParticle(self.tree, 'met')
        self.bookParticle(self.tree, 'tau_refit')
        self.bookParticle(self.tree, 'mu1_refit')
        self.bookParticle(self.tree, 'mu2_refit')
        self.bookParticle(self.tree, 'mu3_refit')        
        self.bookVertex(self.tree, 'tau_sv')
        
    def process(self, event):
        '''
        '''
        self.readCollections(event.input)
        self.tree.reset()

        if not eval(self.skimFunction):
            return False

        self.fillEvent(self.tree, event)
        self.fillTriplet(self.tree, 'cand', event.tau3mu)
        
        # very, very many nasty things, all because the tau3mu object needs to be updated wisely   
        if hasattr(event, 'tau3muRefit'):
            self.fillTriplet(self.tree, 'cand_refit', event.tau3muRefit)
            mu1 = event.tau3muRefit.mu1p4_
            mu1.charge = event.tau3muRefit.mu1().charge()
            mu2 = event.tau3muRefit.mu2p4_
            mu2.charge = event.tau3muRefit.mu2().charge()
            mu3 = event.tau3muRefit.mu3p4_
            mu3.charge = event.tau3muRefit.mu3().charge()
            tau = event.tau3muRefit.p4Muons()
            tau.charge = mu1.charge + mu2.charge + mu3.charge
            self.fillParticle(self.tree, 'tau_refit', tau)
            self.fillParticle(self.tree, 'mu1_refit', mu1)
            self.fillParticle(self.tree, 'mu2_refit', mu2)
            self.fillParticle(self.tree, 'mu3_refit', mu3)

        self.fillTriplet(self.tree, 'cand', event.tau3mu)
        
        event.tau3mu.mu1().charge = event.tau3mu.mu1().charge()  # this sucks
        event.tau3mu.mu2().charge = event.tau3mu.mu2().charge()  # this sucks
        event.tau3mu.mu3().charge = event.tau3mu.mu3().charge()  # this sucks
        event.tau3mu.met().charge = 0                            # this sucks
        
        self.fillMuon(self.tree, 'mu1', event.tau3mu.mu1())
        self.fillMuon(self.tree, 'mu2', event.tau3mu.mu2())
        self.fillMuon(self.tree, 'mu3', event.tau3mu.mu3())
        self.fillParticle(self.tree, 'met', event.tau3mu.met())

        if hasattr(event.tau3mu, 'refittedVertex') and event.tau3mu.refittedVertex is not None:
            self.fillVertex(self.tree, 'tau_sv', event.tau3mu.refittedVertex)

        self.fillTree(event)

