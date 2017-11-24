#define G__DICTIONARY

#include "DataFormats/Common/interface/Wrapper.h"
#include "CMGTools/WTau3Mu/interface/Tau3MuKalmanVertexFitter.h"
#include "CMGTools/WTau3Mu/interface/Tau3MuKinematicVertexFitter.h"
#include "CMGTools/WTau3Mu/interface/DsPhiMuMuPiKinematicVertexFitter.h"

// #include "CMGTools/WTau3Mu/plugins/L1MuonRecoPropagator.h"
// #include "CMGTools/WTau3Mu/plugins/L1MuonRecoPropagator.cc"

#include "TLorentzVector.h"
#include "DataFormats/PatCandidates/interface/Muon.h"


namespace {
  struct CMGTools_WTau3Mu {
    Tau3MuKalmanVertexFitterProducer tau3muKalmanVtx_;
    Tau3MuKinematicVertexFitterProducer tau3muKinVtx_;
    DsPhiMuMuPiKinematicVertexFitterProducer dsphipiKinVtx_;

    std::pair<edm::Ptr<pat::Muon>,TLorentzVector> pppmtlv;
    edm::Wrapper<std::pair<edm::Ptr<pat::Muon>,TLorentzVector> > wpppmtlv;

    std::vector<std::pair<edm::Ptr<pat::Muon>,TLorentzVector> > vpppmtlv;
    edm::Wrapper<std::vector<std::pair<edm::Ptr<pat::Muon>,TLorentzVector> > > wvpppmtlv;

  };
}



