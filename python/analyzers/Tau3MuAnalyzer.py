import ROOT
from itertools import product, combinations
import math
import numpy as np
from collections import OrderedDict, Counter

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

        self.handles['mvamets'] = AutoHandle(
            ('MVAMET', 'MVAMET', 'MVAMET'),
            'std::vector<pat::MET>',
            mayFail = True # not guaranteed MVA MET is always available
        )

    def beginLoop(self, setup):
        super(Tau3MuAnalyzer, self).beginLoop(setup)
        self.counters.addCounter('Tau3Mu')
        count = self.counters.counter('Tau3Mu')
        count.register('all events')
        count.register('> 0 vertex')
        count.register('> 0 tri-muon')
        # count.register('pass resonance veto')
        count.register('m < 3 GeV')
        count.register('pass (mu, mu, mu) Z cut')
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

        event.allmuons  =                     self.handles['muons'    ].product()
        event.muons     = self.buildMuons    (self.handles['muons'    ].product(), event)
        event.electrons = self.buildElectrons(self.handles['electrons'].product(), event)
        event.taus      = self.buildTaus     (self.handles['taus'     ].product(), event)
        event.pfmet     = self.handles['pfmet'   ].product()[0]
        event.puppimet  = self.handles['puppimet'].product()[0]
        if getattr(self.cfg_ana, 'useMVAmet', False):
            event.mvamets  = self.handles['mvamets'].product()
        
        good = self.selectionSequence(event)
        
        event.selectedLeptons = [lep for lep in event.muons + event.electrons if lep.pt()>10.] #+ event.taus # useful for jet cross cleaning

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

        if getattr(self.cfg_ana, 'useMVAmet', False):
            event.tau3mus = [Tau3MuMET(triplet, event.mvamets, useMVAmet=True) for triplet in combinations(event.muons, 3)]
        else:
            event.tau3mus = [Tau3MuMET(triplet, event.pfmet) for triplet in combinations(event.muons, 3)]

        # testing di-lepton itself
        seltau3mu = event.tau3mus

        # mass cut
        seltau3mu = [triplet for triplet in seltau3mu if triplet.massMuons() < 3.]

        if len(seltau3mu) == 0:
            return False
        self.counters.counter('Tau3Mu').inc('m < 3 GeV')

        # z vertex compatibility among mu mu pi
        dzsigmacut = getattr(self.cfg_ana, 'dz_sigma_cut', 5) # 5 sigma compatibility, pretty loose, but fwd tracks back pointing is pretty loose, innit?
        
        seltau3mu_tmp = []
        
        for tt in seltau3mu:
        
            tt.dzcompatibility12 = np.float64(abs(tt.mu1().dz()-tt.mu2().dz())) / math.sqrt(tt.mu1().dzError()**2 + tt.mu2().dzError()**2)
            tt.dzcompatibility13 = np.float64(abs(tt.mu1().dz()-tt.mu3().dz())) / math.sqrt(tt.mu1().dzError()**2 + tt.mu3().dzError()**2)
            tt.dzcompatibility23 = np.float64(abs(tt.mu2().dz()-tt.mu3().dz())) / math.sqrt(tt.mu2().dzError()**2 + tt.mu3().dzError()**2)
            
            if tt.dzcompatibility12 < dzsigmacut and \
               tt.dzcompatibility13 < dzsigmacut and \
               tt.dzcompatibility23 < dzsigmacut :

                seltau3mu_tmp.append(tt)            

        seltau3mu = seltau3mu_tmp                       
                                            
        if len(seltau3mu) == 0:
            return False

        self.counters.counter('Tau3Mu').inc('pass (mu, mu, mu) Z cut')

        # match only if the trigger fired
        event.fired_triggers = [info.name for info in getattr(event, 'trigger_infos', []) if info.fired]

        # trigger matching
        if hasattr(self.cfg_ana, 'trigger_match') and len(self.cfg_ana.trigger_match.keys())>0:
                                   
            for triplet in seltau3mu:
                
                triplet.hltmatched = [] # initialise to no match
                
                triplet.trig_objs = OrderedDict()
                triplet.trig_objs[1] = [] # initialise to no trigger objct matches
                triplet.trig_objs[2] = [] # initialise to no trigger objct matches
                triplet.trig_objs[3] = [] # initialise to no trigger objct matches
    
                triplet.trig_matched = OrderedDict()
                triplet.trig_matched[1] = False # initialise to no match
                triplet.trig_matched[2] = False # initialise to no match
                triplet.trig_matched[3] = False # initialise to no match

                triplet.best_trig_match = OrderedDict()
                triplet.best_trig_match[1] = OrderedDict()
                triplet.best_trig_match[2] = OrderedDict()
                triplet.best_trig_match[3] = OrderedDict()

                # add all matched objects to each muon
                for info in event.trigger_infos:
                                    
                    mykey = '_'.join(info.name.split('_')[:-1])

                    # start with simple matching
                    these_objects1 = sorted([obj for obj in info.objects if deltaR(triplet.mu1(), obj)<0.15], key = lambda x : deltaR(x, triplet.mu1()))
                    these_objects2 = sorted([obj for obj in info.objects if deltaR(triplet.mu2(), obj)<0.15], key = lambda x : deltaR(x, triplet.mu2()))
                    these_objects3 = sorted([obj for obj in info.objects if deltaR(triplet.mu3(), obj)<0.15], key = lambda x : deltaR(x, triplet.mu3()))

                    triplet.trig_objs[1] += these_objects1
                    triplet.trig_objs[2] += these_objects2
                    triplet.trig_objs[3] += these_objects3

                    # get the set of trigger types from the cfg 
                    trigger_types_to_match = self.cfg_ana.trigger_match[mykey][1]
                    
                    # list of tuples of matched objects
                    good_matches = []

                    # initialise the matching to None
                    triplet.best_trig_match[1][mykey] = None
                    triplet.best_trig_match[2][mykey] = None
                    triplet.best_trig_match[3][mykey] = None

                    # investigate all the possible matches (triplets, pairs or singlets)
                    for to1, to2, to3 in product(these_objects1, these_objects2, these_objects3):
                        # avoid double matches!
                        if to1==to2 or to1==to3 or to2==to3:
                            continue

                        # intersect found trigger types to desired trigger types
                        itypes = Counter()
                        for ikey in trigger_types_to_match.keys():
                            itypes[ikey] = sum([1 for iobj in [to1, to2, to3] if iobj.triggerObjectTypes()[0]==ikey])
                                            
                        # all the types to match are matched then assign the 
                        # corresponding trigger object to each muon
                        if itypes & trigger_types_to_match == trigger_types_to_match:
                            good_matches.append((to1, to2, to3))
                    
                    if len(good_matches):
                        good_matches.sort(key = lambda x : deltaR(x[0], triplet.mu1()) + deltaR(x[1], triplet.mu2()) + deltaR(x[2], triplet.mu3()))        
                        triplet.best_trig_match[1][mykey] = good_matches[0][0] if len(good_matches[0])>0 else None
                        triplet.best_trig_match[2][mykey] = good_matches[0][1] if len(good_matches[0])>1 else None
                        triplet.best_trig_match[3][mykey] = good_matches[0][2] if len(good_matches[0])>2 else None
                
                # iterate over the path:filters dictionary
                #     the filters MUST be sorted correctly: i.e. first filter in the dictionary 
                #     goes with the first muons and so on
                for k, vv in self.cfg_ana.trigger_match.iteritems():

                    if not any(k in name for name in event.fired_triggers):
                         continue
                    
                    v = vv[0]
                                                                 
                    for ii, filters in enumerate(v):
                        if not triplet.best_trig_match[ii+1][k]:
                            continue
                        if set([filters]) & set(triplet.best_trig_match[ii+1][k].filterLabels()):
                            triplet.trig_matched[ii+1] = True                 
                    
                    ismatched = sum(triplet.trig_matched.values())            
                                
                    if len(v) == ismatched:
                        triplet.hltmatched.append(k)

            seltau3mu = [triplet for triplet in seltau3mu if len(triplet.hltmatched)>0]
            
            if len(seltau3mu) == 0:
                return False
            self.counters.counter('Tau3Mu').inc('trigger matched')
            
        event.seltau3mu = seltau3mu

        event.tau3mu = self.bestTriplet(event.seltau3mu)

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

    
