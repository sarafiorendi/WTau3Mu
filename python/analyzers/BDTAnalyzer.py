import os
# we want to import the most recent scikit learn from our local installation
import sys
sys.path.insert(0, os.environ['HOME'] + '/.local/lib/python2.7/site-packages')
import numpy as np
from ROOT import TMath
from sklearn.externals import joblib

from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer

class BDTAnalyzer(Analyzer):

    def beginLoop(self, setup):
        super(BDTAnalyzer, self).beginLoop(setup)
        print 'loading BDT classifier...'
        self.classifier = joblib.load(os.environ['CMSSW_BASE'] + '/src/CMGTools/WTau3Mu/data/classifier.pkl')
        print '...done'
    
    def process(self, event):
        self.readCollections(event.input)

        cand = event.tau3muRefit
        vtx  = cand.refittedVertex
        
        if cand.mu1().muonID('POG_ID_Tight'):
            mu1ID = 2
        elif cand.mu1().isSoftMuon(cand.mu1().associatedVertex):
            mu1ID = 1
        else:
            mu1ID = 0

        if cand.mu2().muonID('POG_ID_Tight'):
            mu2ID = 2
        elif cand.mu2().isSoftMuon(cand.mu2().associatedVertex):
            mu2ID = 1
        else:
            mu2ID = 0

        if cand.mu3().muonID('POG_ID_Tight'):
            mu3ID = 2
        elif cand.mu3().isSoftMuon(cand.mu3().associatedVertex):
            mu3ID = 1
        else:
            mu3ID = 0
           
        event_variables = np.array([
            cand.tau_dBetaIsoCone0p8strength0p2_rel                 ,
            cand.mttau()                                            ,
            cand.p4Muons().pt()                                     ,
            cand.dRtauMET()                                         ,
            cand.dRtauMuonMax()                                     ,
            TMath.Prob(vtx.chi2(), int(vtx.ndof()))                 ,
            vtx.ls                                                  ,
            vtx.cos                                                 ,
            cand.mu1().relIsoR(R=0.4, dBetaFactor=0.5, allCharged=0),
            cand.mu2().relIsoR(R=0.4, dBetaFactor=0.5, allCharged=0),
            cand.mu3().relIsoR(R=0.4, dBetaFactor=0.5, allCharged=0),
            cand.met().pt()                                         ,
            int(mu1ID)                                              ,
            int(mu2ID)                                              ,
            int(mu3ID)                                              ,
        ])
        
        # import pdb ; pdb.set_trace()
                
        try:
            event.bdt_proba    = float(self.classifier.predict_proba    (event_variables.reshape(1, -1))[:,1][0])
            event.bdt_decision = float(self.classifier.decision_function(event_variables.reshape(1, -1))[0])
        except:
            event.bdt_proba    = -99.
            event.bdt_decision = -99.
