import ROOT
from DataFormats.FWLite import Events, Handle
from PhysicsTools.HeppyCore.utils.deltar import deltaR, deltaPhi
from itertools import product, combinations
from collections import OrderedDict
from math import cos, cosh, sqrt
from array import array

# ROOT.gROOT.SetBatch()
ROOT.gStyle.SetOptStat(0)

events = Events ('outputFULL.root')

handle = Handle ('std::vector<pat::Muon>')
label  = ('slimmedMuons')

handle_L3muons = Handle('vector<reco::RecoChargedCandidate>')
label_L3muon   = ('hltIterL3MuonCandidates') 

handle_L1muons = Handle('BXVector<l1t::Muon>')
label_L1muon   = ('simGmtStage2Digis') 

handle_global = Handle('vector<reco::RecoChargedCandidate>')
label_global   = ('hltGlbTrkMuonCands') 

handle_gen = Handle('vector<reco::GenParticle>')
label_gen = ('prunedGenParticles')


acceptance = ROOT.TH1F('L1acceptance', 'L1acceptance', 25, 0, 25)


mykeys = [
    'L1_SingleMu_25_qual12',
    'L1_DoubleMu_0_0_qual8',
    'L1_DoubleMu_0_0_qual12',
    'L1_DoubleMu_11_4_qual8',
    'L1_DoubleMu_11_4_qual12',
    'L1_DoubleMu_13_6_qual8',
    'L1_DoubleMu_13_6_qual12',
    'L1_DoubleMu_15_8_qual8',
    'L1_DoubleMu_15_8_qual12',
    'L1_DoubleMu_10_5_qual8_maxMass4',
    'L1_DoubleMu_10_5_qual12_maxMass4',
    'L1_DoubleMu_10_5_qual8_maxApproxMass4',
    'L1_DoubleMu_10_5_qual12_maxApproxMass4',
    'L1_DoubleMu_10_5_qual8_maxDR1p0',
    'L1_DoubleMu_10_5_qual12_maxDR1p0',
    'L1_DoubleMu_8_3_qual8_maxMass4',
    'L1_DoubleMu_8_3_qual12_maxMass4',
    'L1_DoubleMu_8_3_qual8_maxApproxMass4',
    'L1_DoubleMu_8_3_qual12_maxApproxMass4',
    'L1_DoubleMu_8_3_qual8_maxDR1p0',
    'L1_DoubleMu_8_3_qual12_maxDR1p0', 
    'L1_TripleMu_8_3_0_qual8_maxMass4',
    'L1_TripleMu_8_3_0_qual12_maxMass4',
    'L1_TripleMu_8_3_0_qual8_maxApproxMass4',
    'L1_TripleMu_8_3_0_qual12_maxApproxMass4',
]


ntuple = ROOT.TNtuple('tree','tree',':'.join(mykeys))
f = ROOT.TFile('acceptance.root', 'recreate')

