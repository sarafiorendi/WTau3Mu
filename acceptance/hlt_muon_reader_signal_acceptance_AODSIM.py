import ROOT
from DataFormats.FWLite import Events, Handle
from PhysicsTools.HeppyCore.utils.deltar import deltaR, deltaPhi
from itertools import product, combinations, groupby
from collections import OrderedDict
from math import cos, cosh, sqrt
from array import array
from seeds import single_muon, di_muon, tri_muon
import numpy as np


def isSoftMuon(muon, vtx):
    '''
    porting of https://github.com/cms-sw/cmssw/blob/master/DataFormats/MuonReco/src/MuonSelectors.cc#L871-L885
    
    missing pieces, but fuck
    '''  
    muID = muon.isMatchesValid() and muon.isTrackerMuon()
  
    layers = muon.innerTrack().hitPattern().trackerLayersWithMeasurement() > 5 and \
             muon.innerTrack().hitPattern().pixelLayersWithMeasurement() > 0

    ishighq = muon.innerTrack().quality(ROOT.reco.Track.highPurity) 
  
    ip = abs(muon.innerTrack().dxy(vtx.position())) < 0.3 and \
         abs(muon.innerTrack().dz(vtx.position()))  < 20.
  
    return muID and layers and ip and ishighq



# ROOT.gROOT.SetBatch()
ROOT.gStyle.SetOptStat(0)

# events = Events('outputFULL.root')
events = Events([
    '/afs/cern.ch/work/m/manzoni/tauHLT/2017/CMSSW_9_2_4/src/HLTrigger/Configuration/test/jian/outputFULL.root',
])

handle_muons   = Handle ('std::vector<reco::Muon>')
label_muons    = ('muons')

handle_gen     = Handle('vector<reco::GenParticle>')
label_gen      = ('genParticles')

handle_trig    = Handle('edm::TriggerResults')
label_trig     = ('TriggerResults','','MYHLT')

handle_vtx     = Handle('std::vector<reco::Vertex>')
label_vtx      = ('offlinePrimaryVertices','','RECO')

handle_global  = Handle('vector<reco::RecoChargedCandidate>')
label_global   = ('hltGlbTrkMuonLowPtIter01MergeCands') 

handle_L1muons = Handle('BXVector<l1t::Muon>')
label_L1muon   = ('gmtStage2Digis', 'Muon') 

passed            = 0
in_the_acceptance = 0

totevents = events.size()

ric     = 0
jian    = 0
noiso   = 0
anytrig = 0

f1 = ROOT.TFile('tau3mu_jian_tuple.root', 'recreate')

