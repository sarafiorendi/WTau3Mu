import ROOT
from itertools import combinations
from math import cos, cosh, sqrt

def single_muon(muons, pt, eta=2.5, qual=8):
    
    for mu in muons:
        if mu.hwQual()   < qual: continue
        if mu.pt()       < pt  : continue
        if abs(mu.eta()) > eta : continue
        return True
    
    return False
    

def di_muon(muons, pt1, pt2, eta1=2.5, eta2=2.5, 
            qual1=8, qual2=8, minMass=-1., 
            maxMass=1.E10, minDr=-1., maxDr=1.E10, sign=-1):
    
    muons.sort(key = lambda x : x.pt(), reverse = True)
    
    for mu1, mu2 in combinations(muons, 2):
        if mu1.hwQual() < qual1: continue
        if mu2.hwQual() < qual2: continue

        if mu1.pt() < pt1: continue
        if mu2.pt() < pt2: continue
    
        if abs(mu1.eta()) > eta1: continue
        if abs(mu2.eta()) > eta2: continue
        
        if abs(mu1.charge() + mu2.charge())!=sign and sign>=0: continue

        mu1_p4_atVtx = ROOT.TLorentzVector()
        mu1_p4_atVtx.SetPtEtaPhiM(mu1.pt(), mu1.etaAtVtx(), mu1.phiAtVtx(), 0.105658)
    
        mu2_p4_atVtx = ROOT.TLorentzVector()
        mu2_p4_atVtx.SetPtEtaPhiM(mu2.pt(), mu2.etaAtVtx(), mu2.phiAtVtx(), 0.105658)
        
        mass        = (mu1_p4_atVtx + mu2_p4_atVtx).M()
        mass_approx = sqrt(2. * mu1.pt() * mu2.pt() * (cosh(mu1.etaAtVtx() - mu2.etaAtVtx()) - cos(mu1.phiAtVtx() - mu2.phiAtVtx())))
        dR          = mu1_p4_atVtx.DeltaR(mu2_p4_atVtx)
        
        if mass_approx < minMass: continue 
        if mass_approx > maxMass: continue 
        
        if dR < minDr: continue
        if dR > maxDr: continue
        
        return True
    
    return False


def tri_muon(muons, pt1, pt2, pt3, eta1=2.5, eta2=2.5, eta3=2.5, 
             qual1=8, qual2=8, qual3=8, minMass=-1., 
             maxMass=1.E10, minDr=-1., maxDr=1.E10, sign=-1):
    
    passed = False

    if len(muons) < 3:
        return False

    muons.sort(key = lambda x : x.pt(), reverse = True)    
    triplets = combinations(muons, 3)
    
    for mu1, mu2, mu3 in triplets:
        if mu1.hwQual() < qual1: continue
        if mu2.hwQual() < qual2: continue
        if mu3.hwQual() < qual3: continue

        if mu1.pt() < pt1: continue
        if mu2.pt() < pt2: continue
        if mu3.pt() < pt3: continue
    
        if abs(mu1.eta()) > eta1: continue
        if abs(mu2.eta()) > eta2: continue
        if abs(mu3.eta()) > eta2: continue
    
        passed = di_muon([mu1, mu2, mu3], pt1, pt2, eta1, eta2, 
                         qual1, qual2, minMass, 
                         maxMass, minDr, maxDr, sign)
                         
        if passed:        
            return True
    
    return False
