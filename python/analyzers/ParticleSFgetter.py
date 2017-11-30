import json

class ParticleSFgetter():
    def __init__(self, jsonFile, SFname = "medium2016_GH", SFbins = 'Pt_Eta'):
        self.jsonFile = jsonFile
        self.particle = None

        self.sffile = open(self.jsonFile, 'r')
        self.sf     = json.load(self.sffile)
        self.sfname = SFname
        self.sfbins = SFbins

    def getSF(self, particle):
        self.particle = particle

        pt  = self.particle.pt()
        eta = self.particle.eta()

        ieta = self.getEtaBin(eta)
        keta = self.sf[self.sfname][self.sfbins].keys()[ieta]

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