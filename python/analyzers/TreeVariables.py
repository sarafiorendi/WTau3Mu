import ROOT

from PhysicsTools.HeppyCore.utils.deltar import deltaR, deltaPhi

from CMGTools.H2TauTau.proto.analyzers.tauIDs import tauIDs, tauIDs_extra

class Variable():
    def __init__(self, name, function=None, type=float):
        self.name = name
        self.function = function
        if function is None:
            # Note: works for attributes, not member functions
            self.function = lambda x : getattr(x, self.name, -999.) 
        self.type = type

def default():
    return -999.

# event variables
event_vars = [
    Variable('run', type=int),
    Variable('lumi', type=int),
    Variable('event', lambda ev : ev.eventId, type=int),
    Variable('bx', lambda ev : (ev.input.eventAuxiliary().bunchCrossing() * ev.input.eventAuxiliary().isRealData()), type=int),
    Variable('orbit_number', lambda ev : (ev.input.eventAuxiliary().orbitNumber() * ev.input.eventAuxiliary().isRealData()), type=int),
    Variable('is_data', lambda ev: ev.input.eventAuxiliary().isRealData(), type=int),
    Variable('nPU', lambda ev : -99 if getattr(ev, 'nPU', -1) is None else getattr(ev, 'nPU', -1)),
    Variable('rho', lambda ev : ev.rho),
    Variable('Flag_HBHENoiseFilter', type=int),
    Variable('Flag_HBHENoiseIsoFilter', type=int),
    Variable('Flag_EcalDeadCellTriggerPrimitiveFilter', type=int),
    Variable('Flag_goodVertices', type=int),
    Variable('Flag_eeBadScFilter', type=int),
    Variable('Flag_globalTightHalo2016Filter', type=int),
    Variable('passBadMuonFilter', type=int),
    Variable('passBadChargedHadronFilter', type=int),
    Variable('n_muons'    , lambda ev : len(ev.muons), type=int),
    Variable('n_electrons', lambda ev : len(ev.electrons), type=int),
    Variable('n_taus'     , lambda ev : len(ev.taus), type=int),
    Variable('n_candidates', lambda ev : ev.ncands, type=int),
]

# triplet variables
triplet_vars = [
    Variable('vetoResonance2sigma', type=int),
    Variable('vetoResonance3sigma', type=int),
    Variable('sumPt', lambda cand : cand.sumPt()),
    Variable('sumPtMuons', lambda cand : cand.sumPtMuons()),
    Variable('charge', lambda cand : cand.charge()),
    Variable('mass', lambda cand : cand.mass()),
    Variable('massMuons', lambda cand : cand.massMuons()),
    Variable('mass12', lambda cand : cand.mass12()),
    Variable('mass13', lambda cand : cand.mass13()),
    Variable('mass23', lambda cand : cand.mass23()),
    Variable('charge12', lambda cand : cand.charge12(), type=int),
    Variable('charge13', lambda cand : cand.charge13(), type=int),
    Variable('charge23', lambda cand : cand.charge23(), type=int),
    Variable('mt1', lambda cand : cand.mt1()),
    Variable('mt2', lambda cand : cand.mt2()),
    Variable('mt3', lambda cand : cand.mt3()),
    Variable('mttau', lambda cand : cand.mttau()),
    Variable('mtTotal12', lambda cand : cand.mtTotal12()),
    Variable('mtTotal13', lambda cand : cand.mtTotal13()),
    Variable('mtTotal23', lambda cand : cand.mtTotal23()),
    Variable('mtSumMuons', lambda cand : cand.mtSumMuons()),
    Variable('mtSqSumMuons', lambda cand : cand.mtSqSumMuons()),
    Variable('dR12', lambda cand : cand.dR12()),
    Variable('dR13', lambda cand : cand.dR13()),
    Variable('dR23', lambda cand : cand.dR23()),
    Variable('dRtauMET', lambda cand : cand.dRtauMET()),
    Variable('dRtauMuonMax', lambda cand : cand.dRtauMuonMax()),
    Variable('tau_dBetaIsoCone0p8strength0p2_abs'),
    Variable('tau_dBetaIsoCone0p8strength0p2_rel'),
    Variable('absChargedFromPV'),
    Variable('absChargedFromPU'),
    Variable('absPhotonRaw'),
]

