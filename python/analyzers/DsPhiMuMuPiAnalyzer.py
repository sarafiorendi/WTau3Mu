import ROOT
from itertools import product, combinations

from PhysicsTools.Heppy.analyzers.core.Analyzer   import Analyzer
from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle
from PhysicsTools.Heppy.physicsobjects.Muon       import Muon
from PhysicsTools.HeppyCore.utils.deltar          import deltaR, deltaR2

from CMGTools.WTau3Mu.physicsobjects.DsPhiMuMuPi  import DsPhiMuMuPi
from CMGTools.WTau3Mu.analyzers.resonances        import resonances, sigmas_to_exclude
from pdb import set_trace

global m_pi  ; m_pi  = 0.13957061 # GeV

class DsPhiMuMuPiAnalyzer(Analyzer):
    '''
    '''

    def declareHandles(self):
        super(DsPhiMuMuPiAnalyzer, self).declareHandles()

        self.handles['muons'] = AutoHandle(
            'slimmedMuons',
            'std::vector<pat::Muon>'
        )

        self.mchandles['genParticles'] = AutoHandle(
            'prunedGenParticles',
            'std::vector<reco::GenParticle>'
        )

        self.handles['losttracks'] = AutoHandle(
            'lostTracks',
            'std::vector<pat::PackedCandidate>'
        )

        self.handles['pfcands'] = AutoHandle(
            'packedPFCandidates',
            'std::vector<pat::PackedCandidate>'
        )


    def beginLoop(self, setup):
        super(DsPhiMuMuPiAnalyzer, self).beginLoop(setup)
        self.counters.addCounter('DsPhiMuMuPi')
        count = self.counters.counter('DsPhiMuMuPi')
        count.register('all events')
        count.register('> 0 vertex')
        count.register('> 0 di-muon')
        count.register('> 0 opposite sign di-muon')
        count.register('> 0 di-muon pair with mass < 2 GeV')
        count.register('> 0 non degenerate Ds')
        count.register('1.6 < Ds mass < 2.2 GeV')
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
    
    def process(self, event):
        self.readCollections(event.input)

        if not len(event.vertices):
            return False

        self.counters.counter('DsPhiMuMuPi').inc('> 0 vertex')

        # build muons
        event.allmuons   =                 self.handles['muons'].product()
        event.muons      = self.buildMuons(self.handles['muons'].product(), event)
        event.vetomuons  = [mu for mu in event.muons if mu.isMediumMuon()] # needed for track-muon cross cleaning

        # build tracks
        event.allpf      = list(self.handles['pfcands'   ].product())
        event.losttracks = list(self.handles['losttracks'].product())
        # merge the track collections
        event.alltracks      = sorted([tt for tt in event.allpf + event.losttracks if tt.charge() != 0], key = lambda x : x.pt(), reverse = True)
        # select tracks byt pt, eta
        event.selectedtracks = [tt for tt in event.alltracks if tt.pt()>1 and abs(tt.eta())<2.5 and abs(tt.vz() - event.vertices[0].z()) < 0.3]
        # set pion mass
        for track in event.selectedtracks:
             track.setMass(m_pi)
                
        event.selectedLeptons = [lep for lep in event.muons if lep.pt()>10.] #+ event.taus # useful for jet cross cleaning

        # here you need to clean from selected leptons!
        toclean = []
        for tt in event.selectedtracks:
            for mm in event.vetomuons:
                if deltaR2(tt, mm) < 0.001:
                    toclean.append(tt)
        
        event.selectedtracks = [tt for tt in event.selectedtracks if tt not in toclean]

        good = self.selectionSequence(event)

        return good

    def selectionSequence(self, event):

        self.counters.counter('DsPhiMuMuPi').inc('all events')

        # at least 2 muons
        if len(event.muons) < 2:
            return False

        self.counters.counter('DsPhiMuMuPi').inc('> 0 di-muon')

        # at least 1 opposite sign muon pair
        mupairs = combinations(event.muons, 2)
        osmupairs = [[mu1, mu2] for mu1, mu2 in mupairs if mu1.charge()*mu2.charge()<0]
        if len(osmupairs) < 1:
            return False

        self.counters.counter('DsPhiMuMuPi').inc('> 0 opposite sign di-muon')

        # muon pair mass not too far from that of the phi
        osmupairs = [[mu1, mu2] for mu1, mu2 in osmupairs if (mu1.p4() + mu2.p4()).mass() < 2]
        if len(osmupairs) < 1:
            return False

        self.counters.counter('DsPhiMuMuPi').inc('> 0 di-muon pair with mass < 2 GeV')

        # create all Ds Phi(MuMu) Pi candidates, make sure the same object is not
        # picked up twice as track and as muon
        event.dsphipis = [DsPhiMuMuPi(dimuon, pi) for dimuon, pi in product(osmupairs, event.selectedtracks) if \
                            (deltaR(dimuon[0], pi)>0.01 and deltaR(dimuon[1], pi)>0.01)]

        if len(event.dsphipis) == 0:
            return False

        self.counters.counter('DsPhiMuMuPi').inc('> 0 non degenerate Ds')

        # mass cut on Ds Phi(MuMu) Pi
        event.dsphipis = [ds for ds in event.dsphipis if ds.p4().mass()>1.6 and ds.p4().mass()<2.2]
        if len(event.dsphipis) == 0:
            return False

        self.counters.counter('DsPhiMuMuPi').inc('1.6 < Ds mass < 2.2 GeV')

        # match only if the trigger fired
        event.fired_triggers = [info.name for info in getattr(event, 'trigger_infos', []) if info.fired]

        # trigger matching
        for ds in event.dsphipis:
             ds.hltmatched = []
             
        if hasattr(self.cfg_ana, 'trigger_match') and len(self.cfg_ana.trigger_match.keys())>0:
                        
            for ds in event.dsphipis:
                
                ds.hltmatched = [] # initialise to no match
                
                ds.mu1().trig_objs = [] # initialise to no trigger objct matches
                ds.mu2().trig_objs = [] # initialise to no trigger objct matches
                ds.pi ().trig_objs = [] # initialise to no trigger objct matches
    
                ds.mu1().trig_matched = False # initialise to no match
                ds.mu2().trig_matched = False # initialise to no match
                ds.pi ().trig_matched = False # initialise to no match
    
                # add all matched objects to each muon
                for info in event.trigger_infos:
                    ds.mu1().trig_objs += [obj for obj in info.objects if deltaR(ds.mu1(), obj)<0.3]
                    ds.mu2().trig_objs += [obj for obj in info.objects if deltaR(ds.mu2(), obj)<0.3]
                    ds.pi ().trig_objs += [obj for obj in info.objects if deltaR(ds.pi (), obj)<0.3]
                
                # iterate over the path:filters dictionary
                #     the filters MUST be sorted correctly: i.e. first filter in the dictionary 
                #     goes with the first muons and so on
                for k, v in self.cfg_ana.trigger_match.iteritems():

                    if not any(k in name for name in event.fired_triggers):
                         continue
                         
                    trigger_filters = []

                    if len(v)>0: trigger_filters.append( (lambda ds : getattr(ds, 'mu1')(), [v[0]]) )
                    if len(v)>1: trigger_filters.append( (lambda ds : getattr(ds, 'mu2')(), [v[1]]) )
                    if len(v)>2: trigger_filters.append( (lambda ds : getattr(ds, 'pi' )(), [v[2]]) )
                
                    for getter, filters in trigger_filters:
                        for obj in getter(ds).trig_objs:
                            if set(filters) & set(obj.filterLabels()):
                                getter(ds).trig_matched = True

                    ismatched = sum([int(jj.trig_matched) for jj in [ds.mu1(), ds.mu2(), ds.pi()]])            
            
                    if len(trigger_filters) == ismatched:
                        ds.hltmatched.append(k)
                        
            event.dsphipismatched = [ds for ds in event.dsphipis if len(ds.hltmatched)>0]
            
            if not self.cfg_ana.trigger_flag:
                event.dsphipis = event.dsphipismatched
            
            if len(event.dsphipis) == 0:
                return False
            
            self.counters.counter('DsPhiMuMuPi').inc('trigger matched')
        
        event.ds = self.bestDs(event.dsphipis)

        return True

    def bestDs(self, dss):
        '''
        The best Ds is the one with the higher pT.
        '''
        dss.sort(key=lambda ds : ds.pt(), reverse=True)    
        return dss[0]
    
    def testVertex(self, lepton):
        '''Tests vertex constraints, for mu'''
        return abs(lepton.dxy()) < 0.045 and abs(lepton.dz()) < 0.2
