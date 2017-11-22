import ROOT
from CMGTools.WTau3Mu.analyzers.DsPhiMuMuPiTreeProducerBase import DsPhiMuMuPiTreeProducerBase
from PhysicsTools.HeppyCore.utils.deltar import deltaR

global muon_mass
muon_mass = 0.1056583745

class DsPhiMuMuPiTreeProducer(DsPhiMuMuPiTreeProducerBase):

    '''
    '''

    def declareVariables(self, setup):
        '''
        '''
        self.bookEvent(self.tree)
        self.bookDs(self.tree, 'ds')
        self.bookMuon(self.tree, 'mu1')
        self.bookMuon(self.tree, 'mu2')

        self.var(self.tree, 'hlt_doublemu3_trk_tau3mu')

    def process(self, event):
        '''
        '''
        self.readCollections(event.input)
        self.tree.reset()

        if not eval(self.skimFunction):
            return False

        self.fillEvent(self.tree, event)
        self.fillDs(self.tree, 'ds', event.ds)        
        self.fillMuon(self.tree, 'mu1', event.ds.mu1())
        self.fillMuon(self.tree, 'mu2', event.ds.mu2())

        # HLT bits & matches
        # self.fill(self.tree, 'hlt_doublemu3_trk_tau3mu', any('HLT_DoubleMu3_Trk_Tau3mu' in name for name in event.ds.hltmatched))
        # matching is broken here, revert back to simple trigger being fired or not
        fired_triggers = [info.name for info in getattr(event, 'trigger_infos', []) if info.fired]
        self.fill(self.tree, 'hlt_doublemu3_trk_tau3mu', any('HLT_DoubleMu3_Trk_Tau3mu' in name for name in fired_triggers))

        self.fillTree(event)

