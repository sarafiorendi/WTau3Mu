import ROOT
from DataFormats.FWLite import Events, Handle
from PhysicsTools.HeppyCore.utils.deltar import deltaR, deltaPhi
from itertools import product, combinations, groupby
from collections import OrderedDict
from math import cos, cosh, sqrt
from array import array
from seeds import single_muon, di_muon, tri_muon

# ROOT.gROOT.SetBatch()
ROOT.gStyle.SetOptStat(0)

# events = Events('outputFULL.root')
events = Events([
    'root://cms-xrd-global.cern.ch//store/user/manzoni/WTau3Mu2017EnrichedV2/WToTauNu_TauTo3Mu_MadGraph_13TeV/WTau3Mu2017EnrichedV2/170619_151719/0000/outputFULL_1.root',
    'root://cms-xrd-global.cern.ch//store/user/manzoni/WTau3Mu2017EnrichedV2/WToTauNu_TauTo3Mu_MadGraph_13TeV/WTau3Mu2017EnrichedV2/170619_151719/0000/outputFULL_10.root',
    'root://cms-xrd-global.cern.ch//store/user/manzoni/WTau3Mu2017EnrichedV2/WToTauNu_TauTo3Mu_MadGraph_13TeV/WTau3Mu2017EnrichedV2/170619_151719/0000/outputFULL_11.root',
    'root://cms-xrd-global.cern.ch//store/user/manzoni/WTau3Mu2017EnrichedV2/WToTauNu_TauTo3Mu_MadGraph_13TeV/WTau3Mu2017EnrichedV2/170619_151719/0000/outputFULL_12.root',
    'root://cms-xrd-global.cern.ch//store/user/manzoni/WTau3Mu2017EnrichedV2/WToTauNu_TauTo3Mu_MadGraph_13TeV/WTau3Mu2017EnrichedV2/170619_151719/0000/outputFULL_13.root',
    'root://cms-xrd-global.cern.ch//store/user/manzoni/WTau3Mu2017EnrichedV2/WToTauNu_TauTo3Mu_MadGraph_13TeV/WTau3Mu2017EnrichedV2/170619_151719/0000/outputFULL_14.root',
    'root://cms-xrd-global.cern.ch//store/user/manzoni/WTau3Mu2017EnrichedV2/WToTauNu_TauTo3Mu_MadGraph_13TeV/WTau3Mu2017EnrichedV2/170619_151719/0000/outputFULL_15.root',
    'root://cms-xrd-global.cern.ch//store/user/manzoni/WTau3Mu2017EnrichedV2/WToTauNu_TauTo3Mu_MadGraph_13TeV/WTau3Mu2017EnrichedV2/170619_151719/0000/outputFULL_16.root',
    'root://cms-xrd-global.cern.ch//store/user/manzoni/WTau3Mu2017EnrichedV2/WToTauNu_TauTo3Mu_MadGraph_13TeV/WTau3Mu2017EnrichedV2/170619_151719/0000/outputFULL_17.root',
    'root://cms-xrd-global.cern.ch//store/user/manzoni/WTau3Mu2017EnrichedV2/WToTauNu_TauTo3Mu_MadGraph_13TeV/WTau3Mu2017EnrichedV2/170619_151719/0000/outputFULL_18.root',
    'root://cms-xrd-global.cern.ch//store/user/manzoni/WTau3Mu2017EnrichedV2/WToTauNu_TauTo3Mu_MadGraph_13TeV/WTau3Mu2017EnrichedV2/170619_151719/0000/outputFULL_19.root',
    'root://cms-xrd-global.cern.ch//store/user/manzoni/WTau3Mu2017EnrichedV2/WToTauNu_TauTo3Mu_MadGraph_13TeV/WTau3Mu2017EnrichedV2/170619_151719/0000/outputFULL_2.root',
    'root://cms-xrd-global.cern.ch//store/user/manzoni/WTau3Mu2017EnrichedV2/WToTauNu_TauTo3Mu_MadGraph_13TeV/WTau3Mu2017EnrichedV2/170619_151719/0000/outputFULL_20.root',
    'root://cms-xrd-global.cern.ch//store/user/manzoni/WTau3Mu2017EnrichedV2/WToTauNu_TauTo3Mu_MadGraph_13TeV/WTau3Mu2017EnrichedV2/170619_151719/0000/outputFULL_21.root',
    'root://cms-xrd-global.cern.ch//store/user/manzoni/WTau3Mu2017EnrichedV2/WToTauNu_TauTo3Mu_MadGraph_13TeV/WTau3Mu2017EnrichedV2/170619_151719/0000/outputFULL_22.root',
    'root://cms-xrd-global.cern.ch//store/user/manzoni/WTau3Mu2017EnrichedV2/WToTauNu_TauTo3Mu_MadGraph_13TeV/WTau3Mu2017EnrichedV2/170619_151719/0000/outputFULL_23.root',
    'root://cms-xrd-global.cern.ch//store/user/manzoni/WTau3Mu2017EnrichedV2/WToTauNu_TauTo3Mu_MadGraph_13TeV/WTau3Mu2017EnrichedV2/170619_151719/0000/outputFULL_24.root',
    'root://cms-xrd-global.cern.ch//store/user/manzoni/WTau3Mu2017EnrichedV2/WToTauNu_TauTo3Mu_MadGraph_13TeV/WTau3Mu2017EnrichedV2/170619_151719/0000/outputFULL_25.root',
    'root://cms-xrd-global.cern.ch//store/user/manzoni/WTau3Mu2017EnrichedV2/WToTauNu_TauTo3Mu_MadGraph_13TeV/WTau3Mu2017EnrichedV2/170619_151719/0000/outputFULL_26.root',
    'root://cms-xrd-global.cern.ch//store/user/manzoni/WTau3Mu2017EnrichedV2/WToTauNu_TauTo3Mu_MadGraph_13TeV/WTau3Mu2017EnrichedV2/170619_151719/0000/outputFULL_27.root',
    'root://cms-xrd-global.cern.ch//store/user/manzoni/WTau3Mu2017EnrichedV2/WToTauNu_TauTo3Mu_MadGraph_13TeV/WTau3Mu2017EnrichedV2/170619_151719/0000/outputFULL_28.root',
    'root://cms-xrd-global.cern.ch//store/user/manzoni/WTau3Mu2017EnrichedV2/WToTauNu_TauTo3Mu_MadGraph_13TeV/WTau3Mu2017EnrichedV2/170619_151719/0000/outputFULL_29.root',
    'root://cms-xrd-global.cern.ch//store/user/manzoni/WTau3Mu2017EnrichedV2/WToTauNu_TauTo3Mu_MadGraph_13TeV/WTau3Mu2017EnrichedV2/170619_151719/0000/outputFULL_3.root',
    'root://cms-xrd-global.cern.ch//store/user/manzoni/WTau3Mu2017EnrichedV2/WToTauNu_TauTo3Mu_MadGraph_13TeV/WTau3Mu2017EnrichedV2/170619_151719/0000/outputFULL_30.root',
    'root://cms-xrd-global.cern.ch//store/user/manzoni/WTau3Mu2017EnrichedV2/WToTauNu_TauTo3Mu_MadGraph_13TeV/WTau3Mu2017EnrichedV2/170619_151719/0000/outputFULL_31.root',
    'root://cms-xrd-global.cern.ch//store/user/manzoni/WTau3Mu2017EnrichedV2/WToTauNu_TauTo3Mu_MadGraph_13TeV/WTau3Mu2017EnrichedV2/170619_151719/0000/outputFULL_32.root',
    'root://cms-xrd-global.cern.ch//store/user/manzoni/WTau3Mu2017EnrichedV2/WToTauNu_TauTo3Mu_MadGraph_13TeV/WTau3Mu2017EnrichedV2/170619_151719/0000/outputFULL_33.root',
    'root://cms-xrd-global.cern.ch//store/user/manzoni/WTau3Mu2017EnrichedV2/WToTauNu_TauTo3Mu_MadGraph_13TeV/WTau3Mu2017EnrichedV2/170619_151719/0000/outputFULL_34.root',
    'root://cms-xrd-global.cern.ch//store/user/manzoni/WTau3Mu2017EnrichedV2/WToTauNu_TauTo3Mu_MadGraph_13TeV/WTau3Mu2017EnrichedV2/170619_151719/0000/outputFULL_4.root',
    'root://cms-xrd-global.cern.ch//store/user/manzoni/WTau3Mu2017EnrichedV2/WToTauNu_TauTo3Mu_MadGraph_13TeV/WTau3Mu2017EnrichedV2/170619_151719/0000/outputFULL_5.root',
    'root://cms-xrd-global.cern.ch//store/user/manzoni/WTau3Mu2017EnrichedV2/WToTauNu_TauTo3Mu_MadGraph_13TeV/WTau3Mu2017EnrichedV2/170619_151719/0000/outputFULL_6.root',
    'root://cms-xrd-global.cern.ch//store/user/manzoni/WTau3Mu2017EnrichedV2/WToTauNu_TauTo3Mu_MadGraph_13TeV/WTau3Mu2017EnrichedV2/170619_151719/0000/outputFULL_7.root',
    'root://cms-xrd-global.cern.ch//store/user/manzoni/WTau3Mu2017EnrichedV2/WToTauNu_TauTo3Mu_MadGraph_13TeV/WTau3Mu2017EnrichedV2/170619_151719/0000/outputFULL_8.root',
    'root://cms-xrd-global.cern.ch//store/user/manzoni/WTau3Mu2017EnrichedV2/WToTauNu_TauTo3Mu_MadGraph_13TeV/WTau3Mu2017EnrichedV2/170619_151719/0000/outputFULL_9.root',
][:3])