branches = [
    'run',
    'lumi',
    'event',
    'mu1_off_pt',
    'mu1_off_eta',
    'mu1_off_phi',
    'mu1_off_vz',
    'mu2_off_pt',
    'mu2_off_eta',
    'mu2_off_phi',
    'mu2_off_vz',
    'mu3_off_pt',
    'mu3_off_eta',
    'mu3_off_phi',
    'mu3_off_vz',
    'dR_off_12',
    'dR_off_13',
    'dR_off_23',
    'mass_off_12',
    'mass_off_13',
    'mass_off_23',
    'tau_off_mass',
    'tau_off_pt',
    'tau_off_eta',
    'tau_off_phi',
    'tau_off_charge',
    'mu1_gen_pt',
    'mu1_gen_eta',
    'mu1_gen_phi',
    'mu2_gen_pt',
    'mu2_gen_eta',
    'mu2_gen_phi',
    'mu3_gen_pt',
    'mu3_gen_eta',
    'mu3_gen_phi',
    'mu1_hlt_pt',
    'mu1_hlt_eta',
    'mu1_hlt_phi',
    'mu1_hlt_vz',
    'mu2_hlt_pt',
    'mu2_hlt_eta',
    'mu2_hlt_phi',
    'mu2_hlt_vz',
    'mu3_hlt_pt',
    'mu3_hlt_eta',
    'mu3_hlt_phi',
    'mu3_hlt_vz',
    'dR_hlt_12',
    'dR_hlt_13',
    'dR_hlt_23',
    'mass_hlt_12',
    'mass_hlt_13',
    'mass_hlt_23',
    'tau_hlt_mass',
    'tau_hlt_pt',
    'tau_hlt_eta',
    'tau_hlt_phi',
    'tau_hlt_charge',
#     'HLT_DoubleMu3_Trk_Tau3mu_newMuonReco_v1', 
#     'HLT_WTau3Mu_Mu5_Mu1_TrkMu0_TauIso_v1', 
#     'HLT_WTau3Mu_Mu5_Mu1_TrkMu0_v1',
]
hlts = [
    'HLT_IsoMu27_v10',
    'HLT_DoubleMu3_Trk_Tau3mu_newMuonReco_v1',
    'HLT_Tau3Mu_Mu5_Mu1_TkMu1_IsoTau10_v1',
    'HLT_Tau3Mu_Mu5_Mu1_TkMu1_IsoTau10_Iter0and1_v1',
    'HLT_Tau3Mu_Mu5_Mu1_TkMu1_IsoTau10_Iter0and1_merge_v1',
    'HLT_Tau3Mu_Mu5_Mu1_TkMu1_IsoTau10_TauCharge1_v1',
    'HLT_Tau3Mu_Mu5_Mu1_TkMu1_Tau10_v1',
    'HLT_Tau3Mu_Mu5_Mu1_TkMu1_Tau10_TauCharge1_v1',
]
seeds    = [
    'L1_SingleMu_22_eta2p1_Q12'                         ,
      
    'L1_SingleMu_25_Q12'                                ,
      
    'L1_DoubleMu_15_7_Q8'                               ,
      
    'L1_DoubleMu_12_0_Q12_maxMass4p0'                   ,
    'L1_DoubleMu_10_1_Q12_maxMass4p0'                   ,
    'L1_DoubleMu_9_1_Q12_maxMass4p0'                    ,
    'L1_DoubleMu_8_3_Q12_maxMass4p0'                    ,
    'L1_DoubleMu_6_2_Q12_maxMass4p0'                    ,
    'L1_DoubleMu_5_3_Q12_maxMass4p0'                    ,
      
    'L1_DoubleMu_12_0_Q8_maxMass4p0'                    ,
    'L1_DoubleMu_10_1_Q8_maxMass4p0'                    ,
    'L1_DoubleMu_9_1_Q8_maxMass4p0'                     ,
    'L1_DoubleMu_8_3_Q8_maxMass4p0'                     ,
    'L1_DoubleMu_6_2_Q8_maxMass4p0'                     ,
    'L1_DoubleMu_5_3_Q8_maxMass4p0'                     ,
      
    'L1_DoubleMu_12_0_Q12_maxMass4p0_OS'                ,
    'L1_DoubleMu_10_1_Q12_maxMass4p0_OS'                ,
    'L1_DoubleMu_9_1_Q12_maxMass4p0_OS'                 ,
    'L1_DoubleMu_8_3_Q12_maxMass4p0_OS'                 ,
    'L1_DoubleMu_6_2_Q12_maxMass4p0_OS'                 ,
    'L1_DoubleMu_5_3_Q12_maxMass4p0_OS'                 ,
      
    'L1_DoubleMu_12_0_Q8_maxMass4p0_OS'                 ,
    'L1_DoubleMu_10_1_Q8_maxMass4p0_OS'                 ,
    'L1_DoubleMu_9_1_Q8_maxMass4p0_OS'                  ,
    'L1_DoubleMu_8_3_Q8_maxMass4p0_OS'                  ,
    'L1_DoubleMu_6_2_Q8_maxMass4p0_OS'                  ,
    'L1_DoubleMu_5_3_Q8_maxMass4p0_OS'                  ,
      
    'L1_DoubleMu0er1p5_SQ_OS_dR_Max1p4'                 ,
    'L1_DoubleMu4_SQ_OS_dR_Max1p2'                      ,
    'L1_DoubleMu4p5_SQ_OS_dR_Max1p2'                    ,
      
    'L1_TripleMu_4_4_4'                                 ,
    'L1_TripleMu_5_3_3'                                 ,
    'L1_TripleMu_5_5_3'                                 ,
    'L1_TripleMu3_SQ'                                   ,
    'L1_TripleMu_5SQ_3SQ_0OQ'                           ,
    'L1_TripleMu_5_3_0_DoubleMu_5_3_OS_Mass_Max17'      ,
    'L1_TripleMu_5SQ_3SQ_0_DoubleMu_5_3_SQ_OS_Mass_Max9',
]

