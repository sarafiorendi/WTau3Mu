import math

from itertools import combinations, product

from PhysicsTools.HeppyCore.utils.deltar import deltaR, deltaPhi
from PhysicsTools.Heppy.physicsobjects.PhysicsObjects import Muon
from CMGTools.WTau3Mu.analyzers.resonances import resonances, sigmas_to_exclude
from ROOT import TVector3

class Tau3MuMET(object):

    ''' 
    '''

    def __init__(self, muons, met):
        muons = sorted(muons, key=lambda mu : mu.pt(), reverse=True)
        self.mu1_ = muons[0]
        self.mu2_ = muons[1]
        self.mu3_ = muons[2]
        self.met_ = met        
        self.checkResonances()
        
    def checkResonances(self):
        '''
        Save info about di-muon resonances, including whether the two muons are OS or SS.
        Negative is SS.
        '''
        self.vetoResonance3sigma = 0
        self.vetoResonance2sigma = 0
        
        masses = [
            (self.mass12(), self.charge12(),  0), 
            (self.mass13(), self.charge13(), 10), 
            (self.mass23(), self.charge23(), 20),
        ]
        
        for mm in masses:
            distance = lambda rr : abs(mm[0]-rr[0]) / rr[1]
            resonance = sorted(resonances, key=distance)[0]
            id = (mm[2] + resonance[2]) * ((mm[1]==0) - (mm[1]!=0))
            if distance(resonance) < 3. :
                self.vetoResonance3sigma = id
            if distance(resonance) < 2. :
                self.vetoResonance2sigma = id

        
    def sumPt(self):
        return self.p4().pt()

    def sumPtMuons(self):
        return self.p4Muons().pt()
        
    def mass(self):
        return self.p4().mass()

    def massMuons(self):
        return self.p4Muons().mass()

    def mass12(self):
        return (self.mu1().p4() + self.mu2().p4()).mass()

    def mass13(self):
        return (self.mu1().p4() + self.mu3().p4()).mass()

    def mass23(self):
        return (self.mu2().p4() + self.mu3().p4()).mass()

    def charge12(self):
        return self.mu1().charge() + self.mu2().charge()

    def charge13(self):
        return self.mu1().charge() + self.mu3().charge()

    def charge23(self):
        return self.mu2().charge() + self.mu3().charge()

    def dR12(self):
        return deltaR(self.mu1().p4(), self.mu2().p4())

    def dR13(self):
        return deltaR(self.mu1().p4(), self.mu3().p4())

    def dR23(self):
        return deltaR(self.mu2().p4(), self.mu3().p4())

    def dRtauMET(self):
        return deltaR(self.p4Muons(), self.met())

    def dRtauMuonMax(self):
        return max([deltaR(self.p4Muons(), mu) for mu in [self.mu1(), self.mu2(), self.mu3()]])

    def p4(self):
        return self.mu1().p4() + self.mu2().p4() + self.mu3().p4() + self.met().p4()

    def p4Muons(self):
        return self.mu1().p4() + self.mu2().p4() + self.mu3().p4()

    def mu1(self):
        return self.mu1_

    def mu2(self):
        return self.mu2_

    def mu3(self):
        return self.mu3_

    def charge(self):
        return self.mu1().charge() + self.mu2().charge() + self.mu3().charge()
        
    def met(self):
        return self.met_

    def calcPZeta(self):
        mu1PT = TVector3(self.mu1().p4().x(), self.mu1().p4().y(), 0.)
        mu2PT = TVector3(self.mu2().p4().x(), self.mu2().p4().y(), 0.)
        mu3PT = TVector3(self.mu3().p4().x(), self.mu3().p4().y(), 0.)
        metPT = TVector3(self.met().p4().x(), self.met().p4().y(), 0.)
        zetaAxis = (mu1PT.Unit() + mu2PT.Unit() + mu3PT.Unit()).Unit()
        self.pZetaVis_ = mu1PT*zetaAxis + mu2PT*zetaAxis + mu3PT*zetaAxis
        self.pZetaMET_ = metPT*zetaAxis

    def mt1(self):
        mt1 = self.calcMT(self.mu1().p4(), self.met())
        return mt1

    def mt2(self):
        mt2 = self.calcMT(self.mu2().p4(), self.met())
        return mt2

    def mt3(self):
        mt3 = self.calcMT(self.mu3().p4(), self.met())
        return mt3

    def mttau(self):
        mttau = self.calcMT(self.p4Muons(), self.met())
        return mttau

    def mtTotal12(self):
        mtTotal12 = self.mt1()**2 + \
                    self.mt2()**2 + \
                    self.calcMT(self.mu1(), self.mu2())**2
        return math.sqrt(mtTotal12)

    def mtTotal13(self):
        mtTotal13 = self.mt1()**2 + \
                    self.mt3()**2 + \
                    self.calcMT(self.mu1(), self.mu3())**2
        return math.sqrt(mtTotal13)

    def mtTotal23(self):
        mtTotal23 = self.mt2()**2 + \
                    self.mt3()**2 + \
                    self.calcMT(self.mu2(), self.mu3())**2
        return math.sqrt(mtTotal23)

    def mtSumMuons(self):
        return self.mt1() + self.mt2() + self.mt3()

    def mtSqSumMuons(self):
        return math.sqrt(self.mt1()**2 + self.mt2()**2 + self.mt3()**2)

    # Calculate the transverse mass with the same algorithm
    # as previously in the C++ DiObject class
    @staticmethod
    def calcMT(cand1, cand2):
        pt = cand1.pt() + cand2.pt()
        px = cand1.px() + cand2.px()
        py = cand1.py() + cand2.py()
        try:
            return math.sqrt(pt*pt - px*px - py*py)
        except ValueError:
            print 'Funny rounding issue', pt, px, py
            print cand1.px(), cand1.py(), cand1.pt()
            print cand2.px(), cand2.py(), cand2.pt()
            return 0.

#     @staticmethod
#     def calcMtTotal(cands):
#         return math.sqrt(sum(DiObject.calcMT(c1, c2)**2 for c1, c2 in combinations(cands, 2)))

    def __getattr__(self, name):
        '''Redefine getattr to original version.'''
        raise AttributeError

#     def __str__(self):
#         header = '{cls}: mvis={mvis}, sumpT={sumpt}'.format(
#             cls=self.__class__.__name__,
#             mvis=self.mass(),
#             sumpt=self.sumPt())
#         return '\n'.join([header,
#                           '\t'+str(self.leg1()),
#                           '\t'+str(self.leg2())])
