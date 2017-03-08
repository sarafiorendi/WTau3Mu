from itertools import product, combinations

from PhysicsTools.Heppy.analyzers.core.Analyzer   import Analyzer
from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle
from PhysicsTools.Heppy.physicsobjects.Muon       import Muon
from PhysicsTools.Heppy.physicsobjects.Electron   import Electron
from PhysicsTools.Heppy.physicsobjects.Tau        import Tau
from PhysicsTools.HeppyCore.utils.deltar          import deltaR, deltaR2

from CMGTools.WTau3Mu.physicsobjects.Tau3MuMET    import Tau3MuMET

class Tau3MuAnalyzer(Analyzer):
    '''
    '''

    def declareHandles(self):
        super(Tau3MuAnalyzer, self).declareHandles()

        self.handles['taus'] = AutoHandle(
            'slimmedTaus',
            'std::vector<pat::Tau>'
        )

        self.handles['electrons'] = AutoHandle(
            'slimmedElectrons',
            'std::vector<pat::Electron>'
        )

        self.handles['muons'] = AutoHandle(
            'slimmedMuons',
            'std::vector<pat::Muon>'
        )

        self.mchandles['genParticles'] = AutoHandle(
            'prunedGenParticles',
            'std::vector<reco::GenParticle>'
        )

        self.handles['puppimet'] = AutoHandle(
            'slimmedMETsPuppi',
            'std::vector<pat::MET>'
        )

        self.handles['pfmet'] = AutoHandle(
            'slimmedMETs',
            'std::vector<pat::MET>'
        )


    def beginLoop(self, setup):
        super(Tau3MuAnalyzer, self).beginLoop(setup)
        self.counters.addCounter('Tau3Mu')
        count = self.counters.counter('Tau3Mu')
        count.register('all events')
        count.register('> 0 tri-muon')
#         count.register('fourth muon veto')
#         count.register('electron veto')
#         count.register('trig matched')
        count.register('m < 10 GeV')

    def buildMuons(self, muons, event):
        '''
        '''
        return map(Muon, muons)

    def buildElectrons(self, electrons, event):
        '''
        '''
        return map(Electron, electrons)

    def buildTaus(self, taus, event):
        '''
        '''
        return map(Tau, taus)
    
    def process(self, event):
        self.readCollections(event.input)

        event.muons     = self.buildMuons    (self.handles['muons'    ].product(), event)
        event.electrons = self.buildElectrons(self.handles['electrons'].product(), event)
        event.taus      = self.buildElectrons(self.handles['taus'     ].product(), event)
        event.pfmet     = self.handles['pfmet'   ].product()[0]
        event.puppimet  = self.handles['puppimet'].product()[0]

        for mu in event.muons:
            mu.associatedVertex = event.goodVertices[0]

        # to be implemented
        # event.vetoelectrons = [ele for ele in event.electrons if self.isVetoElectron(ele)]
        # event.vetotaus      = [tau for tau in event.taus      if self.isVetoTau(tau)     ]
        
        event.tau3mus = [Tau3MuMET(triplet, event.pfmet) for triplet in combinations(event.muons, 3)]

        good = self.selectionSequence(event)
            
        return good

    def selectionSequence(self, event):

        self.counters.counter('Tau3Mu').inc('all events')

        if len(event.muons) < 3:
            return False

        self.counters.counter('Tau3Mu').inc('> 0 tri-muon')

        # testing di-lepton itself
        seltau3mu = event.tau3mus

        # mass cut
        seltau3mu = [triplet for triplet in seltau3mu if triplet.massMuons() < 10.]
        
        if len(seltau3mu) == 0:
            return False
        self.counters.counter('Tau3Mu').inc('m < 10 GeV')

        event.seltau3mu = seltau3mu

        event.tau3mu = self.bestTriplet(seltau3mu)

        return True


    def bestTriplet(self, triplets):
        '''
        The best triplet is the one with the correct charge and highest mT(3mu, MET). 
        If there are more than one triplets with the wrong charge, take the one with the highest  mT(3mu, MET).
        '''
        #if len(triplets) > 1: 
        #    import pdb ; pdb.set_trace()
        triplets.sort(key=lambda tt : (abs(tt.mu1().charge() + tt.mu2().charge() + tt.mu3().charge())==1 * tt.mttau()) - (abs(tt.mu1().charge() + tt.mu2().charge() + tt.mu3().charge())!=1 / max(tt.mttau(), 1.e-12)), reverse=True )
        return triplets[0]
    
    