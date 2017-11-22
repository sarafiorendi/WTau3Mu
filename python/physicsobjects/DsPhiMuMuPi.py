import math

import numpy as np
from itertools import combinations, product

from PhysicsTools.HeppyCore.utils.deltar import deltaR, deltaPhi
from ROOT import TVector3, Math

global m_k   ; m_k   = 0.493677   # GeV
global m_pi  ; m_pi  = 0.13957061 # GeV
global m_ds  ; m_ds  = 1.96828    # GeV
global m_phi ; m_phi = 1.0195     # GeV

class DsPhiMuMuPi(object):
    ''' 
    '''
    def __init__(self, muons, pion):
        self.muons = muons
        self.pion = pion
        self.pion.setMass(m_pi)

    def mu1(self):
        return sorted(self.muons, key = lambda mu : mu.pt(), reverse = True)[0]

    def mu2(self):
        return sorted(self.muons, key = lambda mu : mu.pt(), reverse = True)[1]

    def mup(self):
        return [mu for mu in self.muons if mu.charge() == 1][0]

    def mum(self):
        return [mu for mu in self.muons if mu.charge() == -1][0]

    def pi(self):
        return self.pion
    
    def p4(self):
        return self.mu1().p4() + self.mu2().p4() + self.pi().p4()
     
    def phi_resonance(self):
        return self.mu1().p4() + self.mu2().p4()
    
    def has_phi(self, width=20):
        '''
        delta mass < widths (in MeV)
        '''
        return abs(self.phi_resonance().mass() - m_phi) < 0.001 * width
        
    def charge(self):
        return sum([self.mu1().charge(), self.mu2().charge(), self.pi().charge()])

    def pt(self):
        return self.p4().pt()

    def eta(self):
        return self.p4().eta()

    def phi(self):
        return self.p4().phi()

    def mass(self):
        return self.p4().mass()