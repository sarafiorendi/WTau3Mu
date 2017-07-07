import ROOT
from DataFormats.FWLite import Events, Handle
from PhysicsTools.HeppyCore.utils.deltar import deltaR, deltaPhi
from itertools import product, combinations
from collections import OrderedDict
from math import cos, cosh, sqrt
from array import array
from seeds import single_muon, di_muon, tri_muon

# ROOT.gROOT.SetBatch()
ROOT.gStyle.SetOptStat(0)

events = Events('outputFULL.root')

handle_L1muons = Handle('BXVector<l1t::Muon>')
label_L1muon   = ('gmtStage2Digis', 'Muon') 
# label_L1muon   = ('gtStage2Digis', 'Muon') 

acceptance = ROOT.TH1F('L1acceptance_rate', 'L1acceptance_rate', 25, 0, 25)

mykeys = [
    'L1_SingleMu_22_eta2p1_qual12',

    'L1_SingleMu_25_qual12',

    'L1_DoubleMu_10_1_Q12_maxMass4p0',
    'L1_DoubleMu_9_1_Q12_maxMass4p0',
    'L1_DoubleMu_8_3_Q12_maxMass4p0',
    'L1_DoubleMu_6_2_Q12_maxMass4p0',
    'L1_DoubleMu_5_3_Q12_maxMass4p0',
    
    'L1_DoubleMu_10_1_Q8_maxMass4p0',
    'L1_DoubleMu_9_1_Q8_maxMass4p0',
    'L1_DoubleMu_8_3_Q8_maxMass4p0',
    'L1_DoubleMu_6_2_Q8_maxMass4p0',
    'L1_DoubleMu_5_3_Q8_maxMass4p0',
    
    'L1_DoubleMu_10_1_Q12_maxMass4p0_OS',
    'L1_DoubleMu_9_1_Q12_maxMass4p0_0S',
    'L1_DoubleMu_8_3_Q12_maxMass4p0_0S',
    'L1_DoubleMu_6_2_Q12_maxMass4p0_0S',
    'L1_DoubleMu_5_3_Q12_maxMass4p0_0S',
    
    'L1_DoubleMu_10_1_Q8_maxMass4p0_0S',
    'L1_DoubleMu_9_1_Q8_maxMass4p0_0S',
    'L1_DoubleMu_8_3_Q8_maxMass4p0_0S',
    'L1_DoubleMu_6_2_Q8_maxMass4p0_0S',
    'L1_DoubleMu_5_3_Q8_maxMass4p0_0S',
    
    'L1_DoubleMu0er1p5_SQ_OS_dR_Max1p4',
    'L1_TripleMu_5_3_0_DoubleMu_5_3_OS_Mass_Max17',
    'L1_DoubleMu4_SQ_OS_dR_Max1p2',
    'L1_DoubleMu4p5_SQ_OS_dR_Max1p2',
]

ntuple = ROOT.TNtuple('tree','tree',':'.join(mykeys))
f = ROOT.TFile('acceptance_signal.root', 'recreate')

passed = 0
totevents = events.size()
for i, event in enumerate(events):
#     if i>2000:
#         break
    
    if i%100==0:
        print '===> processing %d / %d event' %(i, totevents)
    
    passed += 1
        
    event.getByLabel (label_L1muon, handle_L1muons)
    L1_muons_bx = handle_L1muons.product()
    
    if not L1_muons_bx.size(0):
        continue
    