# generic particle
particle_vars = [
    Variable('pt'    , lambda p: p.pt() ),
    Variable('eta'   , lambda p: p.eta()),
    Variable('phi'   , lambda p: p.phi()),
    Variable('charge', lambda p: p.charge() if hasattr(p, 'charge') else 0), # charge may be non-integer for gen particles
    Variable('mass'  , lambda p: p.mass()),
]

# stage-2 L1 object
l1obj_vars = [
    Variable('iso'  , lambda p: p.hwIso()),
    Variable('qual' , lambda p: p.hwQual()),
    Variable('type' , lambda p: p.type),
    Variable('bx'   , lambda p: p.bx),
    Variable('index', lambda p: p.index),
]

# generic lepton
lepton_vars = [
    Variable('dxy', lambda lep : lep.dxy()),
    Variable('dxy_error', lambda lep : lep.edxy() if hasattr(lep, 'edxy') else lep.dxy_error()),
    Variable('dz', lambda lep : lep.leadChargedHadrCand().dz() if hasattr(lep, 'leadChargedHadrCand') else lep.dz()),
    Variable('dz_error', lambda lep : lep.edz() if hasattr(lep, 'edz') else -1.),
    Variable('weight'),
#     Variable('weight_trigger', lambda lep : getattr(lep, 'weight_trigger', 1.)),
#     Variable('eff_trigger_data', lambda lep : getattr(lep, 'eff_data_trigger', -999.)),
#     Variable('eff_trigger_mc', lambda lep : getattr(lep, 'eff_mc_trigger', -999.)),
    Variable('weight_idiso', lambda lep : getattr(lep, 'weight_idiso', 1.)),
#     Variable('eff_idiso_data', lambda lep : getattr(lep, 'eff_data_idiso', -999.)),
#     Variable('eff_idiso_mc', lambda lep : getattr(lep, 'eff_mc_idiso', -999.)),
    Variable('gen_match')
]

# electron
electron_vars = [
    # Variable('eid_nontrigmva_loose', lambda ele : ele.mvaIDRun2("NonTrigPhys14", "Loose")),
    Variable('eid_nontrigmva_loose', lambda ele : ele.mvaRun2('NonTrigSpring15MiniAOD')),
    Variable('eid_nontrigmva_tight', lambda ele : ele.mvaIDRun2("NonTrigSpring15MiniAOD", "POG80")),
    Variable('eid_veto', lambda ele : ele.cutBasedId('POG_SPRING15_25ns_v1_Veto')),
    Variable('eid_loose', lambda ele : ele.cutBasedId('POG_SPRING15_25ns_v1_Loose')),
    Variable('eid_medium', lambda ele : ele.cutBasedId('POG_SPRING15_25ns_v1_Medium')),
    Variable('eid_tight', lambda ele : ele.cutBasedId('POG_SPRING15_25ns_v1_Tight')),
    Variable('nhits_missing', lambda ele : ele.physObj.gsfTrack().hitPattern().numberOfHits(1), int),
    Variable('pass_conv_veto', lambda ele : ele.passConversionVeto()),
    Variable('reliso05', lambda lep : lep.relIsoR(R=0.3, dBetaFactor=0.5, allCharged=0)),
    Variable('reliso05_04', lambda lep : lep.relIsoR(R=0.4, dBetaFactor=0.5, allCharged=0)),
    Variable('reliso05_04', lambda lep : lep.relIsoR(R=0.4, dBetaFactor=0.5, allCharged=0)),
    Variable('weight_tracking', lambda lep : getattr(lep, 'weight_tracking', 1.)),
]