ntuple = ROOT.TNtuple('tree', 'tree', ':'.join(branches+hlts+seeds))

tofill = OrderedDict(zip(branches, [-99.]*len(branches+hlts+seeds)))         

for i, event in enumerate(events):
    if i%100==0:
        print '===> processing %d / %d event' %(i, totevents)
    
    for k, v in tofill.iteritems():
        tofill[k] = -99.
    
    tofill['run'  ] = event.eventAuxiliary().run()
    tofill['lumi' ] = event.eventAuxiliary().luminosityBlock()
    tofill['event'] = event.eventAuxiliary().event()
    
    try:
        event.getByLabel (label_global, handle_global)
        allmuons = handle_global.product()
    except:
        allmuons = []
        pass

    event.getByLabel (label_gen, handle_gen)
    gen_particles = handle_gen.product()

    event.getByLabel (label_vtx, handle_vtx)
    vertices = handle_vtx.product()

    event.getByLabel (label_muons, handle_muons)
    muons = handle_muons.product()
#     muons = [mu for mu in muons if mu.isLooseMuon() and abs(mu.eta())<2.5 and mu.pt()>1.]
#     muons = [mu for mu in muons if mu.isMediumMuon() and abs(mu.eta())<2.5 and mu.pt()>1.]
#     import pdb ; pdb.set_trace()
#     muons = [mu for mu in muons if isSoftMuon(mu, vertices[0]) and abs(mu.eta())<2.5 and mu.pt()>1.]

    muons = [mu for mu in muons if mu.isPFMuon() and (mu.isGlobalMuon() or mu.isTrackerMuon()) and mu.numberOfMatches(ROOT.reco.Muon.NoArbitration)>0]

    # at least one match in the outer system