handle_L1muons = Handle('BXVector<l1t::Muon>')
label_L1muon   = ('gmtStage2Digis', 'Muon') 
# label_L1muon   = ('gtStage2Digis', 'Muon') 

handle_gen = Handle('vector<reco::GenParticle>')
label_gen = ('prunedGenParticles')

mykeys = [
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
    'L1_TripleMu_5SQ_3SQ_0OQ'                           ,
    'L1_TripleMu_5_3_0_DoubleMu_5_3_OS_Mass_Max17'      ,
    'L1_TripleMu_5SQ_3SQ_0_DoubleMu_5_3_SQ_OS_Mass_Max9',
]

f = ROOT.TFile('acceptance_signal.root', 'recreate')

acceptance_tot             = ROOT.TH1F('L1_acceptance_tot'            , 'L1_acceptance_tot'            , len(mykeys), 0, len(mykeys) +1)
acceptance_reconstructable = ROOT.TH1F('L1_acceptance_reconstructable', 'L1_acceptance_reconstructable', len(mykeys), 0, len(mykeys) +1)

ntuple = ROOT.TNtuple('tree', 'tree_tot', ':'.join(mykeys) + ':reconstructable')

in_the_acceptance = 0
totevents = events.size()
for i, event in enumerate(events):
#     if i>2000:
#         break
    
    if i%100==0:
        print '===> processing %d / %d event' %(i, totevents)
    
    event.getByLabel (label_gen, handle_gen)
    gen_particles = handle_gen.product()

    gen_muons = [pp for pp in gen_particles if abs(pp.pdgId())==13 and abs(pp.mother().pdgId())==15]
    
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
        
    event.getByLabel (label_L1muon, handle_L1muons)
    L1_muons_bx = handle_L1muons.product()
    
