import json
import ROOT
from itertools import product

from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle

import PhysicsTools.HeppyCore.framework.config as cfg

class MuonWeighterAnalyzer(Analyzer):

    def __init__(self, *args, **kwargs):
        super(MuonWeighterAnalyzer, self).__init__(*args, **kwargs)

    def beginLoop(self, setup):
        super(MuonWeighterAnalyzer, self).beginLoop(setup)
        self.sffile = open(self.cfg_ana.sffile, 'r')
        self.sf     = json.load(self.sffile)
        self.sfname = self.cfg_ana.sfname
        self.etabins = self.sf['%s_PtEtaBins' %self.sfname]['abseta_pt_ratio'].keys()
        self.etabins = [ [float(str(i.split(':')[-1]).split(',')[0].replace('[','')),
                          float(str(i.split(':')[-1]).split(',')[1].replace(']',''))] for i in self.etabins] 
        self.etabins.sort(key = lambda x : x[0])

        
    def process(self, event):
        self.readCollections(event.input)
        
        muons = self.cfg_ana.getter(event)
    
        for imu in muons:
            imu.idweight    = self.getSF(imu)['value']
            imu.idweightunc = self.getSF(imu)['error']

            if hasattr(imu, 'weight'):
                imu.weight *= imu.idweight
            else:
                imu.weight = imu.idweight

            if getattr(self.cfg_ana, 'multiplyEventWeight', True):
                if hasattr(event, 'eventWeight'):
                    event.eventWeight *= imu.idweight
                else:
                    event.eventWeight = imu.idweight

        return True                

    def getSF(self, mu):
        pt = mu.pt()
        eta = mu.eta()

        ieta = self.getEtaBin(eta)
        if ieta is None:
            import pdb ; pdb.set_trace()
        keta = self.sf['%s_PtEtaBins' %self.sfname]['abseta_pt_ratio'].keys()[ieta]

        ipt = self.getPtBin(keta, pt)
        if ipt is None:
            import pdb ; pdb.set_trace()
        kpt = self.sf['%s_PtEtaBins' %self.sfname]['abseta_pt_ratio'][keta].keys()[ipt]
        
        sf = self.sf['%s_PtEtaBins' %self.sfname]['abseta_pt_ratio'][keta][kpt]
        
        return sf
                
    def getEtaBin(self, eta):
        ''' 
        Return the index of the key to which the muon eta belongs.
        '''
        eta = abs(eta)
        for i, ibin in enumerate(self.etabins):
            if eta < ibin[0] or eta > ibin[1]:
                if i < (len(self.etabins)-1):
                    continue
            return i

    def getPtBin(self, keta, pt):
        ''' 
        Return the index of the key to which the muon pt belongs.
        If it goes beyond maximum it returns the last bin.
        If it sits lower than the minimum, it returns the first bin.
        '''
        ptbins = self.sf['%s_PtEtaBins' %self.sfname]['abseta_pt_ratio'][keta].keys()
        ptbins = [ [float(str(i.split(':')[-1]).split(',')[0].replace('[','')),
                    float(str(i.split(':')[-1]).split(',')[1].replace(']',''))] for i in ptbins] 
        ptbins.sort(key = lambda x : x[0])

        for i, ibin in enumerate(ptbins):
            if i == 0 and pt < ibin[0]:
                return i
            if pt < ibin[0] or pt > ibin[1]:
                if i < (len(ptbins)-1):
                    continue
            return i
            
            
        
        
    def endLoop(self, setup):
        super(MuonWeighterAnalyzer, self).endLoop(setup)
        self.sffile.close()


setattr(MuonWeighterAnalyzer, 'defaultConfig', 
    cfg.Analyzer(
        class_object=MuonWeighterAnalyzer,
        getter = lambda event : [event.tau3muRefit.mu1(), event.tau3muRefit.mu2(), event.tau3muRefit.mu3()],
    )
)
