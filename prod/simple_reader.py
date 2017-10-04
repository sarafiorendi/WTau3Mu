import ROOT
from DataFormats.FWLite import Events, Handle


# events = Events ('/afs/cern.ch/work/m/manzoni/tauHLT/2017/CMSSW_9_1_0_pre3/src/Tau3Mu/outputFULL.root')
events = Events ('output.root')

handle = Handle ('std::vector<pat::Muon>')
label  = ("slimmedMuons")


handle_barrel = Handle('vector<pair<edm::Ptr<pat::Muon>,TLorentzVector> >')
label_barrel  = ("extrapolator", "MB2extrap") 

handle_endcapP = Handle('vector<pair<edm::Ptr<pat::Muon>,TLorentzVector> >')
label_endcapP = ("extrapolator", "ME2Pextrap") 

handle_endcapM = Handle('vector<pair<edm::Ptr<pat::Muon>,TLorentzVector> >')
label_endcapM = ("extrapolator", "ME2Mextrap") 

ROOT.gROOT.SetBatch()

for i, event in enumerate(events):
    if i>0:
        break
        
#     event.getByLabel (label, handle)
#     muons = handle.product()
#     if len(muons):
#         muons[0].track().pt()

# event = events[0]
event.getByLabel (label, handle)
muons = handle.product()


event.getByLabel(label_barrel, handle_barrel)
muonsL1Barrel = handle_barrel.product()

event.getByLabel(label_endcapP, handle_endcapP)
muonsL1EndcapP = handle_endcapP.product()

event.getByLabel(label_endcapM, handle_endcapM)
muonsL1EndcapM = handle_endcapM.product()

for i in range(6):
    print muons[i].pt(), muonsL1Barrel[i].second.Phi(), muonsL1EndcapM[i].second.Phi(), muonsL1EndcapP[i].second.Phi()
    print muons[i].pt(), muonsL1Barrel[i].second.Eta(), muonsL1EndcapM[i].second.Eta(), muonsL1EndcapP[i].second.Eta()


# if len(muons):
#     muons[0].track().pt()