passed = 0
for i, event in enumerate(events):
#     if i>10:
#         break
        
    print '\n====================>'
        
    event.getByLabel (label, handle)
    muons = handle.product()

    event.getByLabel (label_gen, handle_gen)
    gen_particles = handle_gen.product()
    
    gen_muons = [pp for pp in gen_particles if abs(pp.pdgId())==13 and abs(pp.mother().pdgId())==15]

    for gg1, gg2 in combinations(gen_muons, 2):
        print 'gen mass à la L1        ', sqrt(2. * gg1.pt() * gg2.pt() * (cosh(gg1.eta() - gg2.eta()) - cos(gg1.phi() - gg2.phi())))
        print 'gen mass the right way  ', (gg1.p4() + gg2.p4()).M()

    event.getByLabel (label_L1muon, handle_L1muons)
    L1_muons_bx = handle_L1muons.product()
    
    L1_muons = []
    
    for jj in range(L1_muons_bx.size(0)):
        L1_muons.append(L1_muons_bx.at(0,jj))
    
    goodmuons = []
        
    for mm, gg in product(muons, gen_muons):
        if deltaR(mm, gg)<0.1:
            goodmuons.append(mm)
    
    goodmuons = list(set(goodmuons))

    if len(goodmuons)!=3:
        continue
    
    passed += 1 
    
    seeds = OrderedDict()
    
    for kk in mykeys:
        seeds[kk] = 0

    for mu in L1_muons:
        if mu.pt()>25. and mu.hwQual()>=12: seeds['L1_SingleMu_25_qual12'  ] += 1

    qual8muons = [mm for mm in L1_muons if mm.hwQual()>=8]

    for mu_1, mu_2 in combinations(qual8muons, 2):
        
        mu_1_p4_atVtx = ROOT.TLorentzVector()
        mu_1_p4_atVtx.SetPtEtaPhiM(mu_1.pt(), mu_1.etaAtVtx(), mu_1.phiAtVtx(), 0.105658)

        mu_2_p4_atVtx = ROOT.TLorentzVector()
        mu_2_p4_atVtx.SetPtEtaPhiM(mu_2.pt(), mu_2.etaAtVtx(), mu_2.phiAtVtx(), 0.105658)
    
        mass        = (mu_1_p4_atVtx + mu_2_p4_atVtx).M()
        mass_approx = sqrt(2. * mu_1.pt() * mu_2.pt() * (cosh(mu_1.etaAtVtx() - mu_2.etaAtVtx()) - cos(mu_1.phiAtVtx() - mu_2.phiAtVtx())))
        dR          = mu_1_p4_atVtx.DeltaR(mu_2_p4_atVtx)
    
        if mu_1.pt() >  0. and mu_2.pt() > 0.                     : seeds['L1_DoubleMu_0_0_qual8'                 ] += 1
        if mu_1.pt() > 11. and mu_2.pt() > 4.                     : seeds['L1_DoubleMu_11_4_qual8'                ] += 1
        if mu_1.pt() > 13. and mu_2.pt() > 6.                     : seeds['L1_DoubleMu_13_6_qual8'                ] += 1
        if mu_1.pt() > 15. and mu_2.pt() > 8.                     : seeds['L1_DoubleMu_15_8_qual8'                ] += 1
        if mu_1.pt() > 10. and mu_2.pt() > 5. and mass < 4.       : seeds['L1_DoubleMu_10_5_qual8_maxMass4'       ] += 1
        if mu_1.pt() > 10. and mu_2.pt() > 5. and mass_approx < 4.: seeds['L1_DoubleMu_10_5_qual8_maxApproxMass4' ] += 1
        if mu_1.pt() > 10. and mu_2.pt() > 5. and dR < 1.         : seeds['L1_DoubleMu_10_5_qual8_maxDR1p0'       ] += 1
        if mu_1.pt() >  8. and mu_2.pt() > 3. and mass < 4.       : seeds['L1_DoubleMu_8_3_qual8_maxMass4'        ] += 1
        if mu_1.pt() >  8. and mu_2.pt() > 3. and mass_approx < 4.: seeds['L1_DoubleMu_8_3_qual8_maxApproxMass4'  ] += 1
        if mu_1.pt() >  8. and mu_2.pt() > 3. and dR < 1.         : seeds['L1_DoubleMu_8_3_qual8_maxDR1p0'        ] += 1
        if mu_1.pt() >  8. and mu_2.pt() > 3. and mass < 4.        and len(qual8muons)>=3: seeds['L1_TripleMu_8_3_0_qual8_maxMass4'        ] += 1
        if mu_1.pt() >  8. and mu_2.pt() > 3. and mass_approx < 4. and len(qual8muons)>=3: seeds['L1_TripleMu_8_3_0_qual8_maxApproxMass4'  ] += 1


    qual12muons = [mm for mm in L1_muons if mm.hwQual()>=12]

    for mu_1, mu_2 in combinations(qual12muons, 2):
        
        mu_1_p4_atVtx = ROOT.TLorentzVector()
        mu_1_p4_atVtx.SetPtEtaPhiM(mu_1.pt(), mu_1.etaAtVtx(), mu_1.phiAtVtx(), 0.105658)

        mu_2_p4_atVtx = ROOT.TLorentzVector()
        mu_2_p4_atVtx.SetPtEtaPhiM(mu_2.pt(), mu_2.etaAtVtx(), mu_2.phiAtVtx(), 0.105658)
    
        mass        = (mu_1_p4_atVtx + mu_2_p4_atVtx).M()
        mass_approx = sqrt(2. * mu_1.pt() * mu_2.pt() * (cosh(mu_1.etaAtVtx() - mu_2.etaAtVtx()) - cos(mu_1.phiAtVtx() - mu_2.phiAtVtx())))
        dR          = mu_1_p4_atVtx.DeltaR(mu_2_p4_atVtx)
    
        if mu_1.pt() >  0. and mu_2.pt() > 0.                     : seeds['L1_DoubleMu_0_0_qual12'                ] += 1
        if mu_1.pt() > 11. and mu_2.pt() > 4.                     : seeds['L1_DoubleMu_11_4_qual12'               ] += 1
        if mu_1.pt() > 13. and mu_2.pt() > 6.                     : seeds['L1_DoubleMu_13_6_qual12'               ] += 1
        if mu_1.pt() > 15. and mu_2.pt() > 8.                     : seeds['L1_DoubleMu_15_8_qual12'               ] += 1
        if mu_1.pt() > 10. and mu_2.pt() > 5. and mass < 4.       : seeds['L1_DoubleMu_10_5_qual12_maxMass4'      ] += 1
        if mu_1.pt() > 10. and mu_2.pt() > 5. and mass_approx < 4.: seeds['L1_DoubleMu_10_5_qual12_maxApproxMass4'] += 1
        if mu_1.pt() > 10. and mu_2.pt() > 5. and dR < 1.         : seeds['L1_DoubleMu_10_5_qual12_maxDR1p0'      ] += 1
        if mu_1.pt() >  8. and mu_2.pt() > 3. and mass < 4.       : seeds['L1_DoubleMu_8_3_qual12_maxMass4'       ] += 1
        if mu_1.pt() >  8. and mu_2.pt() > 3. and mass_approx < 4.: seeds['L1_DoubleMu_8_3_qual12_maxApproxMass4' ] += 1
        if mu_1.pt() >  8. and mu_2.pt() > 3. and dR < 1.         : seeds['L1_DoubleMu_8_3_qual12_maxDR1p0'       ] += 1
        if mu_1.pt() >  8. and mu_2.pt() > 3. and mass < 4.        and len(qual12muons)>=3: seeds['L1_TripleMu_8_3_0_qual12_maxMass4'        ] += 1
        if mu_1.pt() >  8. and mu_2.pt() > 3. and mass_approx < 4. and len(qual12muons)>=3: seeds['L1_TripleMu_8_3_0_qual12_maxApproxMass4'  ] += 1


    unpackedBs = array('f',seeds.values())      
    ntuple.Fill(unpackedBs)



    for k, v in seeds.iteritems():
        acceptance.Fill(k, v>0)


f.cd()
ntuple.Write()
f.Close()        


acceptance.Scale(1./float(passed))
acceptance.SetMinimum(0.)
acceptance.SetMaximum(1.05)
acceptance.Draw('HIST')



#     for mu in L1_muons:
#         if mu.hwQual>=8 and mu.hwQual: seeds['L1_DoubleMu_0_0_qual8'] += 1
#         if mu.hwQual>=12: seeds['L1_DoubleMu_0_0_qual8'] += 1


    
#     print '\t offline muons pt eta phi'
#     for mu in goodmuons: print '\t\t', mu.pt(), mu.eta(), mu.phi()
#     print '\t online L3 muons pt eta phi'
#     for mu in L3muons: print '\t\t', mu.pt(), mu.eta(), mu.phi()
#     print '\t online merged muons pt eta phi'
#     for mu in AllHLTmuons: print '\t\t', mu.pt(), mu.eta(), mu.phi()