# vertex
vertex_vars = [
    Variable('covxx'           , lambda vtx : vtx.covariance(0,0)                         ),
    Variable('covyy'           , lambda vtx : vtx.covariance(1,1)                         ),
    Variable('covzz'           , lambda vtx : vtx.covariance(2,2)                         ),
    Variable('covxy'           , lambda vtx : vtx.covariance(0,1)                         ),
    Variable('covxz'           , lambda vtx : vtx.covariance(0,2)                         ),
    Variable('covyz'           , lambda vtx : vtx.covariance(1,2)                         ),
    Variable('chi2'            , lambda vtx : vtx.chi2()                                  ),
    Variable('dimension'                                                        , type=int),
    Variable('isValid'         , lambda vtx : vtx.isValid()                     , type=int),
    Variable('nTracks'         , lambda vtx : vtx.nTracks()                     , type=int),
    Variable('ndof'            , lambda vtx : vtx.ndof()                                  ),
    Variable('normalizedChi2'  , lambda vtx : vtx.normalizedChi2()              , type=int),
    Variable('x'               , lambda vtx : vtx.x()                                     ),
    Variable('y'               , lambda vtx : vtx.y()                                     ),
    Variable('z'               , lambda vtx : vtx.z()                                     ),
    Variable('xError'          , lambda vtx : vtx.xError()                                ),
    Variable('yError'          , lambda vtx : vtx.yError()                                ),
    Variable('zError'          , lambda vtx : vtx.zError()                                ),
    Variable('prob'            , lambda vtx : ROOT.TMath.Prob(vtx.chi2(), int(vtx.ndof()))),
    Variable('ls'                                                                         ),
    Variable('cos'                                                                        ),
]

# muon
muon_vars = [
    Variable('reliso05'         , lambda muon : muon.relIsoR(R=0.4, dBetaFactor=0.5, allCharged=0)),
    Variable('reliso05_03'      , lambda muon : muon.relIsoR(R=0.3, dBetaFactor=0.5, allCharged=0)),
    Variable('muonid_soft'      , lambda muon : muon.isSoftMuon(muon.associatedVertex)            ),
    Variable('muonid_loose'     , lambda muon : muon.muonID('POG_ID_Loose')                       ),
    Variable('muonid_medium'    , lambda muon : muon.muonID('POG_ID_Medium_ICHEP')                ),
    Variable('muonid_tight'     , lambda muon : muon.muonID('POG_ID_Tight')                       ),
    Variable('muonid_tightnovtx', lambda muon : muon.muonID('POG_ID_TightNoVtx')                  ),
    Variable('muonid_highpt'    , lambda muon : muon.muonID('POG_ID_HighPt')                      ),
    # ask quality first...
#     Variable('dxy_innertrack', lambda muon : muon.innerTrack().dxy(muon.associatedVertex.position())),
#     Variable('dz_innertrack', lambda muon : muon.innerTrack().dz(muon.associatedVertex.position())),
    Variable('weight_tracking'  , lambda muon : getattr(muon, 'weight_tracking', 1.)),
]

# tau
tau_vars = [
    Variable('decayMode', lambda tau : tau.decayMode()),
    Variable('zImpact', lambda tau : tau.zImpact()),
    Variable('dz_selfvertex', lambda tau : tau.vertex().z() - tau.associatedVertex.position().z()),
    Variable('ptScale', lambda tau : getattr(tau, 'ptScale', -999.)),
    Variable('NewMVAID'),
    Variable('NewMVAraw'),
]
for tau_id in tauIDs:
    if type(tau_id) is str:
        # Need to use eval since functions are otherwise bound to local
        # variables
        tau_vars.append(Variable(tau_id, eval('lambda tau : tau.tauID("{id}")'.format(id=tau_id))))
    else:
        sum_id_str = ' + '.join('tau.tauID("{id}")'.format(id=tau_id[0].format(wp=wp)) for wp in tau_id[1])
        tau_vars.append(Variable(tau_id[0].format(wp=''), 
            eval('lambda tau : ' + sum_id_str), int))

