import ROOT
import math

from ROOT import gSystem
from copy import deepcopy as dc
from itertools import product

from PhysicsTools.Heppy.analyzers.core.Analyzer       import Analyzer
from PhysicsTools.Heppy.analyzers.core.AutoHandle     import AutoHandle
from PhysicsTools.Heppy.physicsobjects.PhysicsObjects import Muon

from CMGTools.WTau3Mu.physicsobjects.Tau3MuMET import Tau3MuMET
from CMGTools.WTau3Mu.analyzers.resonances     import resonances, sigmas_to_exclude

gSystem.Load("libCMGToolsWTau3Mu")

from ROOT import Tau3MuKinematicVertexFitterProducer as VertexFitter

class Tau3MuKinematicVertexFitterAnalyzer(Analyzer):
    '''
    https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideKinematicVertexFit
    '''

    def beginLoop(self, setup):
        super(Tau3MuKinematicVertexFitterAnalyzer, self).beginLoop(setup)
        self.counters.addCounter('KinematicVertexFitter')
        count = self.counters.counter('KinematicVertexFitter')
        count.register('all events')
        count.register('>0 triplets with good vertex')
        count.register('>0 triplets without resonances with other muons')
        count.register('candidate chosen')        
        count.register('valid refitted vertex')
        count.register('valid refitted muon 1')
        count.register('valid refitted muon 2')
        count.register('valid refitted muon 3')
        
        self.vertTool = ROOT.VertexDistanceXY()
        self.vf = VertexFitter()

    def declareHandles(self):
        super(Tau3MuKinematicVertexFitterAnalyzer, self).declareHandles()

        self.handles['offlinebeamspot'] = AutoHandle(
            'offlineBeamSpot',
            'reco::BeamSpot'
        )

    def hasDiMuonVertex(self, mu1, mu2, minprob=0.):
        muons = ROOT.std.vector('pat::Muon')()
        muons.push_back(mu1.physObj)
        muons.push_back(mu2.physObj)
        svtree = self.vf.Fit(muons)
        
        # check that the vertex is valid
        if svtree.get().isEmpty() or not svtree.get().isValid():
            return False, svtree
        
        # optional: check that the vertex probability is good enough
        if minprob > 0.:
            svtree.movePointerToTheTop()
            sv = svtree.currentDecayVertex().get()
            recoSv = self.RecoVertex(sv, kinVtxTrkSize=2)
            svprob = ROOT.TMath.Prob(recoSv.chi2(), int(recoSv.ndof()))
            # if the vertex is there, but with low prob
            if svprob < minprob:
                return False, svtree
        # the two muons make a good vertex with good probability
        return True, svtree
        
    def checkTripletVertex(self, triplet):
        muons = ROOT.std.vector('pat::Muon')()
        muons.push_back(triplet.mu1().physObj)
        muons.push_back(triplet.mu2().physObj)
        muons.push_back(triplet.mu3().physObj)

        svtree = self.vf.Fit(muons)
        
        if svtree.get().isEmpty() or not svtree.get().isValid():
            return False
        
        triplet.svtree = svtree
        svtree.movePointerToTheTop()
        sv = svtree.currentDecayVertex().get()
        
        recoSv = self.RecoVertex(sv, kinVtxTrkSize=3)
        
        svprob = ROOT.TMath.Prob(recoSv.chi2(), int(recoSv.ndof()))
        triplet.svtree.prob = svprob
        
        return True
        
    def checkResonanceOtherMuon(self, triplet, event):
        # muons from the triplet
        tripletMuons = [triplet.mu1(), triplet.mu2(), triplet.mu3()]
        # other muons, not in the considered triplet
        otherMuons   = [mu for mu in event.muons if mu not in tripletMuons]

        # build and check all possible pairs from triplet and other muons
        pairs = [(i,j) for i, j in product(tripletMuons, otherMuons) if (i.charge()+j.charge()) == 0]
        for rmass, rwidth, _ in resonances:
            for m1, m2 in pairs:
                #import pdb ; pdb.set_trace()
                hasVtx, vtxtree = self.hasDiMuonVertex(m1, m2, 0.05)
                if not hasVtx:
                    continue
                # get mu1 refitted p4
                vtxtree.movePointerToTheFirstChild()
                mu1ref = vtxtree.currentParticle()
                refitMu1 = self.buildP4(mu1ref)[0]
                
                # get mu2 refitted p4
                vtxtree.movePointerToTheNextChild()
                mu2ref = vtxtree.currentParticle()
                refitMu2 = self.buildP4(mu2ref)[0]
                
                # check mass of the refitted dimuon
                delta_mass = abs( (refitMu1+refitMu2).M() - rmass ) / rwidth
                if delta_mass < sigmas_to_exclude:
                        return False

        return True
    
    def process(self, event):
        self.readCollections(event.input)

        self.counters.counter('KinematicVertexFitter').inc('all events')
        
        event.bs = self.handles['offlinebeamspot'].product()

        point = ROOT.reco.Vertex.Point(
            event.bs.position().x(),
            event.bs.position().y(),
            event.bs.position().z(),
        )
        error = event.bs.covariance3D()
        chi2 = 0.
        ndof = 0.
        bsvtx = ROOT.reco.Vertex(point, error, chi2, ndof, 3) # size? say 3? does it matter?

        # select the best triplet candidate, according to:

        #   - the candidate must have a good refitted vertex
        candidates = [cand for cand in event.seltau3mu if self.checkTripletVertex(cand)]
        if not len(candidates):
            return False
        self.counters.counter('KinematicVertexFitter').inc('>0 triplets with good vertex')

        #   - none of the candidate's muons can make a good resonance with another muon in the event
        candidates = [cand for cand in candidates if self.checkResonanceOtherMuon(cand, event)]
        if not len(candidates):
            return False
        self.counters.counter('KinematicVertexFitter').inc('>0 triplets without resonances with other muons')

        #   - if there's still more than one candidate, pick the one with the best vertex probability.
        #     Give precedence to candidates with the correct charge        
        candidates.sort(key=lambda cand : (abs(cand.charge())==1, cand.mttau()), reverse=True)
        candidate = candidates[0]
