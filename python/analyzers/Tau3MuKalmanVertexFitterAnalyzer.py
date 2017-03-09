import ROOT
import math

from ROOT import gSystem
from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle

gSystem.Load("libCMGToolsWTau3Mu")

from ROOT import Tau3MuKalmanVertexFitterProducer as VertexFitter

class Tau3MuKalmanVertexFitterAnalyzer(Analyzer):

    def declareHandles(self):
        super(Tau3MuKalmanVertexFitterAnalyzer, self).declareHandles()

        self.handles['offlinebeamspot'] = AutoHandle(
            'offlineBeamSpot',
            'reco::BeamSpot'
        )
    
    def process(self, event):
        self.readCollections(event.input)
        
        event.bs = self.handles['offlinebeamspot'].product()

        muons = ROOT.std.vector('pat::Muon')()
        muons.push_back(event.tau3mu.mu1().physObj)
        muons.push_back(event.tau3mu.mu2().physObj)
        muons.push_back(event.tau3mu.mu3().physObj)
    
        try:
            vf = VertexFitter()
            secondaryVertex = vf.Fit(muons) # this is a TransientVertex
            tauVertex = getattr(secondaryVertex, 'operator Vertex')() # this is now a reco::Vertex, see http://cmslxr.fnal.gov/source/RecoVertex/VertexPrimitives/interface/TransientVertex.h#0237
            event.tau3mu.refittedVertex = tauVertex
        except:
            pass
       
        if event.tau3mu.refittedVertex is None or not event.tau3mu.refittedVertex.isValid():
            return True
                
        tauvtx    = secondaryVertex.position()
        tauvtxerr = secondaryVertex.positionError()
        
        # calculate three-track transverse momentum
        tauperp = ROOT.math.XYZVector(muons[0].px() + muons[1].px() + muons[2].px(),
                                      muons[0].py() + muons[1].py() + muons[2].py(),
                                      0.)
        
        # calculate decay length significance w.r.t. the beamspot
        displacementFromBeamspotTau = ROOT.GlobalPoint(-1*((event.bs.x0() - tauvtx.x()) + (tauvtx.z() - event.bs.z0()) * event.bs.dxdz()), 
                                                       -1*((event.bs.y0() - tauvtx.y()) + (tauvtx.z() - event.bs.z0()) * event.bs.dydz()),
                                                        0)
        vperptau = ROOT.math.XYZVector(displacementFromBeamspotTau.x(), displacementFromBeamspotTau.y(), 0.)

        event.tau3mu.refittedVertex.ls  = displacementFromBeamspotTau.perp() / math.sqrt(tauvtxerr.rerr(displacementFromBeamspotTau))
        event.tau3mu.refittedVertex.cos = vperptau.Dot(tauperp)/(vperptau.R()*tauperp.R())

        # add refitted p4 to the muons
#         event.tau3mu.mu1_.p4refit = 
#         event.tau3mu.mu2_.p4refit = 
#         event.tau3mu.mu3_.p4refit = 
#         event.refitTau3mu = event.tau3mu

        return True






