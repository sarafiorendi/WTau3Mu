import ROOT
import math
from array import array
from copy import deepcopy as dc
from collections import OrderedDict
from itertools import product, combinations, groupby
from DataFormats.FWLite import Events, Handle
from PhysicsTools.HeppyCore.utils.deltar import deltaR, deltaPhi

def finalDaughters(gen, daughters=None):
    if daughters is None:
        daughters = []
    for i in range(gen.numberOfDaughters()):
        daughter = gen.daughter(i)
        if daughter.numberOfDaughters() == 0:
            daughters.append(daughter)
        else:
            finalDaughters(daughter, daughters)
    return daughters

def findMVAmet(muons, met, event):
    
#     print '==============================================================================='
#     print 'reco muon pts'
#     for imu in muons:
#         print imu.pt(), imu.eta(), imu.phi()
#     print 'recomuons ', muons
    for imet in met:
    
        metmuons = [imet.userCand(iname).get() for iname in imet.userCandNames()]
        
        if len(metmuons)!=3:
            continue
     
        matched = 0
        
#         print 'metmuons  ', metmuons, '  ', [mm.pt() for mm in metmuons]
        
        already_matched = []
        for i, j in product(metmuons, muons):
            if i==j and j not in already_matched:
                already_matched.append(j)
                matched += 1

        if matched == 3:
            return imet
            break   
    
#     import pdb ; pdb.set_trace()
    return False

events = Events('output.root') # make sure this corresponds to your file name!
# events = Events('output_test.root') # make sure this corresponds to your file name!
maxevents = -1 # max events to process
totevents = events.size() # total number of events in the files

output = ROOT.TFile('mvamet_tuple.root', 'recreate')

branches = [
    'run',
    'lumi',
    'event',
    'met_gen_pt',
    'met_gen_phi',
    'met_pf_pt',
    'met_pf_phi',
    'met_mva_pt',
    'met_mva_phi',
    'u_parallel_genmet',
    'u_perp_genmet',
    'u_parallel_pfmet',
    'u_perp_pfmet',
    'u_parallel_mvamet',
    'u_perp_mvamet',    
]

ntuple = ROOT.TNtuple('tree', 'tree', ':'.join(branches))

tofill = OrderedDict(zip(branches, [-99.]*len(branches)))         

handles = OrderedDict()

handles['muons' ] = ( ('slimmedMuons'                 , ''      , 'PAT'   ), Handle('std::vector<pat::Muon>')        )
handles['pfmet' ] = ( ('slimmedMETs'                  , ''      , 'PAT'   ), Handle('std::vector<pat::MET>')         )
handles['mvamet'] = ( ('MVAMET'                       , 'MVAMET', 'MVAMET'), Handle('std::vector<pat::MET>')         )
handles['vtx'   ] = ( ('offlineSlimmedPrimaryVertices', ''      , 'PAT'   ), Handle('std::vector<reco::Vertex>')     )
handles['genp'  ] = ( ('prunedGenParticles'           , ''      , 'PAT'   ), Handle('std::vector<reco::GenParticle>'))

# start looping on the events
for i, ev in enumerate(events):

    for k, v in tofill.iteritems():
        tofill[k] = -99.

    tofill['run'  ] = ev.eventAuxiliary().run()
    tofill['lumi' ] = ev.eventAuxiliary().luminosityBlock()
    tofill['event'] = ev.eventAuxiliary().event()
    
    # controls on the events being processed
    if maxevents>0 and i>maxevents:
        break
        
    if i%100==0:
        print '===> processing %d / %d event' %(i, totevents)
    
    # access the collections
    for k, v in handles.iteritems():
        ev.getByLabel(v[0], v[1])
        setattr(ev, k, v[1].product())

    gen_muons = [pp for pp in ev.genp if abs(pp.pdgId())==13 and abs(pp.mother().pdgId())==15]
    
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
    

    goodmuons = []
        
    for mm, gg in product(ev.muons, gen_muons):
        if deltaR(mm, gg)<0.1:
            goodmuons.append(mm)
    
    goodmuons = list(set(goodmuons))

    if len(goodmuons)!=3:
        continue

    ev.selmuons = [mu for mu in goodmuons if (mu.isLooseMuon() or mu.isSoftMuon(ev.vtx[0])) and abs(mu.eta())<2.5 and mu.pt()>1.]
        
    if len(ev.selmuons)<3:
        continue

#     print '\n\n\>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'
#     print 'run, lumi, event ', ev.eventAuxiliary().run(), ev.eventAuxiliary().luminosityBlock(), ev.eventAuxiliary().event()
#     print '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'

    mvamet = findMVAmet(ev.selmuons, ev.mvamet, ev)

    if not(mvamet):
        print 'no MVA MET found, probably the needed leptons were not considered!'
        continue
        #import pdb ; pdb.set_trace()

    gen_neutrinos = [pp for pp in ev.genp if abs(pp.pdgId()) in (12,14,16) and pp.status()==1]
    
    try:
        gen_tau = [pp for pp in ev.genp if abs(pp.pdgId())==15 and abs(pp.mother().pdgId())==24 \
                                                               and sum([abs(mm.pdgId())==13 for mm in finalDaughters(pp)])>=3][0]
    except:
        import pdb ; pdb.set_trace()
    
    gen_w = gen_tau.mother()
        
    gen_met = ROOT.Math.LorentzVector('ROOT::Math::PxPyPzE4D<double>')()
    
    for nn in gen_neutrinos:
        gen_met += nn.p4()

    minus_gen_w = -gen_w.p4()

    dphi_genw_genmet = deltaPhi(minus_gen_w.phi(), gen_met    .phi())
    dphi_genw_pfmet  = deltaPhi(minus_gen_w.phi(), ev.pfmet[0].phi())
    dphi_genw_mvamet = deltaPhi(minus_gen_w.phi(), mvamet     .phi())

    u_parallel_genmet = gen_met.pt() * math.cos(dphi_genw_genmet)
    u_perp_genmet     = gen_met.pt() * math.sin(dphi_genw_genmet)

    u_parallel_pfmet  = ev.pfmet[0].pt() * math.cos(dphi_genw_pfmet)
    u_perp_pfmet      = ev.pfmet[0].pt() * math.sin(dphi_genw_pfmet)

    u_parallel_mvamet = mvamet.pt() * math.cos(dphi_genw_mvamet)
    u_perp_mvamet     = mvamet.pt() * math.sin(dphi_genw_mvamet)

    tofill['met_gen_pt' ] = gen_met.pt()
    tofill['met_gen_phi'] = gen_met.phi()
    tofill['met_pf_pt'  ] = ev.pfmet[0].pt()
    tofill['met_pf_phi' ] = ev.pfmet[0].phi()
    tofill['met_mva_pt' ] = mvamet.pt() 
    tofill['met_mva_phi'] = mvamet.phi()
    tofill['u_parallel_genmet'] = u_parallel_genmet
    tofill['u_perp_genmet'    ] = u_perp_genmet    
    tofill['u_parallel_pfmet' ] = u_parallel_pfmet 
    tofill['u_perp_pfmet'     ] = u_perp_pfmet     
    tofill['u_parallel_mvamet'] = u_parallel_mvamet
    tofill['u_perp_mvamet'    ] = u_perp_mvamet    

    ntuple.Fill(array('f',tofill.values()))
    
output.cd()
ntuple.Write()
output.Close()

