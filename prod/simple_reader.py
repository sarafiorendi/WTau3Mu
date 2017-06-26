import ROOT
from DataFormats.FWLite import Events, Handle


# events = Events ('/afs/cern.ch/work/m/manzoni/tauHLT/2017/CMSSW_9_1_0_pre3/src/Tau3Mu/outputFULL.root')
events = Events ('output.root')

handle = Handle ('std::vector<pat::Muon>')
label  = ("slimmedMuons")


handle_bis = Handle ('vector<pair<edm::Ptr<pat::Muon>,TLorentzVector> >')
label_bis  = ("extrapolator", "MB2extrap") 

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


event.getByLabel (label_bis, handle_bis)
muonsL1Barrel = handle_bis.product()

# if len(muons):
#     muons[0].track().pt()