#     if any(mm.numberOfMatches(ROOT.reco.Muon.NoArbitration) == 0 for mm in muons):
#         import pdb ; pdb.set_trace()

    gen_muons = [pp for pp in gen_particles if abs(pp.pdgId())==13 and abs(pp.mother().pdgId())==15]
    gen_taus  = [pp for pp in gen_particles if abs(pp.pdgId())==15]
    
    normalTau = 0
    for itau in gen_taus:
        if not(itau.numberOfDaughters() and abs(itau.daughter(0).pdgId())==13 \
          and abs(itau.daughter(1).pdgId())==13 and abs(itau.daughter(2).pdgId())==13):
            normalTau += 1
    
    if normalTau:
        print 'thanks God I found a regular tau!'
        import pdb ; pdb.set_trace()
    
    if len(gen_muons)>3:
        candidate_gen_muons = []
        for key, group in groupby(gen_muons, lambda x : x.mother()):
            igroup = list(group)
            if abs(key.pdgId())==15 and len(igroup)==3:
                candidate_gen_muons.append(igroup)
        
        if len(candidate_gen_muons)==1:
            gen_muons = candidate_gen_muons[0]
            print 'patched', gen_muons
        else:
            print 'whatthefuck', gen_muons
            import pdb ; pdb.set_trace()
        
    if len(gen_muons)<3:
        print 'gen muons <3 !!'
        import pdb ; pdb.set_trace()
    
    reconstructable_muons = []
    for gg in gen_muons:
        if abs(gg.eta()) > 2.5: continue
        elif abs(gg.eta()) < 1.  and gg.pt() > 3. : reconstructable_muons.append(gg)
        elif abs(gg.eta()) >= 1. and gg.pt() > 0.8: reconstructable_muons.append(gg)
    
    if len(reconstructable_muons)==3:
        in_the_acceptance += 1
    else:
        continue
    
    goodmuons = []
        
    for mm, gg in product(muons, reconstructable_muons):
        if deltaR(mm, gg)<0.1:
            goodmuons.append(mm)
    
    goodmuons = list(set(goodmuons))

    if len(goodmuons)!=3:
        continue

    goodmuons.sort(key = lambda mu : mu.pt(), reverse=True)

    event.getByLabel (label_L1muon, handle_L1muons)
    L1_muons_bx = handle_L1muons.product()
    
    L1_muons = []
    
    for jj in range(L1_muons_bx.size(0)):
        L1_muons.append(L1_muons_bx.at(0,jj))

    tofill['mu1_off_pt' ] = goodmuons[0].pt ()
    tofill['mu1_off_eta'] = goodmuons[0].eta()
    tofill['mu1_off_phi'] = goodmuons[0].phi()
    tofill['mu1_off_vz' ] = goodmuons[0].vz()
    tofill['mu2_off_pt' ] = goodmuons[1].pt ()
    tofill['mu2_off_eta'] = goodmuons[1].eta()
    tofill['mu2_off_phi'] = goodmuons[1].phi()
    tofill['mu2_off_vz' ] = goodmuons[1].vz()
    tofill['mu3_off_pt' ] = goodmuons[2].pt ()
    tofill['mu3_off_eta'] = goodmuons[2].eta()
    tofill['mu3_off_phi'] = goodmuons[2].phi()
    tofill['mu3_off_vz' ] = goodmuons[2].vz()
    
    tofill['dR_off_12'] = deltaR(goodmuons[0], goodmuons[1])
    tofill['dR_off_13'] = deltaR(goodmuons[0], goodmuons[2])
    tofill['dR_off_23'] = deltaR(goodmuons[1], goodmuons[2])

    tofill['mass_off_12'] = (goodmuons[0].p4() + goodmuons[1].p4()).mass()
    tofill['mass_off_13'] = (goodmuons[0].p4() + goodmuons[2].p4()).mass()
    tofill['mass_off_23'] = (goodmuons[1].p4() + goodmuons[2].p4()).mass()

    tau_off = goodmuons[0].p4() + goodmuons[1].p4() + goodmuons[2].p4()
    
    tofill['tau_off_mass'  ] = tau_off.mass()
    tofill['tau_off_pt'    ] = tau_off.pt()
    tofill['tau_off_eta'   ] = tau_off.eta()
    tofill['tau_off_phi'   ] = tau_off.phi()
    tofill['tau_off_charge'] = sum([mu.charge() for mu in goodmuons])
    
    gen_mu1 = sorted([gg for gg in gen_muons if deltaR(gg, goodmuons[0])<0.1], key = lambda gg : deltaR(gg, goodmuons[0]))[0]
    gen_mu2 = sorted([gg for gg in gen_muons if deltaR(gg, goodmuons[1])<0.1], key = lambda gg : deltaR(gg, goodmuons[1]))[0]
    gen_mu3 = sorted([gg for gg in gen_muons if deltaR(gg, goodmuons[2])<0.1], key = lambda gg : deltaR(gg, goodmuons[2]))[0]

    tofill['mu1_gen_pt' ] = gen_mu1.pt ()
    tofill['mu1_gen_eta'] = gen_mu1.eta()
    tofill['mu1_gen_phi'] = gen_mu1.phi()
    tofill['mu2_gen_pt' ] = gen_mu2.pt ()
    tofill['mu2_gen_eta'] = gen_mu2.eta()
    tofill['mu2_gen_phi'] = gen_mu2.phi()
    tofill['mu3_gen_pt' ] = gen_mu3.pt ()
    tofill['mu3_gen_eta'] = gen_mu3.eta()
    tofill['mu3_gen_phi'] = gen_mu3.phi()
    
    passed += 1 

    try:
        hlt_mu1 = sorted([hh for hh in allmuons if deltaR(hh, goodmuons[0])<0.03], key = lambda gg : deltaR(gg, goodmuons[0]))[0]
        tofill['mu1_hlt_pt' ] = hlt_mu1.pt ()
        tofill['mu1_hlt_eta'] = hlt_mu1.eta()
        tofill['mu1_hlt_phi'] = hlt_mu1.phi()
        tofill['mu1_hlt_vz' ] = hlt_mu1.vz ()
    except:
        hlt_mu1 = None
        pass

    try:
        hlt_mu2 = sorted([hh for hh in allmuons if deltaR(hh, goodmuons[1])<0.03], key = lambda gg : deltaR(gg, goodmuons[1]))[0]
        tofill['mu2_hlt_pt' ] = hlt_mu2.pt ()
        tofill['mu2_hlt_eta'] = hlt_mu2.eta()
        tofill['mu2_hlt_phi'] = hlt_mu2.phi()
        tofill['mu2_hlt_vz' ] = hlt_mu2.vz ()
    except:
        hlt_mu2 = None
        pass
    
    try:
        hlt_mu3 = sorted([hh for hh in allmuons if deltaR(hh, goodmuons[2])<0.03], key = lambda gg : deltaR(gg, goodmuons[2]))[0]
        tofill['mu3_hlt_pt' ] = hlt_mu3.pt ()
        tofill['mu3_hlt_eta'] = hlt_mu3.eta()
        tofill['mu3_hlt_phi'] = hlt_mu3.phi()
        tofill['mu3_hlt_vz' ] = hlt_mu3.vz ()
    except:
        hlt_mu3 = None
        pass

    try:
        tofill['dR_hlt_12'] = deltaR(hlt_mu1, hlt_mu2)
        tofill['dR_hlt_13'] = deltaR(hlt_mu1, hlt_mu3)
        tofill['dR_hlt_23'] = deltaR(hlt_mu2, hlt_mu3)
    
        tofill['mass_hlt_12'] = (hlt_mu1.p4() + hlt_mu2.p4()).mass()
        tofill['mass_hlt_13'] = (hlt_mu1.p4() + hlt_mu3.p4()).mass()
        tofill['mass_hlt_23'] = (hlt_mu2.p4() + hlt_mu3.p4()).mass()
    
        tau_hlt = hlt_mu1.p4() + hlt_mu2.p4() + hlt_mu3.p4()
        
        tofill['tau_hlt_mass'  ] = tau_hlt.mass()
        tofill['tau_hlt_pt'    ] = tau_hlt.pt()
        tofill['tau_hlt_eta'   ] = tau_hlt.eta()
        tofill['tau_hlt_phi'   ] = tau_hlt.phi()
        tofill['tau_hlt_charge'] = sum([mu.charge() for mu in [hlt_mu1, hlt_mu2, hlt_mu3]])
    except:
        pass

    event.getByLabel(label_trig, handle_trig)
    triggers = handle_trig.product()
    names    = event.object().triggerNames(triggers)

    triggers_fired = [ ]

