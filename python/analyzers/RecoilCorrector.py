import math

# this needs to stay on top, otherwise it'll complain for some reason
# *** TypeError: HTTRecoilCorrector::HTTRecoilCorrector() =>
#     takes at most 0 arguments (1 given)
from ROOT import gSystem
gSystem.Load('libCMGToolsH2TauTau')
from ROOT import HTTRecoilCorrector as RC

from ROOT.Math import LorentzVector
from PhysicsTools.Heppy.analyzers.core.Analyzer       import Analyzer
from PhysicsTools.Heppy.analyzers.core.AutoHandle     import AutoHandle

from PhysicsTools.HeppyCore.utils.deltar              import cleanObjectCollection, matchObjectCollection
from PhysicsTools.Heppy.physicsobjects.PhysicsObjects import Jet
from CMGTools.WTau3Mu.analyzers.GenMatcherAnalyzer    import GenMatcherAnalyzer
from CMGTools.H2TauTau.proto.analyzers.HTTGenAnalyzer import HTTGenAnalyzer

p4sum = HTTGenAnalyzer.p4sum

class RecoilCorrector(Analyzer):
    '''
    Corrects MVA/PF MET recoil.
    See Alexei's talk here 
    https://indico.cern.ch/event/562201/contributions/2298907/attachments/1334012/2014168/Recoil_20160910.pdf
    https://github.com/CMS-HTT/RecoilCorrections/blob/master/data/TypeI-PFMet_Run2016BtoH.root
    '''

    def __init__(self, cfg_ana, cfg_comp, looperName):
        super(RecoilCorrector, self).__init__(cfg_ana, cfg_comp, looperName)

        # Instantiate a Recoil Corrector
        self.rcPFMET = RC(self.cfg_ana.pfMetRCFile)

    def declareHandles(self):
        super(RecoilCorrector, self).declareHandles()

        self.handles['jets'] = AutoHandle(
            'slimmedJets',
            'vector<pat::Jet>'
        )

    @staticmethod
    def getGenP4(boson):

        daughters = GenMatcherAnalyzer.finalDaughters(boson)
        
        visible_daughters = [dd for dd in daughters if abs(dd.pdgId()) not in (12,14,16)] 
        
        if len(visible_daughters) == 0 or len(daughters) == 0:
            return 0., 0., 0., 0.

        p4 = boson.p4()
        p4_vis = p4sum(visible_daughters)

        return p4.px(), p4.py(), p4_vis.px(), p4_vis.py()


    def process(self, event):
        if not self.cfg_comp.isMC:
            return
        
        # Calculate recoil correction only if the three final muons 
        # come from the tau which comes from the W
        if not hasattr(event, 'genw'):
            return

        # read the jet collection and count
        # build the jets as prescribed by Alexei
        self.readCollections(event.input)
        event.jets = [Jet(jj) for jj in self.handles['jets'].product()]

        event.cleanJets, _ = cleanObjectCollection(
            event.jets,
            masks = event.muons + event.electrons, # clean from leptons as prescribed (see Tau3Mu analyzer)
            deltaRMin = 0.5
        )

        event.cleanJets30 = [jet for jet in event.cleanJets if jet.pt()>30                 and\
                                                               abs(jet.eta())<4.7          and\
                                                               jet.jetID("POG_PFID_Loose") and\
                                                               jet.puJetId()                   ]

        n_jets_30 = len(event.cleanJets30)

        # Calculate generator four-momenta even if not applying corrections
        # to save them in final trees
        gen_w_px, gen_w_py, gen_vis_w_px, gen_vis_w_py = self.getGenP4(event.genw)
        
        # Correct PF MET
        pfmet_px_old = event.pfmet.px()
        pfmet_py_old = event.pfmet.py()
    
        # Correct by mean and resolution as default (otherwise use .Correct(..))
        new = self.rcPFMET.CorrectByMeanResolution(
            pfmet_px_old, 
            pfmet_py_old, 
            gen_w_px,    
            gen_w_py,    
            gen_vis_w_px,    
            gen_vis_w_py,    
            n_jets_30,   
        )
    
        px_new, py_new = new.first, new.second

        newmet = LorentzVector("ROOT::Math::PxPyPzE4D<double>")(
            px_new, 
            py_new, 
            0., 
            math.sqrt(px_new*px_new + py_new*py_new)
        )
        
#         print '\n\n==========================================================================='
#         print 'gen MET pt                                ', event.genmet.pt()
#         print 'gen MET phi                               ', event.genmet.phi()
#         print '=========='
#         print '         tau3mu MET before corrections pt ', event.tau3mu.met().pt()
#         print '         tau3mu MET before corrections phi', event.tau3mu.met().phi()
#         print '         tau3mu mT  before corrections    ', event.tau3mu.mttau()

        event.pfmet.setP4(newmet)

        return True