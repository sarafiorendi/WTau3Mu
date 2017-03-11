import ROOT
import math

from ROOT import gSystem
from copy import deepcopy as dc
from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle
from CMGTools.WTau3Mu.physicsobjects.Tau3MuMET import Tau3MuMET
from PhysicsTools.Heppy.physicsobjects.PhysicsObjects import Muon

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

        muons = ROOT.std.vector('pat::Muon')()
        muons.push_back(event.tau3mu.mu1().physObj)
        muons.push_back(event.tau3mu.mu2().physObj)
        muons.push_back(event.tau3mu.mu3().physObj)
             
        svtree = self.vf.Fit(muons)
        
        if svtree.get().isEmpty() or not svtree.get().isValid():
            return False
        
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
        point = ROOT.reco.Vertex.Point(
            sv.vertexState().position().x(),
            sv.vertexState().position().y(),
            sv.vertexState().position().z(),
        )
        error = sv.vertexState().error().matrix()
        chi2 = sv.chiSquared()
        ndof = sv.degreesOfFreedom()
        tauvtx = ROOT.reco.Vertex(point, error, chi2, ndof, 3)

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
        
        # create a new tau3mu object
        event.tau3muRefit = Tau3MuMET(refitMuons, event.tau3mu.met())

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