#     for trigger_name in ['HLT_DoubleMu3_Trk_Tau3mu_newMuonReco_v1', 'HLT_WTau3Mu_Mu5_Mu1_TrkMu0_TauIso_v1', 'HLT_WTau3Mu_Mu5_Mu1_TrkMu0_v1']:
    for trigger_name in hlts:
        index = names.triggerIndex(trigger_name)
        if index > len(triggers):
            continue
        if triggers.accept(index):
            triggers_fired.append(trigger_name)
            tofill[trigger_name] = 1
        else:
            tofill[trigger_name] = 0
    
    tofill['L1_SingleMu_22_eta2p1_Q12'                         ] = single_muon(L1_muons, 22, 2.1, 12)
                   
    tofill['L1_SingleMu_25_Q12'                                ] = single_muon(L1_muons, 25, 2.5, 12)
    
    tofill['L1_DoubleMu_15_7_Q8'                               ] = di_muon    (L1_muons, 15, 7, qual1= 8, qual2= 8)
                   
    tofill['L1_DoubleMu_12_0_Q12_maxMass4p0'                   ] = di_muon    (L1_muons, 12, 0, qual1=12, qual2=12, maxMass=4)
    tofill['L1_DoubleMu_10_1_Q12_maxMass4p0'                   ] = di_muon    (L1_muons, 10, 1, qual1=12, qual2=12, maxMass=4)
    tofill['L1_DoubleMu_9_1_Q12_maxMass4p0'                    ] = di_muon    (L1_muons,  9, 1, qual1=12, qual2=12, maxMass=4)
    tofill['L1_DoubleMu_8_3_Q12_maxMass4p0'                    ] = di_muon    (L1_muons,  8, 3, qual1=12, qual2=12, maxMass=4)
    tofill['L1_DoubleMu_6_2_Q12_maxMass4p0'                    ] = di_muon    (L1_muons,  6, 2, qual1=12, qual2=12, maxMass=4)
    tofill['L1_DoubleMu_5_3_Q12_maxMass4p0'                    ] = di_muon    (L1_muons,  5, 3, qual1=12, qual2=12, maxMass=4)
      
    tofill['L1_DoubleMu_12_0_Q8_maxMass4p0'                    ] = di_muon    (L1_muons, 12, 0, qual1= 8, qual2= 8, maxMass=4)
    tofill['L1_DoubleMu_10_1_Q8_maxMass4p0'                    ] = di_muon    (L1_muons, 10, 1, qual1= 8, qual2= 8, maxMass=4)
    tofill['L1_DoubleMu_9_1_Q8_maxMass4p0'                     ] = di_muon    (L1_muons,  9, 1, qual1= 8, qual2= 8, maxMass=4)
    tofill['L1_DoubleMu_8_3_Q8_maxMass4p0'                     ] = di_muon    (L1_muons,  8, 3, qual1= 8, qual2= 8, maxMass=4)
    tofill['L1_DoubleMu_6_2_Q8_maxMass4p0'                     ] = di_muon    (L1_muons,  6, 2, qual1= 8, qual2= 8, maxMass=4)
    tofill['L1_DoubleMu_5_3_Q8_maxMass4p0'                     ] = di_muon    (L1_muons,  5, 3, qual1= 8, qual2= 8, maxMass=4)
      
    tofill['L1_DoubleMu_12_0_Q12_maxMass4p0_OS'                ] = di_muon    (L1_muons, 12, 0, qual1=12, qual2=12, maxMass=4, sign=0)
    tofill['L1_DoubleMu_10_1_Q12_maxMass4p0_OS'                ] = di_muon    (L1_muons, 10, 1, qual1=12, qual2=12, maxMass=4, sign=0)
    tofill['L1_DoubleMu_9_1_Q12_maxMass4p0_OS'                 ] = di_muon    (L1_muons,  9, 1, qual1=12, qual2=12, maxMass=4, sign=0)
    tofill['L1_DoubleMu_8_3_Q12_maxMass4p0_OS'                 ] = di_muon    (L1_muons,  8, 3, qual1=12, qual2=12, maxMass=4, sign=0)
    tofill['L1_DoubleMu_6_2_Q12_maxMass4p0_OS'                 ] = di_muon    (L1_muons,  6, 2, qual1=12, qual2=12, maxMass=4, sign=0)
    tofill['L1_DoubleMu_5_3_Q12_maxMass4p0_OS'                 ] = di_muon    (L1_muons,  5, 3, qual1=12, qual2=12, maxMass=4, sign=0)
      
    tofill['L1_DoubleMu_12_0_Q8_maxMass4p0_OS'                 ] = di_muon    (L1_muons, 12, 0, qual1= 8, qual2= 8, maxMass=4, sign=0)
    tofill['L1_DoubleMu_10_1_Q8_maxMass4p0_OS'                 ] = di_muon    (L1_muons, 10, 1, qual1= 8, qual2= 8, maxMass=4, sign=0)
    tofill['L1_DoubleMu_9_1_Q8_maxMass4p0_OS'                  ] = di_muon    (L1_muons,  9, 1, qual1= 8, qual2= 8, maxMass=4, sign=0)
    tofill['L1_DoubleMu_8_3_Q8_maxMass4p0_OS'                  ] = di_muon    (L1_muons,  8, 3, qual1= 8, qual2= 8, maxMass=4, sign=0)
    tofill['L1_DoubleMu_6_2_Q8_maxMass4p0_OS'                  ] = di_muon    (L1_muons,  6, 2, qual1= 8, qual2= 8, maxMass=4, sign=0)
    tofill['L1_DoubleMu_5_3_Q8_maxMass4p0_OS'                  ] = di_muon    (L1_muons,  5, 3, qual1= 8, qual2= 8, maxMass=4, sign=0)
      
    tofill['L1_DoubleMu0er1p5_SQ_OS_dR_Max1p4'                 ] = di_muon    (L1_muons,  0  , 0  , eta1=1.5, eta2=1.5, qual1=12, qual2=12, maxDr=1.4, sign=0)
    tofill['L1_DoubleMu4_SQ_OS_dR_Max1p2'                      ] = di_muon    (L1_muons,  4  , 4  , qual1=12, qual2=12, maxDr=1.2, sign=0)
    tofill['L1_DoubleMu4p5_SQ_OS_dR_Max1p2'                    ] = di_muon    (L1_muons,  4.5, 4.5, qual1=12, qual2=12, maxDr=1.2, sign=0)
    
    tofill['L1_TripleMu_4_4_4'                                 ] = tri_muon   (L1_muons,  4, 4, 4)
    tofill['L1_TripleMu_5_3_3'                                 ] = tri_muon   (L1_muons,  5, 3, 3)
    tofill['L1_TripleMu_5_5_3'                                 ] = tri_muon   (L1_muons,  5, 5, 3)
    tofill['L1_TripleMu3_SQ'                                   ] = tri_muon   (L1_muons,  3, 3, 3, qual1=12, qual2=12, qual3=12)
    tofill['L1_TripleMu_5SQ_3SQ_0OQ'                           ] = tri_muon   (L1_muons,  5, 3, 0, qual1=12, qual2=12, qual3=4)
    tofill['L1_TripleMu_5_3_0_DoubleMu_5_3_OS_Mass_Max17'      ] = tri_muon   (L1_muons,  5, 3, 0, maxMass=17, sign=0)
    tofill['L1_TripleMu_5SQ_3SQ_0_DoubleMu_5_3_SQ_OS_Mass_Max9'] = tri_muon   (L1_muons,  5, 3, 0, qual1=12, qual2=12, maxMass=9, sign=0)

    ntuple.Fill(array('f',tofill.values()))