tau_vars_extra = []
for tau_id in tauIDs_extra:
    if type(tau_id) is str:
        # Need to use eval since functions are otherwise bound to local
        # variables
        tau_vars_extra.append(Variable(tau_id, eval('lambda tau : tau.tauID("{id}")'.format(id=tau_id))))
    else:
        sum_id_str = ' + '.join('tau.tauID("{id}")'.format(id=tau_id[0].format(wp=wp)) for wp in tau_id[1])
        tau_vars_extra.append(Variable(tau_id[0].format(wp=''), 
            eval('lambda tau : ' + sum_id_str), int))


# jet
jet_vars = [
    Variable('mva_pu', lambda jet : jet.puMva('pileupJetId:fullDiscriminant')),
    # Variable('id_loose', lambda jet : jet.looseJetId()),
    Variable('id_pu', lambda jet : jet.puJetId() + jet.puJetId(wp='medium') + jet.puJetId(wp='tight')),
    # Variable('area', lambda jet : jet.jetArea()),
    Variable('flavour_parton', lambda jet : jet.partonFlavour()),
    Variable('csv', lambda jet : jet.btagMVA),
    Variable('genjet_pt', lambda jet : jet.matchedGenJet.pt() if hasattr(jet, 'matchedGenJet') and jet.matchedGenJet else -999.),
]

# extended jet vars
jet_vars_extra = [
    Variable('nConstituents', lambda jet : getattr(jet, 'nConstituents', default)()),
    Variable('rawFactor', lambda jet : getattr(jet, 'rawFactor', default)()),
    Variable('chargedHadronEnergy', lambda jet : getattr(jet, 'chargedHadronEnergy', default)()),
    Variable('neutralHadronEnergy', lambda jet : getattr(jet, 'neutralHadronEnergy', default)()),
    Variable('neutralEmEnergy', lambda jet : getattr(jet, 'neutralEmEnergy', default)()),
    Variable('muonEnergy', lambda jet : getattr(jet, 'muonEnergy', default)()),
    Variable('chargedEmEnergy', lambda jet : getattr(jet, 'chargedEmEnergy', default)()),
    Variable('chargedHadronMultiplicity', lambda jet : getattr(jet, 'chargedHadronMultiplicity', default)()),
    Variable('chargedMultiplicity', lambda jet : getattr(jet, 'chargedMultiplicity', default)()),
    Variable('neutralMultiplicity', lambda jet : getattr(jet, 'neutralMultiplicity', default)()),
]


# gen info
geninfo_vars = [
    Variable('geninfo_mcweight', lambda ev : getattr(ev, 'mcweight', 1.)),
    Variable('geninfo_nup', lambda ev : getattr(ev, 'NUP', -1), type=int),
    Variable('geninfo_htgen', lambda ev : getattr(ev, 'genPartonHT', -1)),
    Variable('geninfo_invmass', lambda ev : getattr(ev, 'geninvmass', -1)),
    Variable('weight_gen'),
    Variable('genmet_pt'),
    # Variable('genmet_eta'),
    # Variable('genmet_e'),
    # Variable('genmet_px'),
    # Variable('genmet_py'),
    Variable('genmet_phi'),
]

vbf_vars = [
    Variable('mjj'),
    Variable('deta'),
    Variable('n_central20', lambda vbf : len(vbf.centralJets), int),
    Variable('n_central', lambda vbf : sum([1 for j in vbf.centralJets if j.pt() > 30.]), int),
    Variable('jdphi', lambda vbf : vbf.dphi),
    Variable('dijetpt'),
    Variable('dijetphi'),
    Variable('dphidijethiggs'),
    Variable('mindetajetvis', lambda vbf : vbf.visjeteta),
]