#     if not L1_muons_bx.size(0):
#         continue
            
    L1_muons = []
    
    for jj in range(L1_muons_bx.size(0)):
        L1_muons.append(L1_muons_bx.at(0,jj))
    
    seeds = OrderedDict()
        
    for kk in mykeys:
        seeds[kk] = False

        seeds['L1_SingleMu_22_eta2p1_Q12'                         ] = single_muon(L1_muons, 22, 2.1, 12)
                       
        seeds['L1_SingleMu_25_Q12'                                ] = single_muon(L1_muons, 25, 2.5, 12)
      
        seeds['L1_DoubleMu_15_7_Q8'                               ] = di_muon    (L1_muons, 15, 7, qual1= 8, qual2= 8)
                       
        seeds['L1_DoubleMu_12_0_Q12_maxMass4p0'                   ] = di_muon    (L1_muons, 12, 0, qual1=12, qual2=12, maxMass=4)
        seeds['L1_DoubleMu_10_1_Q12_maxMass4p0'                   ] = di_muon    (L1_muons, 10, 1, qual1=12, qual2=12, maxMass=4)
        seeds['L1_DoubleMu_9_1_Q12_maxMass4p0'                    ] = di_muon    (L1_muons,  9, 1, qual1=12, qual2=12, maxMass=4)
        seeds['L1_DoubleMu_8_3_Q12_maxMass4p0'                    ] = di_muon    (L1_muons,  8, 3, qual1=12, qual2=12, maxMass=4)
        seeds['L1_DoubleMu_6_2_Q12_maxMass4p0'                    ] = di_muon    (L1_muons,  6, 2, qual1=12, qual2=12, maxMass=4)
        seeds['L1_DoubleMu_5_3_Q12_maxMass4p0'                    ] = di_muon    (L1_muons,  5, 3, qual1=12, qual2=12, maxMass=4)
          
        seeds['L1_DoubleMu_12_0_Q8_maxMass4p0'                    ] = di_muon    (L1_muons, 12, 0, qual1= 8, qual2= 8, maxMass=4)
        seeds['L1_DoubleMu_10_1_Q8_maxMass4p0'                    ] = di_muon    (L1_muons, 10, 1, qual1= 8, qual2= 8, maxMass=4)
        seeds['L1_DoubleMu_9_1_Q8_maxMass4p0'                     ] = di_muon    (L1_muons,  9, 1, qual1= 8, qual2= 8, maxMass=4)
        seeds['L1_DoubleMu_8_3_Q8_maxMass4p0'                     ] = di_muon    (L1_muons,  8, 3, qual1= 8, qual2= 8, maxMass=4)
        seeds['L1_DoubleMu_6_2_Q8_maxMass4p0'                     ] = di_muon    (L1_muons,  6, 2, qual1= 8, qual2= 8, maxMass=4)
        seeds['L1_DoubleMu_5_3_Q8_maxMass4p0'                     ] = di_muon    (L1_muons,  5, 3, qual1= 8, qual2= 8, maxMass=4)
          
        seeds['L1_DoubleMu_12_0_Q12_maxMass4p0_OS'                ] = di_muon    (L1_muons, 12, 0, qual1=12, qual2=12, maxMass=4, sign=0)
        seeds['L1_DoubleMu_10_1_Q12_maxMass4p0_OS'                ] = di_muon    (L1_muons, 10, 1, qual1=12, qual2=12, maxMass=4, sign=0)
        seeds['L1_DoubleMu_9_1_Q12_maxMass4p0_OS'                 ] = di_muon    (L1_muons,  9, 1, qual1=12, qual2=12, maxMass=4, sign=0)
        seeds['L1_DoubleMu_8_3_Q12_maxMass4p0_OS'                 ] = di_muon    (L1_muons,  8, 3, qual1=12, qual2=12, maxMass=4, sign=0)
        seeds['L1_DoubleMu_6_2_Q12_maxMass4p0_OS'                 ] = di_muon    (L1_muons,  6, 2, qual1=12, qual2=12, maxMass=4, sign=0)
        seeds['L1_DoubleMu_5_3_Q12_maxMass4p0_OS'                 ] = di_muon    (L1_muons,  5, 3, qual1=12, qual2=12, maxMass=4, sign=0)
          
        seeds['L1_DoubleMu_12_0_Q8_maxMass4p0_OS'                 ] = di_muon    (L1_muons, 12, 0, qual1= 8, qual2= 8, maxMass=4, sign=0)
        seeds['L1_DoubleMu_10_1_Q8_maxMass4p0_OS'                 ] = di_muon    (L1_muons, 10, 1, qual1= 8, qual2= 8, maxMass=4, sign=0)
        seeds['L1_DoubleMu_9_1_Q8_maxMass4p0_OS'                  ] = di_muon    (L1_muons,  9, 1, qual1= 8, qual2= 8, maxMass=4, sign=0)
        seeds['L1_DoubleMu_8_3_Q8_maxMass4p0_OS'                  ] = di_muon    (L1_muons,  8, 3, qual1= 8, qual2= 8, maxMass=4, sign=0)
        seeds['L1_DoubleMu_6_2_Q8_maxMass4p0_OS'                  ] = di_muon    (L1_muons,  6, 2, qual1= 8, qual2= 8, maxMass=4, sign=0)
        seeds['L1_DoubleMu_5_3_Q8_maxMass4p0_OS'                  ] = di_muon    (L1_muons,  5, 3, qual1= 8, qual2= 8, maxMass=4, sign=0)
          
        seeds['L1_DoubleMu0er1p5_SQ_OS_dR_Max1p4'                 ] = di_muon    (L1_muons,  0  , 0  , eta1=1.5, eta2=1.5, qual1=12, qual2=12, maxDr=1.4, sign=0)
        seeds['L1_DoubleMu4_SQ_OS_dR_Max1p2'                      ] = di_muon    (L1_muons,  4  , 4  , qual1=12, qual2=12, maxDr=1.2, sign=0)
        seeds['L1_DoubleMu4p5_SQ_OS_dR_Max1p2'                    ] = di_muon    (L1_muons,  4.5, 4.5, qual1=12, qual2=12, maxDr=1.2, sign=0)
      
        seeds['L1_TripleMu_4_4_4'                                 ] = tri_muon   (L1_muons,  4, 4, 4)
        seeds['L1_TripleMu_5_3_3'                                 ] = tri_muon   (L1_muons,  5, 3, 0)
        seeds['L1_TripleMu_5SQ_3SQ_0OQ'                           ] = tri_muon   (L1_muons,  5, 3, 0, qual1=12, qual2=12, qual3=4)
        seeds['L1_TripleMu_5_3_0_DoubleMu_5_3_OS_Mass_Max17'      ] = tri_muon   (L1_muons,  5, 3, 0, maxMass=17, sign=0)
        seeds['L1_TripleMu_5SQ_3SQ_0_DoubleMu_5_3_SQ_OS_Mass_Max9'] = tri_muon   (L1_muons,  5, 3, 0, qual1=12, qual2=12, maxMass=9, sign=0)

    unpackedBs = array('f',seeds.values()+[len(reconstructable_muons)==3])      
    ntuple.Fill(unpackedBs)

    for k, v in seeds.iteritems():
        acceptance_tot.Fill(k, v>0)
        if len(reconstructable_muons)==3:
            acceptance_reconstructable.Fill(k, v>0)

f.cd()
ntuple.Write()

acceptance_tot.SetLineColor(ROOT.kBlue)
acceptance_tot.Scale(1./float(totevents))
acceptance_tot.SetMinimum(0.)
acceptance_tot.SetMaximum(1.05)
acceptance_tot.Draw('HIST')
acceptance_tot.Write()

acceptance_reconstructable.SetLineColor(ROOT.kRed)
acceptance_reconstructable.Scale(1./float(in_the_acceptance))
acceptance_reconstructable.SetMinimum(0.)
acceptance_reconstructable.SetMaximum(1.05)
acceptance_reconstructable.Draw('HIST')
acceptance_reconstructable.Write()

f.Close()


# l1 = ROOT.TLegend(0.5,0.7,0.88,0.88)
# l1.AddEntry(acceptance_reconstructable, 'wrt all gen events')
# l1.AddEntry(acceptance_tot            , "wrt 'reconstructable' gen events")
# l1.SetFillColor(0)
# l1.Draw('sameAEPZ')