f1.cd()
ntuple.Write()
f1.Close()


#     print triggers_fired
    
print 'passed  ', passed
print 'in the acceptance ', in_the_acceptance
print 'jian    ', jian
print 'ric     ', ric
# print 'noiso   ', noiso
print 'any     ', anytrig



# # pass L1
# "L1_DoubleMu_15_7_Q8 || L1_DoubleMu4_SQ_OS_dR_Max1p2 || L1_DoubleMu4p5_SQ_OS_dR_Max1p2 || L1_SingleMu_22_eta2p1_Q12 || L1_SingleMu_25_Q12 || L1_DoubleMu0er1p5_SQ_OS_dR_Max1p4 || L1_TripleMu_5_3_0_DoubleMu_5_3_OS_Mass_Max17"        



# "HLT_IsoMu27_v10 || HLT_DoubleMu3_Trk_Tau3mu_newMuonReco_v1 || HLT_Tau3Mu_Mu5_Mu1_TkMu1_IsoTau10_v1 || HLT_Tau3Mu_Mu5_Mu1_TkMu1_IsoTau10_Iter0and1_v1 || HLT_Tau3Mu_Mu5_Mu1_TkMu1_IsoTau10_Iter0and1_merge_v1 || HLT_Tau3Mu_Mu5_Mu1_TkMu1_IsoTau10_TauCharge1_v1 || HLT_Tau3Mu_Mu5_Mu1_TkMu1_Tau10_v1 || HLT_Tau3Mu_Mu5_Mu1_TkMu1_Tau10_TauCharge1_v1" 