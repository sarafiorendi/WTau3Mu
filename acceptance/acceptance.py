import ROOT
from DataFormats.FWLite import Events, Handle
from PhysicsTools.HeppyCore.utils.deltar import deltaR, deltaPhi
from itertools import product, combinations, groupby
from collections import OrderedDict
from math import cos, cosh, sqrt
from array import array

# ROOT.gROOT.SetBatch()
ROOT.gStyle.SetOptStat(0)

events = Events ([
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
][:1])

handle = Handle ('std::vector<pat::Muon>')
label  = ('slimmedMuons')

handle_gen = Handle('vector<reco::GenParticle>')
label_gen = ('prunedGenParticles')


# acceptance = ROOT.TH1F('L1acceptance', 'L1acceptance', 25, 0, 25)


# ntuple = ROOT.TNtuple('tree','tree',':'.join(mykeys))
# f = ROOT.TFile('acceptance.root', 'recreate')

passed = 0
in_the_acceptance = 0
totevents = events.size()
for i, event in enumerate(events):
#     if i>10:
#         break
        
    if i%100==0:
        print '===> processing %d / %d event' %(i, totevents)
        
    event.getByLabel (label, handle)
    muons = handle.product()

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

    goodmuons = []
        
    for mm, gg in product(muons, gen_muons):
        if deltaR(mm, gg)<0.1:
            goodmuons.append(mm)
    
    goodmuons = list(set(goodmuons))
    goodmuons.sort(key = lambda x : x.pt(), reverse = True)

    if len(goodmuons)!=3:
        continue
    
    passed += 1 
    


print 'run on %d signal events' %totevents
print '       %d signal events have ALL muons inside the tracker acceptance' %in_the_acceptance
print '       %d signal events are eventually reconstructed at offline' %passed




# f.cd()
# ntuple.Write()
# f.Close()        


# acceptance.Scale(1./float(passed))
# acceptance.SetMinimum(0.)
# acceptance.SetMaximum(1.05)
# acceptance.Draw('HIST')



#     for mu in L1_muons:
#         if mu.hwQual>=8 and mu.hwQual: seeds['L1_DoubleMu_0_0_qual8'] += 1
#         if mu.hwQual>=12: seeds['L1_DoubleMu_0_0_qual8'] += 1


    
#     print '\t offline muons pt eta phi'
#     for mu in goodmuons: print '\t\t', mu.pt(), mu.eta(), mu.phi()
#     print '\t online L3 muons pt eta phi'
#     for mu in L3muons: print '\t\t', mu.pt(), mu.eta(), mu.phi()
#     print '\t online merged muons pt eta phi'
#     for mu in AllHLTmuons: print '\t\t', mu.pt(), mu.eta(), mu.phi()




