from CMGTools.WTau3Mu.analyzers.WTau3MuTreeProducerBase import WTau3MuTreeProducerBase

class WTau3MuTreeProducer(WTau3MuTreeProducerBase):

    '''
    '''

    def declareVariables(self, setup):
        '''
        '''
        self.bookEvent(self.tree)
        self.bookTriplet(self.tree, 'cand')
        self.bookMuon(self.tree, 'mu1')
        self.bookMuon(self.tree, 'mu2')
        self.bookMuon(self.tree, 'mu3')
        self.bookParticle(self.tree, 'met')
        self.bookVertex(self.tree, 'tau_sv')
        
    def process(self, event):
        '''
        '''
        self.readCollections(event.input)
        self.tree.reset()

        if not eval(self.skimFunction):
            return False

        self.fillEvent(self.tree, event)
        #import pdb ; pdb.set_trace()
        self.fillTriplet(self.tree, 'cand', event.tau3mu)
        self.fillMuon(self.tree, 'mu1', event.tau3mu.mu1())
        self.fillMuon(self.tree, 'mu2', event.tau3mu.mu2())
        self.fillMuon(self.tree, 'mu3', event.tau3mu.mu3())
        self.fillParticle(self.tree, 'met', event.tau3mu.met())

        if hasattr(event.tau3mu, 'refittedVertex') and event.tau3mu.refittedVertex is not None:
            self.fillVertex(self.tree, 'tau_sv', event.tau3mu.refittedVertex)

        self.fillTree(event)