#     else: import pdb ; pdb.set_trace()
        
    L1_muons = []
    
    for jj in range(L1_muons_bx.size(0)):
        L1_muons.append(L1_muons_bx.at(0,jj))
    
    seeds = OrderedDict()
        
    for kk in mykeys:
        seeds[kk] = False

    seeds['L1_SingleMu_22_eta2p1_qual12'                ] = single_muon(L1_muons, 22, 2.1, 12)
             
    seeds['L1_SingleMu_25_qual12'                       ] = single_muon(L1_muons, 25, 2.5, 12)
             
    seeds['L1_DoubleMu_10_1_Q12_maxMass4p0'             ] = di_muon    (L1_muons, 10, 1, qual1=12, qual2=12, maxMass=4)
    seeds['L1_DoubleMu_9_1_Q12_maxMass4p0'              ] = di_muon    (L1_muons,  9, 1, qual1=12, qual2=12, maxMass=4)
    seeds['L1_DoubleMu_8_3_Q12_maxMass4p0'              ] = di_muon    (L1_muons,  8, 3, qual1=12, qual2=12, maxMass=4)
    seeds['L1_DoubleMu_6_2_Q12_maxMass4p0'              ] = di_muon    (L1_muons,  6, 2, qual1=12, qual2=12, maxMass=4)
    seeds['L1_DoubleMu_5_3_Q12_maxMass4p0'              ] = di_muon    (L1_muons,  5, 3, qual1=12, qual2=12, maxMass=4)

    seeds['L1_DoubleMu_10_1_Q8_maxMass4p0'              ] = di_muon    (L1_muons, 10, 1, qual1= 8, qual2= 8, maxMass=4)
    seeds['L1_DoubleMu_9_1_Q8_maxMass4p0'               ] = di_muon    (L1_muons,  9, 1, qual1= 8, qual2= 8, maxMass=4)
    seeds['L1_DoubleMu_8_3_Q8_maxMass4p0'               ] = di_muon    (L1_muons,  8, 3, qual1= 8, qual2= 8, maxMass=4)
    seeds['L1_DoubleMu_6_2_Q8_maxMass4p0'               ] = di_muon    (L1_muons,  6, 2, qual1= 8, qual2= 8, maxMass=4)
    seeds['L1_DoubleMu_5_3_Q8_maxMass4p0'               ] = di_muon    (L1_muons,  5, 3, qual1= 8, qual2= 8, maxMass=4)

    seeds['L1_DoubleMu_10_1_Q12_maxMass4p0_OS'          ] = di_muon    (L1_muons, 10, 1, qual1=12, qual2=12, maxMass=4, sign=0)
    seeds['L1_DoubleMu_9_1_Q12_maxMass4p0_0S'           ] = di_muon    (L1_muons,  9, 1, qual1=12, qual2=12, maxMass=4, sign=0)
    seeds['L1_DoubleMu_8_3_Q12_maxMass4p0_0S'           ] = di_muon    (L1_muons,  8, 3, qual1=12, qual2=12, maxMass=4, sign=0)
    seeds['L1_DoubleMu_6_2_Q12_maxMass4p0_0S'           ] = di_muon    (L1_muons,  6, 2, qual1=12, qual2=12, maxMass=4, sign=0)
    seeds['L1_DoubleMu_5_3_Q12_maxMass4p0_0S'           ] = di_muon    (L1_muons,  5, 3, qual1=12, qual2=12, maxMass=4, sign=0)

    seeds['L1_DoubleMu_10_1_Q8_maxMass4p0_0S'           ] = di_muon    (L1_muons, 10, 1, qual1= 8, qual2= 8, maxMass=4, sign=0)
    seeds['L1_DoubleMu_9_1_Q8_maxMass4p0_0S'            ] = di_muon    (L1_muons,  9, 1, qual1= 8, qual2= 8, maxMass=4, sign=0)
    seeds['L1_DoubleMu_8_3_Q8_maxMass4p0_0S'            ] = di_muon    (L1_muons,  8, 3, qual1= 8, qual2= 8, maxMass=4, sign=0)
    seeds['L1_DoubleMu_6_2_Q8_maxMass4p0_0S'            ] = di_muon    (L1_muons,  6, 2, qual1= 8, qual2= 8, maxMass=4, sign=0)
    seeds['L1_DoubleMu_5_3_Q8_maxMass4p0_0S'            ] = di_muon    (L1_muons,  5, 3, qual1= 8, qual2= 8, maxMass=4, sign=0)

    seeds['L1_DoubleMu0er1p5_SQ_OS_dR_Max1p4'           ] = di_muon    (L1_muons,  0, 0, eta1=1.5, eta2=1.5, qual1=12, qual2=12, maxDr=1.4, sign=0)
    seeds['L1_TripleMu_5_3_0_DoubleMu_5_3_OS_Mass_Max17'] = tri_muon   (L1_muons,  5, 3, 0, maxMass=17, sign=0)
    seeds['L1_DoubleMu4_SQ_OS_dR_Max1p2'                ] = di_muon    (L1_muons,  4  , 4  , qual1=12, qual2=12, maxDr=1.2, sign=0)
    seeds['L1_DoubleMu4p5_SQ_OS_dR_Max1p2'              ] = di_muon    (L1_muons,  4.5, 4.5, qual1=12, qual2=12, maxDr=1.2, sign=0)

    unpackedBs = array('f',seeds.values())      
    ntuple.Fill(unpackedBs)

    for k, v in seeds.iteritems():
        acceptance.Fill(k, v>0)

f.cd()
ntuple.Write()

acceptance.Scale(1./float(passed))
acceptance.SetMinimum(0.)
acceptance.SetMaximum(1.05)
acceptance.Draw('HIST')
acceptance.Write()

f.Close()


