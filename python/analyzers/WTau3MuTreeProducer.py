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
        self.bookMuon(self.tree, 'mu1_refit')
        self.bookMuon(self.tree, 'mu2_refit')
        self.bookMuon(self.tree, 'mu3_refit')        
        self.bookVertex(self.tree, 'tau_sv')

        # generator information
        self.bookGenParticle(self.tree, 'w')
        self.bookGenParticle(self.tree, 'mu1_refit_gen')
        self.bookGenParticle(self.tree, 'mu2_refit_gen')
        self.bookGenParticle(self.tree, 'mu3_refit_gen')
        self.bookGenParticle(self.tree, 'gentau')
        self.bookParticle(self.tree, 'genmet')

        # trigger information
        self.bookL1object(self.tree, 'mu1_L1')
        self.bookL1object(self.tree, 'mu2_L1')
        self.bookL1object(self.tree, 'mu3_L1')

        # BDT output
        self.var(self.tree, 'bdt_score')
        
    def process(self, event):
        '''
        '''
        self.readCollections(event.input)
        self.tree.reset()

        if not eval(self.skimFunction):
            return False

        self.fillEvent(self.tree, event)
        self.fillTriplet(self.tree, 'cand', event.tau3mu)
        
        self.fillTriplet(self.tree, 'cand', event.tau3mu)        
        self.fillMuon(self.tree, 'mu1', event.tau3mu.mu1())
        self.fillMuon(self.tree, 'mu2', event.tau3mu.mu2())
        self.fillMuon(self.tree, 'mu3', event.tau3mu.mu3())
        self.fillParticle(self.tree, 'met', event.tau3mu.met())

        self.fillTriplet(self.tree, 'cand_refit', event.tau3muRefit)
        self.fillMuon(self.tree, 'mu1_refit', event.tau3muRefit.mu1())
        self.fillMuon(self.tree, 'mu2_refit', event.tau3muRefit.mu2())
        self.fillMuon(self.tree, 'mu3_refit', event.tau3muRefit.mu3())

        if hasattr(event.tau3muRefit, 'refittedVertex') and event.tau3muRefit.refittedVertex is not None:
            self.fillVertex(self.tree, 'tau_sv', event.tau3muRefit.refittedVertex)

        # generator information
        if hasattr(event, 'genw') and event.genw is not None: 
            self.fillGenParticle(self.tree, 'w', event.genw)

        if hasattr(event.tau3muRefit.mu1(), 'genp') and event.tau3muRefit.mu1().genp is not None: 
            self.fillGenParticle(self.tree, 'mu1_refit_gen', event.tau3muRefit.mu1().genp)
        if hasattr(event.tau3muRefit.mu2(), 'genp') and event.tau3muRefit.mu2().genp is not None: 
            self.fillGenParticle(self.tree, 'mu2_refit_gen', event.tau3muRefit.mu2().genp)
        if hasattr(event.tau3muRefit.mu3(), 'genp') and event.tau3muRefit.mu3().genp is not None: 
            self.fillGenParticle(self.tree, 'mu3_refit_gen', event.tau3muRefit.mu3().genp)

        if hasattr(event, 'genmet') and event.genmet is not None: 
            self.fillParticle(self.tree, 'genmet', event.genmet)

        if hasattr(event, 'gentau') and event.gentau is not None: 
            self.fillParticle(self.tree, 'gentau', event.gentau)

        # trigger information
        if hasattr(event.tau3muRefit.mu1(), 'L1'):
            self.fillL1object(self.tree, 'mu1_L1', event.tau3muRefit.mu1().L1)
        if hasattr(event.tau3muRefit.mu2(), 'L1'):
            self.fillL1object(self.tree, 'mu2_L1', event.tau3muRefit.mu2().L1)
        if hasattr(event.tau3muRefit.mu3(), 'L1'):
            self.fillL1object(self.tree, 'mu3_L1', event.tau3muRefit.mu3().L1)

        # BDT output
        if hasattr(event, 'bdt'):
            self.fill(self.tree, 'bdt_score', event.bdt)
 
        self.fillTree(event)

