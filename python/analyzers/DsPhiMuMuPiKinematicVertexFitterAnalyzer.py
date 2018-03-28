import ROOT
import math

from ROOT import gSystem
from copy import deepcopy as dc
from itertools import product

from PhysicsTools.Heppy.analyzers.core.Analyzer       import Analyzer
from PhysicsTools.Heppy.analyzers.core.AutoHandle     import AutoHandle
from PhysicsTools.Heppy.physicsobjects.PhysicsObjects import Muon

from CMGTools.WTau3Mu.physicsobjects.DsPhiMuMuPi      import DsPhiMuMuPi

gSystem.Load("libCMGToolsWTau3Mu")

from ROOT import DsPhiMuMuPiKinematicVertexFitterProducer as VertexFitter

class DsPhiMuMuPiKinematicVertexFitterAnalyzer(Analyzer):
    '''
    https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideKinematicVertexFit
    '''

    def beginLoop(self, setup):
        super(DsPhiMuMuPiKinematicVertexFitterAnalyzer, self).beginLoop(setup)
        self.counters.addCounter('KinematicVertexFitter')
        count = self.counters.counter('KinematicVertexFitter')
        count.register('all events')
        count.register('has refitted vertex')
        count.register('valid refitted vertex')
        count.register('valid refitted muon 1')
        count.register('valid refitted muon 2')
        count.register('valid refitted pion'  )
        
        self.vertTool = ROOT.VertexDistanceXY()
        self.vf = VertexFitter()

    def declareHandles(self):
        super(DsPhiMuMuPiKinematicVertexFitterAnalyzer, self).declareHandles()

        self.handles['offlinebeamspot'] = AutoHandle(
            'offlineBeamSpot',
            'reco::BeamSpot'
        )

    def checkTripletVertex(self, ds):
        muons = ROOT.std.vector('pat::Muon')()
        muons.push_back(ds.mu1().physObj)
        muons.push_back(ds.mu2().physObj)

        pion = ds.pi()
        
        svtree = self.vf.Fit(muons, pion)
        
        if svtree.get().isEmpty() or not svtree.get().isValid():
            return False
        
        ds.svtree = svtree
        svtree.movePointerToTheTop()
        sv = svtree.currentDecayVertex().get()

        if not sv.vertexIsValid(): 
            return False
        
        recoSv = self.RecoVertex(sv, kinVtxTrkSize=3)
        
        svprob = ROOT.TMath.Prob(recoSv.chi2(), int(recoSv.ndof()))
        ds.svtree.prob = svprob
        
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

        # loop over all Ds candidates
        cands = []
        for ids in event.dsphipis:

            # select the best triplet candidate, according to:
    
            #   - the candidate must have a good refitted vertex
            hasvtx = self.checkTripletVertex(ids)
            
            if not hasvtx:
                continue
            
            cands.append(ids)
        
        # sort candidates by vertex prob and pick the first
        cands.sort(key=lambda ds : ( ds.has_phi(), ds.svtree.prob ), reverse = True)

        if not len(cands):
            return False
            
        event.ds = cands[0]
        
        self.counters.counter('KinematicVertexFitter').inc('has refitted vertex')
 
        # now investigate the one good candidate
        svtree = event.ds.svtree
    
        # accessing the tree components
        svtree.movePointerToTheTop()
    
        # We are now at the top of the decay tree getting
        # the Tau reconstructed KinematicPartlcle
        dsref = svtree.currentParticle()
        event.ds.dsref = self.buildP4(dsref)[0]
        
        # getting the ds->phi(mu,mu) pi decay vertex
        sv = svtree.currentDecayVertex().get()
        
        if not sv.vertexIsValid(): return False
        self.counters.counter('KinematicVertexFitter').inc('valid refitted vertex')
        
        # let's work it around
        dsvtx = self.RecoVertex(sv, kinVtxTrkSize=3)
    
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
    
        # pion
        if not svtree.movePointerToTheNextChild(): return False
        self.counters.counter('KinematicVertexFitter').inc('valid refitted pion')
        piref = svtree.currentParticle()
        refitPi = self.buildP4(piref)[0]
    
        # create a new ds object using the original pat muons and pi
        # after their p4 is updated to the refitted p4        
        pirefit = ROOT.pat.PackedCandidate(event.ds.pi()) # clone PAT PackedCandidate        
        pirefit.setP4(refitPi) # update p4
    
        # instantiate heppy muons from PAT muons
        mu1refit = dc(Muon(event.ds.mu1().physObj))
        mu2refit = dc(Muon(event.ds.mu2().physObj))
    
        mu1refit.setP4(refitMu1) # update p4
        mu2refit.setP4(refitMu2) # update p4
        
        refitMuons = [
            mu1refit, 
            mu2refit, 
        ]
    
        # associate the primary vertex to the muons
        for mu in refitMuons:
            mu.associatedVertex = event.vertices[0]
        
        # create a new tau3mu object
        event.dsRefit = DsPhiMuMuPi(refitMuons, pirefit)
    
        # append the refitted vertex to it
        event.dsRefit.refittedVertex = dsvtx
    
        # calculate 2D displacement significance
        distanceDsBS = self.vertTool.distance(dsvtx, bsvtx)
        event.dsRefit.refittedVertex.ls = distanceDsBS.significance()
    
        # calculate decay length significance w.r.t. the beamspot
        dsperp = ROOT.math.XYZVector(event.ds.dsref.px(),
                                     event.ds.dsref.py(),
                                     0.)
        
        displacementFromBeamspotDs = ROOT.GlobalPoint(-1*((event.bs.x0() - dsvtx.x()) + (dsvtx.z() - event.bs.z0()) * event.bs.dxdz()), 
                                                      -1*((event.bs.y0() - dsvtx.y()) + (dsvtx.z() - event.bs.z0()) * event.bs.dydz()),
                                                       0)
        
        vperpds = ROOT.math.XYZVector(displacementFromBeamspotDs.x(), displacementFromBeamspotDs.y(), 0.)
        
        event.dsRefit.refittedVertex.cos = vperpds.Dot(dsperp)/(vperpds.R()*dsperp.R())

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
    
    