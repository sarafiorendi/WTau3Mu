#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "FWCore/Framework/interface/ConsumesCollector.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/HepMCCandidate/interface/GenParticleFwd.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/MuonReco/interface/Muon.h"
#include "DataFormats/MuonReco/interface/MuonFwd.h"
#include "DataFormats/MuonReco/interface/MuonSelectors.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"

#include "MagneticField/Engine/interface/MagneticField.h"
#include "MagneticField/Records/interface/IdealMagneticFieldRecord.h"
#include "RecoVertex/KalmanVertexFit/interface/KalmanVertexFitter.h"
#include "TrackingTools/PatternTools/interface/ClosestApproachInRPhi.h"
#include "TrackingTools/PatternTools/interface/TSCBLBuilderNoMaterial.h"
#include "TrackingTools/Records/interface/TransientTrackRecord.h"
#include "TrackingTools/TransientTrack/interface/TransientTrackBuilder.h"

#include "TrackingTools/TransientTrack/interface/TransientTrackBuilder.h"
#include "MagneticField/ParametrizedEngine/src/OAEParametrizedMagneticField.h"


class Tau3MuKalmanVertexFitterProducer {

  public:
    Tau3MuKalmanVertexFitterProducer() {};
    virtual ~Tau3MuKalmanVertexFitterProducer() {};

    reco::TransientTrack getTransientTrack(const reco::TrackRef& trackRef) {    
      reco::TransientTrack transientTrack(trackRef, paramField);
      return transientTrack;
    }

    TransientVertex Fit(const pat::MuonCollection & muons)
    {
    
      // do tau vertex fit
      std::vector<reco::TransientTrack> tau_tks;
      for (pat::MuonCollection::const_iterator imu = muons.begin(); imu != muons.end(); ++imu){
          tau_tks.push_back(getTransientTrack(imu->track()));
      }
    
      KalmanVertexFitter taukvf;
      TransientVertex tautv = taukvf.vertex(tau_tks);
      
      // reco::Vertex tauvertex = tautv;
      
      return tautv;
          
    };

  private:
    OAEParametrizedMagneticField *paramField = new OAEParametrizedMagneticField("3_8T");

};
