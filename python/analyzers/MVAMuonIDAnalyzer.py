import ROOT
import math
import array
import os

from PhysicsTools.Heppy.analyzers.core.Analyzer     import Analyzer
from PhysicsTools.Heppy.analyzers.core.AutoHandle   import AutoHandle

class MVAMuonIDAnalyzer (Analyzer):
    
    def beginLoop(self, setup):
        super(MVAMuonIDAnalyzer, self).beginLoop(setup)
        
        self.counters.addCounter('TMVA')
        count = self.counters.counter('TMVA')
        count.register('all muons')
        count.register('all events')

        count.register('hasOuterTrack')
        count.register('is outer-null')
        count.register('isStandAloneMuon')
        count.register('hasOuterChi2')
        count.register('hasOuterCharge')

        count.register('hasGlobalTrack')
        count.register('is global-null')
        count.register('isGlobalMuon')
        count.register('hasGlobalHitPattern')
        
        count.register('isTrackerMuon')
        
        count.register('has global and outer but outer is null')
        count.register('has global and outer but global is null')

        count.register('isPFMuon')
        
        #the reader has to be initialized only when the loop begins
        xml_pathBB = '/'.join([os.environ['CMSSW_BASE'], 'src', 'CMGTools', 'WTau3Mu', 'data', 'muonID', self.cfg_ana.xml_pathBB])
        xml_pathEC = '/'.join([os.environ['CMSSW_BASE'], 'src', 'CMGTools', 'WTau3Mu', 'data', 'muonID', self.cfg_ana.xml_pathEC])       
        self.var = []
        self.spe = []
        self.readerBB = ROOT.TMVA.Reader("Silent")
        self.readerEC = ROOT.TMVA.Reader("Silent")
        
        #reader and variables initialization
        for i in range(0, 14):
            self.var.append(array.array('f', [0]))
        for i in range(0, 4):
            self.spe.append(array.array('f', [0]))
            
        var_list_v25 = [
            "segComp",
            "chi2LocMom",
            "chi2LocPos",
            "glbTrackTailProb",
            "iValFrac",
            "LWH",
            "kinkFinder",
            "TMath::Log(2+glbKinkFinder)",
            "timeAtIpInOutErr",
            "outerChi2",
            "innerChi2",
            "trkRelChi2",
            "vMuonHitComb",
            "Qprod"
        ]
        var_list_v19 = [
            "segComp",
            "chi2LocMom",
            "chi2LocPos",
            "glbTrackTailProb",
            "iValFrac",
            "LWH",
            "kinkFinder",
            "glbKinkFinder",
            "timeAtIpInOutErr",
            "outerChi2",
            "innerChi2",
            "trkRelChi2",
            "vMuonHitComb"
        ]
        spe_list_v25 = [    #used only in version 25
            "pID",
            "pt",
            "eta",
            "MomID"
        ]        
        for ll, vv in zip(var_list_v25, self.var):
            self.readerBB.AddVariable(ll, vv)       

        for ll, vv in zip(var_list_v19, self.var):
            self.readerEC.AddVariable(ll, vv)
        #    self.readerBB.AddVariable(ll, vv) 

        for ll, ss in zip(spe_list_v25, self.spe):
            self.readerBB.AddSpectator(ll, ss)

        self.readerBB.BookMVA("BDT", xml_pathBB)
        self.readerEC.BookMVA("BDT", xml_pathEC)


    #from https://github.com/Bmm4/Bmm/blob/master/RootAnalysis/macros/candAna.cc#L2861-L2960
    def passPreSelection(self, mu):
        return  (
            (mu.combinedQuality().chi2LocalMomentum <= 5000)    and\
            (mu.combinedQuality().chi2LocalPosition <= 2000)    and\
            (mu.combinedQuality().glbTrackProbability <= 5000)  and\
            (mu.combinedQuality().trkKink  <= 900)              and\
            (math.log(2+mu.combinedQuality().glbKink) <= 50)    and\
            (mu.time().timeAtIpInOutErr <= 4)                   and\
            (hasattr(mu, 'outerTrack')                  and\
             hasattr(mu.outerTrack(), 'normalizedChi2') and\
             mu.outerTrack().normalizedChi2() <= 1000)          and\
            (hasattr(mu, 'globalTrack'))                        and\
            (mu.innerTrack().normalizedChi2() <= 10)            and\
            (mu.combinedQuality().trkRelChi2 <= 3)              and\
            (hasattr(mu, 'globalTrack')                 and\
             hasattr(mu.globalTrack(), 'hitPattern'))
        )

    #from https://github.com/Bmm4/Bmm/blob/master/CmsswAnalysis/src/HFBDT.cc#L343
    def vMuonHitComb(self, mu):
        dt1=0; dt2=0; dt3=0; dt4=0
        rpc1=0; rpc2=0; rpc3=0; rpc4=0
        csc1=0; csc2=0; csc3=0; csc4=0

        pattern = mu.globalTrack().hitPattern()
       
        for i in range(0, pattern.numberOfHits(ROOT.reco.HitPattern.TRACK_HITS)):
            hit = pattern.getHitPattern(ROOT.reco.HitPattern.TRACK_HITS, i)
            if pattern.validHitFilter(hit) != 1: continue
            if pattern.getMuonStation(hit)   == 1:
                if pattern.muonDTHitFilter(hit) : dt1  = dt1 +1
                if pattern.muonRPCHitFilter(hit): rpc1 = rpc1+1
                if pattern.muonCSCHitFilter(hit): csc1 = csc1+1
            elif pattern.getMuonStation(hit) == 2:
                if pattern.muonDTHitFilter(hit) : dt2  = dt2 +1
                if pattern.muonRPCHitFilter(hit): rpc2 = rpc2+1
                if pattern.muonCSCHitFilter(hit): csc2 = csc2+1
            elif pattern.getMuonStation(hit) == 3:
                if pattern.muonDTHitFilter(hit) : dt3  = dt3 +1
                if pattern.muonRPCHitFilter(hit): rpc3 = rpc3+1
                if pattern.muonCSCHitFilter(hit): csc3 = csc3+1
            elif pattern.getMuonStation(hit) == 4:
                if pattern.muonDTHitFilter(hit) : dt4  = dt4 +1  
                if pattern.muonRPCHitFilter(hit): rpc4 = rpc4+1
                if pattern.muonCSCHitFilter(hit): csc4 = csc4+1     

        comb = (dt1+dt2+dt3+dt4)/2. + (rpc1+rpc2+rpc3+rpc4)
        comb = comb+6 if csc1>6 else comb+csc1
        comb = comb+6 if csc2>6 else comb+csc2
        comb = comb+6 if csc3>6 else comb+csc3
        comb = comb+6 if csc4>6 else comb+csc4

        return comb

    def process(self, event):
        self.readCollections(event.input)
        count = self.counters.counter('TMVA')
        muons = [event.tau3mu.mu1(), event.tau3mu.mu2(), event.tau3mu.mu3()]
        muonsRefit = [event.tau3muRefit.mu1(), event.tau3muRefit.mu2(), event.tau3muRefit.mu3()]

        #gen match the non-refitted muons
        for mm, mr in zip(muons, muonsRefit):
            if hasattr(mr, 'genp'): mm.genp = mr.genp
            mm.BDTvalue = -1
            mr.BDTvalue = -1

        count.inc('all events')
        #muon tracks counters
        for mu in event.muons:
            count.inc("all muons")
            if hasattr(mu, 'outerTrack')                    : count.inc("hasOuterTrack")
            if hasattr(mu.outerTrack(), 'normalizedChi2')   : count.inc("hasOuterChi2")
            if hasattr(mu.outerTrack(), 'charge')           : count.inc("hasOuterCharge")
            if hasattr(mu, 'globalTrack')                   : count.inc("hasGlobalTrack")
            if hasattr(mu.globalTrack(), 'hitPattern')      : count.inc("hasGlobalHitPattern")
            if hasattr(mu, 'outerTrack')  and\
               mu.outerTrack().isNull()                     : count.inc("is outer-null")
            if hasattr(mu, 'globalTrack') and\
               mu.globalTrack().isNull()                    : count.inc("is global-null")
            if hasattr(mu, 'globalTrack') and\
               hasattr(mu, 'outerTrack')  and\
               mu.outerTrack().isNull()                     : count.inc('has global and outer but outer is null')
            if hasattr(mu, 'globalTrack') and\
               hasattr(mu, 'outerTrack')  and\
               mu.globalTrack().isNull()                    : count.inc('has global and outer but global is null')

            if mu.isGlobalMuon()    : count.inc('isGlobalMuon')
            if mu.isTrackerMuon()   : count.inc('isTrackerMuon')                       
            if mu.isStandAloneMuon(): count.inc('isStandAloneMuon')            
            if mu.isPFMuon()        : count.inc('isPFMuon')

        # compute the BDT value for both pre- and post-refit muons, as the score can slightly change
        for mu in muons + muonsRefit:
            if not self.passPreSelection(mu): continue
            mu.segComp          = self.var[0][0] = mu.segmentCompatibility()
            mu.chi2LocMom       = self.var[1][0] = mu.combinedQuality().chi2LocalMomentum
            mu.chi2LocPos       = self.var[2][0] = mu.combinedQuality().chi2LocalPosition
            mu.glbTrackTailProb = self.var[3][0] = mu.combinedQuality().glbTrackProbability
            mu.iValFrac         = self.var[4][0] = mu.innerTrack().validFraction()
            mu.LHW              = self.var[5][0] = mu.innerTrack().hitPattern().trackerLayersWithMeasurement()
            mu.kinkFinder       = self.var[6][0] = mu.combinedQuality().trkKink
            mu.glbKinkFinder    = self.var[7][0] = mu.combinedQuality().glbKink #different between versions 19 and 25
            mu.timeAtIpInOutErr = self.var[8][0] = mu.time().timeAtIpInOutErr    
            mu.outerChi2        = self.var[9][0] = mu.outerTrack().normalizedChi2()
            mu.innerChi2        = self.var[10][0]= mu.innerTrack().normalizedChi2() 
            mu.trkRelChi2       = self.var[11][0]= mu.combinedQuality().trkRelChi2 
            mu.vMuonHitComb     = self.var[12][0]= self.vMuonHitComb(mu)
            mu.Qprod            = self.var[13][0]= (mu.innerTrack().charge()*mu.outerTrack().charge()) #not used in version 19
            #barrel muons
            if abs(mu.eta()) < 1.6:
                mu.LogGlbKinkFinder = self.var[7][0] = math.log(2+mu.combinedQuality().glbKink)
                mu.glbKinkFinder    = -99 #this is a variable for endcaps only
                #barrel spectators
                self.spe[0][0] = 0  #not set
                self.spe[1][0] = mu.pt()
                self.spe[2][0] = mu.eta()
                self.spe[3][0] = 0  #not set
                mu.BDTvalue = self.readerBB.EvaluateMVA("BDT")
            #endcap muons
            else:
                mu.BDTvalue = self.readerEC.EvaluateMVA("BDT")

        return True