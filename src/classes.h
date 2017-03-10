#define G__DICTIONARY

#include "DataFormats/Common/interface/Wrapper.h"
#include "CMGTools/WTau3Mu/interface/Tau3MuKalmanVertexFitter.h"
#include "CMGTools/WTau3Mu/interface/Tau3MuKinematicVertexFitter.h"

namespace {
  struct CMGTools_WTau3Mu {
    Tau3MuKalmanVertexFitterProducer tau3muKalmanVtx_;
    Tau3MuKinematicVertexFitterProducer tau3muKinVtx_;
  };
}
