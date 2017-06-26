// -*- C++ -*-
//
// Package:    CMGTools/WTau3Mu
// Class:      L1MuonRecoPropagator
// 
/**\class L1MuonRecoPropagator L1MuonRecoPropagator.cc CMGTools/WTau3Mu/src/L1MuonRecoPropagator.cc

 Description: for each PAT muon extrapolates its coordinates to the second muon station, 
              so that the offline-L1 matching is done on an equal footing.
              Saves a map: each offline muon is associated to the extrapolated 4 vector. 
              
              Very much inspired to 
              https://github.com/cms-l1-dpg/Legacy-L1Ntuples/blob/6b1d8fce0bd2058d4309af71b913e608fced4b17/src/L1MuonRecoTreeProducer.cc

*/
//
// Original Author:  Riccardo Manzoni
//
//

#include <memory>

// ROOT
#include "TMath.h"
#include "TLorentzVector.h"

// framework
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/Utilities/interface/InputTag.h"

// Muons & Tracks Data Formats
#include "DataFormats/GeometrySurface/interface/Cylinder.h"
#include "DataFormats/GeometrySurface/interface/Plane.h"
#include "DataFormats/MuonReco/interface/Muon.h"
#include "DataFormats/MuonReco/interface/MuonFwd.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackExtra.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"

// Cond Formats
#include "CondFormats/AlignmentRecord/interface/TrackerSurfaceDeformationRcd.h"

// Transient tracks (for extrapolations)
#include "TrackingTools/GeomPropagators/interface/Propagator.h"
#include "TrackingTools/Records/interface/TrackingComponentsRecord.h"
#include "TrackingTools/TrajectoryState/interface/FreeTrajectoryState.h"
#include "TrackingTools/TrajectoryState/interface/TrajectoryStateOnSurface.h"
#include "TrackingTools/TrajectoryState/interface/TrajectoryStateTransform.h"

// B Field
#include "MagneticField/Engine/interface/MagneticField.h"

namespace cmg{
  class L1MuonRecoPropagator : public edm::EDProducer {
    public:
      explicit L1MuonRecoPropagator(const edm::ParameterSet & iConfig);
      virtual ~L1MuonRecoPropagator() { }
  
      virtual void produce(edm::Event & iEvent, const edm::EventSetup& iSetup) override;
  
      TrajectoryStateOnSurface  cylExtrapTrkSam  (reco::TrackRef track, double rho);
      TrajectoryStateOnSurface  surfExtrapTrkSam (reco::TrackRef track, double z);
    
    private:

      // The Magnetic field
      edm::ESHandle<MagneticField> theBField;
       
      // reco muons
      const edm::EDGetTokenT<edm::View<pat::Muon>> muonSrc_;
      edm::Handle<edm::View<pat::Muon>> mucand;

      // Extrapolator to cylinder
      edm::ESHandle<Propagator> propagatorAlong;
      edm::ESHandle<Propagator> propagatorOpposite;
    
      FreeTrajectoryState freeTrajStateMuon(reco::TrackRef track);
      
      // Trajectory on surface
      TrajectoryStateOnSurface tsos;
      
      // PiGreco
      float pig = TMath::Pi();
      
      // phi and eta
      double phi, eta;
      
      // extrapolated lorentz vector
      TLorentzVector ME2Pextrap;    
      TLorentzVector ME2Mextrap;    
      TLorentzVector MB2extrap;    
      
  };
}

cmg::L1MuonRecoPropagator::L1MuonRecoPropagator(const edm::ParameterSet & iConfig):
  muonSrc_( consumes<edm::View<pat::Muon>>(iConfig.getParameter<edm::InputTag>("patMuonSrc") ) )
{ 
  produces<std::vector<std::pair<edm::Ptr<pat::Muon>, TLorentzVector>>> ("ME2Pextrap");
  produces<std::vector<std::pair<edm::Ptr<pat::Muon>, TLorentzVector>>> ("ME2Mextrap");
  produces<std::vector<std::pair<edm::Ptr<pat::Muon>, TLorentzVector>>> ("MB2extrap" );
}


