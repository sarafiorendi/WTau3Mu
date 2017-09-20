import ROOT
from itertools import product, combinations

from PhysicsTools.Heppy.analyzers.core.Analyzer   import Analyzer
from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle
from PhysicsTools.Heppy.physicsobjects.Muon       import Muon
from PhysicsTools.Heppy.physicsobjects.Electron   import Electron
from PhysicsTools.Heppy.physicsobjects.Tau        import Tau
from PhysicsTools.HeppyCore.utils.deltar          import deltaR, deltaR2

from CMGTools.WTau3Mu.physicsobjects.Tau3MuMET    import Tau3MuMET
from CMGTools.WTau3Mu.analyzers.resonances        import resonances, sigmas_to_exclude
from pdb import set_trace

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
        count.register('> 0 vertex')
        count.register('> 0 tri-muon')
        # count.register('pass resonance veto')
        count.register('m < 10 GeV')
        count.register('trigger matched')

    def buildMuons(self, muons, event):
        '''
        '''
        muons = map(Muon, muons)
        for mu in muons:
            mu.associatedVertex = event.vertices[0]
        muons = [mu for mu in muons if 
                 (mu.isSoftMuon(mu.associatedVertex) or mu.isLooseMuon()) and
                 mu.pt()>1. and
                 abs(mu.eta())<=2.5]          
        return muons

    def resonanceVeto(self, muons):
        pairs = [(i,j) for i, j in combinations(muons, 2) if (i.charge()+j.charge()) == 0]
        excluded = set()
        for rmass, rwidth, _ in resonances:
            for m1, m2 in pairs:
                if m1 in excluded or m2 in excluded: continue
                delta_mass = abs( (m1.p4()+m2.p4()).M() - rmass ) / rwidth
                if delta_mass < sigmas_to_exclude:
                    excluded.add(m1)
                    excluded.add(m2)
            pairs = [(i, j) for i, j in pairs if i not in excluded and j not in excluded]
        return list(set(muons) - excluded)

    def buildElectrons(self, electrons, event):
        '''
        Used for veto
        '''
        electrons = map(Electron, electrons)
        for ele in electrons:
            ele.associatedVertex = event.vertices[0]
#         if len(electrons):
#             import pdb ; pdb.set_trace()
        electrons = [ele for ele in electrons if
                     ele.pt()>10 and
                     abs(ele.eta())<2.5 and
                     # ele.mvaIDRun2('Spring16', 'Veto') and # why?
                     ele.mvaIDRun2('NonTrigSpring15MiniAOD', 'POG90') and
                     self.testVertex(ele) and
                     ele.passConversionVeto() and
                     ele.physObj.gsfTrack().hitPattern().numberOfHits(ROOT.reco.HitPattern.MISSING_INNER_HITS) <= 1 and
                     ele.relIsoR(R=0.3, dBetaFactor=0.5, allCharged=0) < 0.3]
        return electrons

    def buildTaus(self, taus, event):
        '''
        '''
        taus = map(Tau, taus)
        taus = [tau for tau in taus if 
                tau.tauID('decayModeFinding') > 0.5 and
                tau.tauID('byLooseIsolationMVArun2v1DBoldDMwLT') > 0.5 and
                tau.pt()>18. and
                abs(tau.eta())<2.3 and
                self.testTauVertex(tau)]
        return map(Tau, taus)
    
    def process(self, event):
        self.readCollections(event.input)

        if not len(event.vertices):
            return False

        self.counters.counter('Tau3Mu').inc('> 0 vertex')

        event.muons     = self.buildMuons    (self.handles['muons'    ].product(), event)
        event.electrons = self.buildElectrons(self.handles['electrons'].product(), event)
        event.taus      = self.buildTaus     (self.handles['taus'     ].product(), event)
        event.pfmet     = self.handles['pfmet'   ].product()[0]
        event.puppimet  = self.handles['puppimet'].product()[0]
        
        good = self.selectionSequence(event)
        
        return good

    def selectionSequence(self, event):

        self.counters.counter('Tau3Mu').inc('all events')

        if len(event.muons) < 3:
            return False

        self.counters.counter('Tau3Mu').inc('> 0 tri-muon')

        # event.muons = self.resonanceVeto(event.muons)

        # if len(event.muons) < 3:
        #     return False

        # self.counters.counter('Tau3Mu').inc('pass resonance veto')

        event.tau3mus = [Tau3MuMET(triplet, event.pfmet) for triplet in combinations(event.muons, 3)]

        # testing di-lepton itself
        seltau3mu = event.tau3mus

        # mass cut
        seltau3mu = [triplet for triplet in seltau3mu if triplet.massMuons() < 3.]

        if len(seltau3mu) == 0:
            return False
        self.counters.counter('Tau3Mu').inc('m < 10 GeV')

        # trigger matching
        # RM FIXME! for now it makes sense only if there's just one trigger
        if hasattr(self.cfg_ana, 'trigger_match') and self.cfg_ana.trigger_match:
            for triplet in seltau3mu:
                triplet.mu1().trig_objs = []
                triplet.mu2().trig_objs = []
                triplet.mu3().trig_objs = []
    
                triplet.mu1().trig_matched = False
                triplet.mu2().trig_matched = False
                triplet.mu3().trig_matched = False
    
                for info in event.trigger_infos:
                    triplet.mu1().trig_objs += [obj for obj in info.objects if deltaR(triplet.mu1(), obj)<0.3]
                    triplet.mu2().trig_objs += [obj for obj in info.objects if deltaR(triplet.mu2(), obj)<0.3]
                    triplet.mu3().trig_objs += [obj for obj in info.objects if deltaR(triplet.mu3(), obj)<0.3]
                
                # FIXME! cannot pickle properly
                self.cfg_comp.trigger_filters = [
                    (lambda triplet : triplet.mu1(), ['hltTau3muTkVertexFilter']),
                    (lambda triplet : triplet.mu2(), ['hltTau3muTkVertexFilter']),
                    (lambda triplet : triplet.mu3(), ['hltTau3muTkVertexFilter']),
                ]
                
                for getter, filters in self.cfg_comp.trigger_filters:
                    for obj in getter(triplet).trig_objs:
                        if set(filters) & set(obj.filterLabels()):
                            getter(triplet).trig_matched = True
            
            seltau3mu = [triplet for triplet in seltau3mu if triplet.mu1().trig_matched \
                         and triplet.mu2().trig_matched and triplet.mu3().trig_matched]
            if len(seltau3mu) == 0:
                return False
            self.counters.counter('Tau3Mu').inc('trigger matched')
        
        event.seltau3mu = seltau3mu

        event.tau3mu = self.bestTriplet(seltau3mu)


        return True


    def bestTriplet(self, triplets):
        '''
        The best triplet is the one with the correct charge and highest mT(3mu, MET). 
        If there are more than one triplets with the wrong charge, take the one with the highest  mT(3mu, MET).
        '''
        triplets.sort(key=lambda tt : (abs(tt.charge())==1, tt.mttau()), reverse=True)    
        return triplets[0]
    
    def testVertex(self, lepton):
        '''Tests vertex constraints, for mu'''
        return abs(lepton.dxy()) < 0.045 and abs(lepton.dz()) < 0.2
        
    def testTauVertex(self, tau):
        '''Tests vertex constraints, for tau'''
        # Just checks if the primary vertex the tau was reconstructed with
        # corresponds to the one used in the analysis
        # isPV = abs(tau.vertex().z() - tau.associatedVertex.z()) < 0.2
        isPV = abs(tau.leadChargedHadrCand().dz()) < 0.2
        return isPV

    
