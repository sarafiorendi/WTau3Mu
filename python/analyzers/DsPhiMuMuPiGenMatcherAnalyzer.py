from copy import deepcopy as dc
import ROOT

from PhysicsTools.Heppy.analyzers.core.Analyzer   import Analyzer
from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle
from PhysicsTools.HeppyCore.utils.deltar          import deltaR, bestMatch

from CMGTools.WTau3Mu.physicsobjects.DsPhiMuMuPi  import DsPhiMuMuPi

class DsPhiMuMuPiGenMatcherAnalyzer(Analyzer):
    '''
    '''


    def declareHandles(self):
        super(DsPhiMuMuPiGenMatcherAnalyzer, self).declareHandles()
        
        self.mchandles['packedGenParticles'] = AutoHandle(
            'packedGenParticles',
            'std::vector<pat::PackedGenParticle>'
        )

    def process(self, event):
        if event.input.eventAuxiliary().isRealData():
            return True

        self.readCollections(event.input)
   
        # packed gen particles
        packed_gen_particles = self.mchandles['packedGenParticles'].product()
     
        # match the ds to gen ds
        dsphimumupi = self.cfg_ana.getter(event)
        
        # get all Ds in the event
        gends = [pp for pp in event.genParticles if abs(pp.pdgId())==431]

        if len(gends)>1:
            print 'more than one Ds!'
            import pdb ; pdb.set_trace()
        
        
        for ip in gends:            
            ip.final_daus = []
            for ipp in packed_gen_particles:
                mother = ipp.mother(0)
                if mother and self.isAncestor(gends, mother):
                    ip.final_daus.append(ipp)                 

            ids = [ipp.pdgId() for ipp in ip.final_daus if ipp.pdgId()!=22]
        
            if len(ids) != 3:
                if len(gends)==1:
                    print 'not a three body decay'
                    import pdb ; pdb.set_trace()
                continue
            
            if set(ids) & set([13, -13]) != set([13, -13]):
                if len(gends)==1:
                    print 'I wanted a muon pair'
                    import pdb ; pdb.set_trace()
                continue
        
            if 211 not in set(ids) and -211 not in set(ids):
                if len(gends)==1:
                    print 'missing my pion'
                    import pdb ; pdb.set_trace()
                continue
            
            mygends = ip

        '''
        # restrict to only those that decay into phi pi
        gends = [pp for pp in gends if pp.numberOfDaughters()==2 and (len(set([333, 211]) & set([abs(pp.daughter(0).pdgId()), abs(pp.daughter(1).pdgId())]))==2)]
        
        # append to the event the gen level Ds Phi Mu Mu Phi with the highest momentum
        gends.sort(key = lambda x : x.pt(), reverse=True)
        try:
            mygends = gends[0]  
        except:
            import pdb ; pdb.set_trace()
        mygends.phip = [dau for dau in [mygends.daughter(ii)      for ii in range(mygends.numberOfDaughters())     ] if abs(dau.pdgId())==333][0]  
        mygends.pi   = [dau for dau in [mygends.daughter(ii)      for ii in range(mygends.numberOfDaughters())     ] if abs(dau.pdgId())==211][0]  
        mygends.mum  = [mu  for mu  in [mygends.phip.daughter(ii) for ii in range(mygends.phip.numberOfDaughters())] if     mu .pdgId() == 13][0]  
        mygends.mup  = [mu  for mu  in [mygends.phip.daughter(ii) for ii in range(mygends.phip.numberOfDaughters())] if     mu .pdgId() ==-13][0]  
        event.gends  = DsPhiMuMuPi([mygends.mum, mygends.mup], mygends.pi)
        event.ngends = len(gends)
                
        # match the reco candidate to the gen Ds
        best_match, dRmin = bestMatch(dsphimumupi, gends)
        ds_match = best_match if dRmin < 0.3 else None
        if ds_match:
            ds_match.phip = [pp for pp in [ds_match.daughter(0), ds_match.daughter(1)] if pp.pdgId()==333][0]
                    
        muons = [dsphimumupi.mu1(), dsphimumupi.mu2()]          
        
        # now match the two muons and the pion: 
        #    first try to match to any stable gen particle
        stableGenParticles = [pp for pp in event.genParticles if pp.status()==1]
        for mu in muons + [dsphimumupi.pi()]:
            best_match, dRmin = bestMatch(mu, stableGenParticles)
            if dRmin < 0.1:
                mu.genp = best_match
            
        #     then match to phi daughters
        #     but only if the reco ds is matched to a gen ds itself
        if ds_match:
            # append the gen ds to the event
            event.ds.genp = ds_match
            muons_from_phi = [mu for mu in [ds_match.phip.daughter(ii) for ii in range(ds_match.phip.numberOfDaughters())] if abs(mu.pdgId())==13]
            for mu in muons_from_phi:
                best_match, dRmin = bestMatch(mu, muons)
                if dRmin < 0.1:
                    best_match.genp = mu
        
        neutrinos = [pp for pp in event.genParticles if abs(pp.pdgId()) in [12, 14, 16] and pp.status()==1]
        
        for i, nn in enumerate(neutrinos):
            if i==0:
                event.genmet = nn.p4()
            else:
                event.genmet += nn.p4()
        '''
        return True
    
    @staticmethod
    def finalDaughters(gen, daughters=None):
        if daughters is None:
            daughters = []
        for i in range(gen.numberOfDaughters()):
            daughter = gen.daughter(i)
            if daughter.numberOfDaughters() == 0:
                daughters.append(daughter)
            else:
                DsPhiMuMuPiGenMatcherAnalyzer.finalDaughters(daughter, daughters)
        return daughters


    @staticmethod
    def isAncestor(a, p):
        if a == p :
            return True
        for i in xrange(0,p.numberOfMothers()):
            if DsPhiMuMuPiGenMatcherAnalyzer.isAncestor(a,p.mother(i)):
                return True
        return False

