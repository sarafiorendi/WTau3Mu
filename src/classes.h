#define G__DICTIONARY

#include "DataFormats/Common/interface/Wrapper.h"
#include "CMGTools/WTau3Mu/interface/Tau3MuKalmanVertexFitter.h"
#include "CMGTools/WTau3Mu/interface/Tau3MuKinematicVertexFitter.h"

// #include "CMGTools/WTau3Mu/plugins/L1MuonRecoPropagator.h"
// #include "CMGTools/WTau3Mu/plugins/L1MuonRecoPropagator.cc"

#include "TLorentzVector.h"
#include "DataFormats/PatCandidates/interface/Muon.h"


namespace {
  struct CMGTools_WTau3Mu {
    Tau3MuKalmanVertexFitterProducer tau3muKalmanVtx_;
    Tau3MuKinematicVertexFitterProducer tau3muKinVtx_;

    std::vector<std::pair<const pat::Muon*, TLorentzVector> > mpmtlv;
    edm::Wrapper<std::vector<std::pair<const pat::Muon*, TLorentzVector> > > wmpmtlv; 
//     edm::helpers<std::vector<std::pair<const pat::Muon *, TLorentzVector>>> hmpmtlv; 

    std::pair<const pat::Muon*,TLorentzVector> ppmtlv;
    edm::Wrapper<std::pair<const pat::Muon*,TLorentzVector> > wppmtlv; 
//     edm::helpers<std::pair<const pat::Muon*,TLorentzVector> > hppmtlv; 

  };
}



