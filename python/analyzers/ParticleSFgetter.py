import json
from collections import OrderedDict

class ParticleSFgetter():
    def __init__(self, jsonFile, SFname, SFbins, usePtOnly):
        self.jsonFile = jsonFile
        self.particle = None

        self.usePtOnly = usePtOnly

        self.sffile = open(self.jsonFile, 'r')
        self.sf     = json.load(self.sffile, object_pairs_hook=OrderedDict)
        self.sfname = SFname
        self.sfbins = SFbins

    def getSF(self, particle):
        self.particle = particle

        pt  = self.particle.pt()

        ## if using 2D SFs (ptVSabseta)
        if not self.usePtOnly:
            eta  = self.particle.eta() 
            ieta = self.getEtaBin(eta)
            keta = self.sf[self.sfname][self.sfbins].keys()[ieta]
        ## else use first key as eta key (that should be '0.0, 2.4' and contain all the pt bins keys)
        else: keta = str(self.sf[self.sfname][self.sfbins].keys()[0])

        ipt = self.getPtBin(keta, pt)
        kpt = self.sf[self.sfname][self.sfbins][keta].keys()[ipt]
        
        sf = self.sf[self.sfname][self.sfbins][keta][kpt]
        
        return sf

    def getEtaBin(self, eta):
        ''' 
        Return the index of the key to which the muon eta belongs.
        '''
        etabins = self.sf[self.sfname][self.sfbins].keys()
        etabins = [ [float(str(i.split(':')[-1]).split(',')[0].replace('[','')),
                     float(str(i.split(':')[-1]).split(',')[1].replace(']',''))] for i in etabins]

        eta = abs(eta)
        for i, ibin in enumerate(etabins):
            if eta < ibin[0] or eta > ibin[1]:
                if i < (len(etabins)-1):
                    continue
            return i

    def getPtBin(self, keta, pt):
        ''' 
        Return the index of the key to which the muon pt belongs.
        If it goes beyond maximum it returns the last bin.
        If it sits lower than the minimum, it returns the first bin.
        '''
        ptbins = self.sf[self.sfname][self.sfbins][keta].keys()
        ptbins = [ [float(str(i.split(':')[-1]).split(',')[0].replace('[','')),
                    float(str(i.split(':')[-1]).split(',')[1].replace(']',''))] for i in ptbins] 

        for i, ibin in enumerate(ptbins):
            if i == 0 and pt < ibin[0]:
                return i
            if pt < ibin[0] or pt > ibin[1]:
                if i < (len(ptbins)-1):
                    continue
            return i

    ## return a dummy value (1 \pm 1) for muons out of the analysis categories ("even-not-soft muons")
    def getDummy(self):
        dmy = OrderedDict()
        dmy['value'] = 1
        dmy['error'] = 1
        
        return  dmy