void 
cmg::L1MuonRecoPropagator::produce(edm::Event & iEvent, const edm::EventSetup & iSetup)
{
  
  // unique pointers for the output
  std::unique_ptr<std::vector<std::pair<edm::Ptr<pat::Muon>, TLorentzVector>>> ME2Pextrap_ptr(new std::vector<std::pair<edm::Ptr<pat::Muon>, TLorentzVector>>);
  std::unique_ptr<std::vector<std::pair<edm::Ptr<pat::Muon>, TLorentzVector>>> ME2Mextrap_ptr(new std::vector<std::pair<edm::Ptr<pat::Muon>, TLorentzVector>>);
  std::unique_ptr<std::vector<std::pair<edm::Ptr<pat::Muon>, TLorentzVector>>> MB2extrap_ptr (new std::vector<std::pair<edm::Ptr<pat::Muon>, TLorentzVector>>);
       
  // Get the muon candidates
  iEvent.getByToken(muonSrc_, mucand);

  // Get the Magnetic field from the setup
  iSetup.get<IdealMagneticFieldRecord>().get(theBField);

  // Get the propagators 
  iSetup.get<TrackingComponentsRecord>().get("SmartPropagatorAny"        , propagatorAlong   );
  iSetup.get<TrackingComponentsRecord>().get("SmartPropagatorAnyOpposite", propagatorOpposite);
  
//   for(pat::MuonCollection::const_iterator imu = mucand->begin(); imu != mucand->end(); imu++){
  for(edm::View<pat::Muon>::const_iterator imu = mucand->begin(); imu != mucand->end(); imu++){
    
    // Get the pointer to the muon in the collection
    unsigned int idx = imu - mucand->begin();
    edm::Ptr<pat::Muon> ptrMuon = mucand->ptrAt(idx);
    
    // reset the extrapolated TLorentzVectors to the pat Muon p4
    ME2Pextrap.SetPtEtaPhiM(imu->pt(), imu->eta(), imu->phi(), imu->mass());
    ME2Mextrap.SetPtEtaPhiM(imu->pt(), imu->eta(), imu->phi(), imu->mass());
    MB2extrap .SetPtEtaPhiM(imu->pt(), imu->eta(), imu->phi(), imu->mass());

    if (imu->isStandAloneMuon() || imu->isGlobalMuon()){

      // RM: don't be lazy, use a logger!
      // std::cout << __LINE__ << " ==============================================================================="<< std::endl;
      // std::cout             << "reco pt  " << imu -> pt() <<  "\t eta  " << imu->eta() << "\t phi  " << imu->phi() << std::endl;
          
      // Take the tracker track and build a transient track out of it
      reco::TrackRef tr_mu = imu->outerTrack(); // the only one that does not fail!
        
      tsos = surfExtrapTrkSam(tr_mu, 790);   // track at ME2+ plane - extrapolation
      if (tsos.isValid()) {
        phi = tsos.globalMomentum().phi();
        eta = tsos.globalMomentum().eta();
        ME2Pextrap.SetPtEtaPhiM(imu->pt(), eta, phi, imu->mass());
        // std::cout << "\t extrapolation to ME2+ plane" << std::endl;
        // std::cout << "\t phi " << phi << " eta " << eta << std::endl;
      }
      
      tsos = surfExtrapTrkSam(tr_mu, -790);   // track at ME2- plane - extrapolation
      if (tsos.isValid()) {
        phi = tsos.globalMomentum().phi();
        eta = tsos.globalMomentum().eta();
        ME2Mextrap.SetPtEtaPhiM(imu->pt(), eta, phi, imu->mass());
        // std::cout << "\t extrapolation to ME2- plane" << std::endl;
        // std::cout << "\t phi " << phi << " eta " << eta << std::endl;
      }
  
      tsos = cylExtrapTrkSam(tr_mu, 500);  // track at MB2 radius - extrapolation
      if (tsos.isValid()) {
        phi = tsos.globalMomentum().phi();
        eta = tsos.globalMomentum().eta();
        MB2extrap.SetPtEtaPhiM(imu->pt(), eta, phi, imu->mass());
        // std::cout << "\t extrapolation to MB2 plane" << std::endl;
        // std::cout << "\t phi " << phi << " eta " << eta << std::endl;
      }    
    }

    ME2Pextrap_ptr -> push_back ( std::pair<edm::Ptr<pat::Muon>, TLorentzVector>( ptrMuon, ME2Pextrap) );
    ME2Mextrap_ptr -> push_back ( std::pair<edm::Ptr<pat::Muon>, TLorentzVector>( ptrMuon, ME2Pextrap) );
    MB2extrap_ptr  -> push_back ( std::pair<edm::Ptr<pat::Muon>, TLorentzVector>( ptrMuon, ME2Pextrap) );

  }
  
  iEvent.put(std::move(ME2Pextrap_ptr), "ME2Pextrap");
  iEvent.put(std::move(ME2Mextrap_ptr), "ME2Mextrap");
  iEvent.put(std::move(MB2extrap_ptr ), "MB2extrap" );

}

FreeTrajectoryState 
cmg::L1MuonRecoPropagator::freeTrajStateMuon(reco::TrackRef track)
{
    
  GlobalPoint  innerPoint(track->innerPosition().x(), track->innerPosition().y(),  track->innerPosition().z());
  GlobalVector innerVec  (track->innerMomentum().x(), track->innerMomentum().y(),  track->innerMomentum().z());  
  
  FreeTrajectoryState recoStart(innerPoint, innerVec, track->charge(), &*theBField);
  
  return recoStart;
}

TrajectoryStateOnSurface
cmg::L1MuonRecoPropagator::surfExtrapTrkSam(reco::TrackRef track, double z)
{
  Plane::PositionType pos(0, 0, z);
  Plane::RotationType rot;
  Plane::PlanePointer myPlane = Plane::build(pos, rot);

  FreeTrajectoryState recoStart = freeTrajStateMuon(track);
  TrajectoryStateOnSurface recoProp;
  recoProp = propagatorAlong->propagate(recoStart, *myPlane);
  if (!recoProp.isValid()) {
    recoProp = propagatorOpposite->propagate(recoStart, *myPlane);
  }
  return recoProp;
}

TrajectoryStateOnSurface 
cmg::L1MuonRecoPropagator::cylExtrapTrkSam(reco::TrackRef track, double rho)
{
  Cylinder::PositionType pos(0, 0, 0);
  Cylinder::RotationType rot;
  Cylinder::CylinderPointer myCylinder = Cylinder::build(pos, rot, rho);

  FreeTrajectoryState recoStart = freeTrajStateMuon(track);
  TrajectoryStateOnSurface recoProp;
  recoProp = propagatorAlong->propagate(recoStart, *myCylinder);
  if (!recoProp.isValid()) {
    recoProp = propagatorOpposite->propagate(recoStart, *myCylinder);
  }
  return recoProp;
}