#         if len(candidates)>1:
#             print '\n###############################################################'
#             import pdb ; pdb.set_trace()
#             for tt in candidates: print tt.charge(), tt.p4Muons().pt(), tt.p4Muons().eta(), tt.p4Muons().phi(), tt.p4Muons().mass(), tt.mttau(), tt.svtree.prob 
        self.counters.counter('KinematicVertexFitter').inc('candidate chosen')        

        # save the number of candidates as event attribute
        event.ncands = len(candidates)
        
        # now investigate the one good candidate
        event.tau3mu = candidate
        svtree = candidate.svtree
        
        # accessing the tree components
        svtree.movePointerToTheTop()

        # We are now at the top of the decay tree getting
        # the Tau reconstructed KinematicPartlcle
        tauref = svtree.currentParticle()
        event.tau3mu.refitTau = self.buildP4(tauref)[0]
        
        # getting the tau->mu mu mu decay vertex
        sv = svtree.currentDecayVertex().get()
        
        if not sv.vertexIsValid(): return False
        self.counters.counter('KinematicVertexFitter').inc('valid refitted vertex')
       
        # this shit does not work, but it should http://cmslxr.fnal.gov/source/RecoVertex/KinematicFitPrimitives/src/KinematicVertex.cc#0112
        # event.tau3mu.refittedVertex = getattr(sv, 'operator Vertex')() # this is now a reco::Vertex
        
        # let's work it around
        tauvtx = self.RecoVertex(sv, kinVtxTrkSize=3)

        # Now navigating down the tree, mu1
        if not svtree.movePointerToTheFirstChild(): return False
        self.counters.counter('KinematicVertexFitter').inc('valid refitted muon 1')
        mu1ref = svtree.currentParticle()
        refitMu1 = self.buildP4(mu1ref)[0]

        # mu2
        if not svtree.movePointerToTheNextChild(): return False
        self.counters.counter('KinematicVertexFitter').inc('valid refitted muon 2')
        mu2ref = svtree.currentParticle()
        refitMu2 = self.buildP4(mu2ref)[0]

        # mu3
        if not svtree.movePointerToTheNextChild(): return False
        self.counters.counter('KinematicVertexFitter').inc('valid refitted muon 3')
        mu3ref = svtree.currentParticle()
        refitMu3 = self.buildP4(mu3ref)[0]

        # create a new tau3mu object using the original pat muons
        # after their p4 is updated to the refitted p4
        
        mu1refit = dc(event.tau3mu.mu1().physObj) # clone PAT Muons
        mu2refit = dc(event.tau3mu.mu2().physObj) # clone PAT Muons
        mu3refit = dc(event.tau3mu.mu3().physObj) # clone PAT Muons

        mu1refit.setP4(refitMu1) # update p4
        mu2refit.setP4(refitMu2) # update p4
        mu3refit.setP4(refitMu3) # update p4
        
        # instantiate heppy muons from PAT muons
        refitMuons = [
             Muon(mu1refit), 
             Muon(mu2refit), 
             Muon(mu3refit),
        ]
        
        # associate the primary vertex to the muons
        for mu in refitMuons:
            mu.associatedVertex = event.vertices[0]
        
        # propagate the new muon p4s to the MET: subtract old, add new muons
        newmet = dc(event.tau3mu.met())
        
        newmetP4 = event.tau3mu.met().p4() - \
                   event.tau3mu.mu1().p4() - \
                   event.tau3mu.mu2().p4() - \
                   event.tau3mu.mu3().p4() + \
                   mu1refit.p4()           + \
                   mu2refit.p4()           + \
                   mu3refit.p4()
        
        newmet.setP4(newmetP4)
                
        # create a new tau3mu object
        event.tau3muRefit = Tau3MuMET(refitMuons, newmet)

        # append the refitted vertex to it
        event.tau3muRefit.refittedVertex = tauvtx

        # calculate 2D displacement significance
        distanceTauBS = self.vertTool.distance(tauvtx, bsvtx)
        event.tau3muRefit.refittedVertex.ls = distanceTauBS.significance()

        # calculate decay length significance w.r.t. the beamspot
        tauperp = ROOT.math.XYZVector(event.tau3mu.refitTau.px(),
                                      event.tau3mu.refitTau.py(),
                                      0.)
        
        displacementFromBeamspotTau = ROOT.GlobalPoint(-1*((event.bs.x0() - tauvtx.x()) + (tauvtx.z() - event.bs.z0()) * event.bs.dxdz()), 
                                                       -1*((event.bs.y0() - tauvtx.y()) + (tauvtx.z() - event.bs.z0()) * event.bs.dydz()),
                                                        0)
        
        vperptau = ROOT.math.XYZVector(displacementFromBeamspotTau.x(), displacementFromBeamspotTau.y(), 0.)
        
        event.tau3muRefit.refittedVertex.cos = vperptau.Dot(tauperp)/(vperptau.R()*tauperp.R())

#         print '         tau3mu MET after corrections pt ', event.tau3mu.met().pt()
#         print '         tau3mu MET after corrections phi', event.tau3mu.met().phi()
#         print '         tau3mu mT  after corrections    ', event.tau3mu.mttau()
#         print 'refitted tau3mu MET after corrections pt ', event.tau3muRefit.met().pt()
#         print 'refitted tau3mu MET after corrections phi', event.tau3muRefit.met().phi()
#         print 'refitted tau3mu mT  after corrections    ', event.tau3muRefit.mttau()
        
        return True

    @staticmethod
    def buildP4(ref):

        ref_x  = ref.currentState().kinematicParameters().vector().At(0)
        ref_y  = ref.currentState().kinematicParameters().vector().At(1)
        ref_z  = ref.currentState().kinematicParameters().vector().At(2)
        ref_px = ref.currentState().kinematicParameters().vector().At(3)
        ref_py = ref.currentState().kinematicParameters().vector().At(4)
        ref_pz = ref.currentState().kinematicParameters().vector().At(5)
        ref_m  = ref.currentState().kinematicParameters().vector().At(6)

        energy = math.sqrt(ref_px**2 + ref_py**2 + ref_pz**2 + ref_m**2)

        p4 = ROOT.Math.LorentzVector("ROOT::Math::PxPyPzE4D<double>")(ref_px, ref_py, ref_pz, energy)
        
        return p4, ref

    @staticmethod
    def RecoVertex(kinVtx, kinVtxChi2=0., kinVtxNdof=0, kinVtxTrkSize=0):
        point = ROOT.reco.Vertex.Point(
            kinVtx.vertexState().position().x(),
            kinVtx.vertexState().position().y(),
            kinVtx.vertexState().position().z(),
        )
        error = kinVtx.vertexState().error().matrix()
        chi2  = kinVtxChi2 if kinVtxChi2 else kinVtx.chiSquared()
        ndof  = kinVtxNdof if kinVtxNdof else kinVtx.degreesOfFreedom()
        recoVtx = ROOT.reco.Vertex(point, error, chi2, ndof, kinVtxTrkSize)
        return recoVtx
    
    