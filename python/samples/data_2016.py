import PhysicsTools.HeppyCore.framework.config as cfg
import os

#####COMPONENT CREATOR

from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator
kreator = ComponentCreator()

json = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/ReReco/Final/Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON.txt'


DoubleMuonLowMass_Run2016B_23Sep2016     = kreator.makeDataComponent("DoubleMuonLowMass_Run2016B_23Sep2016"    , "/DoubleMuonLowMass/Run2016B-23Sep2016-v3/MINIAOD" , "CMS", ".*root", json, useAAA=True)
DoubleMuonLowMass_Run2016C_23Sep2016     = kreator.makeDataComponent("DoubleMuonLowMass_Run2016C_23Sep2016"    , "/DoubleMuonLowMass/Run2016C-23Sep2016-v1/MINIAOD" , "CMS", ".*root", json, useAAA=True)
DoubleMuonLowMass_Run2016D_23Sep2016     = kreator.makeDataComponent("DoubleMuonLowMass_Run2016D_23Sep2016"    , "/DoubleMuonLowMass/Run2016D-23Sep2016-v1/MINIAOD" , "CMS", ".*root", json, useAAA=True)
DoubleMuonLowMass_Run2016E_23Sep2016     = kreator.makeDataComponent("DoubleMuonLowMass_Run2016E_23Sep2016"    , "/DoubleMuonLowMass/Run2016E-23Sep2016-v1/MINIAOD" , "CMS", ".*root", json, useAAA=True)
DoubleMuonLowMass_Run2016F_23Sep2016     = kreator.makeDataComponent("DoubleMuonLowMass_Run2016F_23Sep2016"    , "/DoubleMuonLowMass/Run2016F-23Sep2016-v1/MINIAOD" , "CMS", ".*root", json, useAAA=True)
DoubleMuonLowMass_Run2016G_23Sep2016     = kreator.makeDataComponent("DoubleMuonLowMass_Run2016G_23Sep2016"    , "/DoubleMuonLowMass/Run2016G-23Sep2016-v1/MINIAOD" , "CMS", ".*root", json, useAAA=True)

DoubleMuonLowMass_Run2016H_PromptReco_v1 = kreator.makeDataComponent("DoubleMuonLowMass_Run2016H_PromptReco_v1", "/DoubleMuonLowMass/Run2016H-PromptReco-v1/MINIAOD", "CMS", ".*root", json, useAAA=True)
DoubleMuonLowMass_Run2016H_PromptReco_v2 = kreator.makeDataComponent("DoubleMuonLowMass_Run2016H_PromptReco_v2", "/DoubleMuonLowMass/Run2016H-PromptReco-v2/MINIAOD", "CMS", ".*root", json, useAAA=True)
DoubleMuonLowMass_Run2016H_PromptReco_v3 = kreator.makeDataComponent("DoubleMuonLowMass_Run2016H_PromptReco_v3", "/DoubleMuonLowMass/Run2016H-PromptReco-v3/MINIAOD", "CMS", ".*root", json, useAAA=True)

datasamplesDoubleMuLowMass23Sept2017 = [
    DoubleMuonLowMass_Run2016B_23Sep2016    ,
    DoubleMuonLowMass_Run2016C_23Sep2016    ,
    DoubleMuonLowMass_Run2016D_23Sep2016    ,
    DoubleMuonLowMass_Run2016E_23Sep2016    ,
    DoubleMuonLowMass_Run2016F_23Sep2016    ,
    DoubleMuonLowMass_Run2016G_23Sep2016    ,
    DoubleMuonLowMass_Run2016H_PromptReco_v1,
    DoubleMuonLowMass_Run2016H_PromptReco_v2,
    DoubleMuonLowMass_Run2016H_PromptReco_v3,
]

DoubleMuonLowMass_Run2016Bv1_03Feb2017     = kreator.makeDataComponent("DoubleMuonLowMass_Run2016Bv1_03Feb2017"    , "/DoubleMuonLowMass/Run2016B-03Feb2017_ver1-v1/MINIAOD" , "CMS", ".*root", json) #, useAAA=True)
DoubleMuonLowMass_Run2016Bv2_03Feb2017     = kreator.makeDataComponent("DoubleMuonLowMass_Run2016Bv2_03Feb2017"    , "/DoubleMuonLowMass/Run2016B-03Feb2017_ver2-v2/MINIAOD" , "CMS", ".*root", json) #, useAAA=True)
DoubleMuonLowMass_Run2016C_03Feb2017       = kreator.makeDataComponent("DoubleMuonLowMass_Run2016C_03Feb2017"      , "/DoubleMuonLowMass/Run2016C-03Feb2017-v1/MINIAOD"      , "CMS", ".*root", json) #, useAAA=True)
DoubleMuonLowMass_Run2016D_03Feb2017       = kreator.makeDataComponent("DoubleMuonLowMass_Run2016D_03Feb2017"      , "/DoubleMuonLowMass/Run2016D-03Feb2017-v1/MINIAOD"      , "CMS", ".*root", json, useAAA=True)
DoubleMuonLowMass_Run2016E_03Feb2017       = kreator.makeDataComponent("DoubleMuonLowMass_Run2016E_03Feb2017"      , "/DoubleMuonLowMass/Run2016E-03Feb2017-v1/MINIAOD"      , "CMS", ".*root", json, useAAA=True)
DoubleMuonLowMass_Run2016F_03Feb2017       = kreator.makeDataComponent("DoubleMuonLowMass_Run2016F_03Feb2017"      , "/DoubleMuonLowMass/Run2016F-03Feb2017-v1/MINIAOD"      , "CMS", ".*root", json, useAAA=True)
DoubleMuonLowMass_Run2016G_03Feb2017       = kreator.makeDataComponent("DoubleMuonLowMass_Run2016G_03Feb2017"      , "/DoubleMuonLowMass/Run2016G-03Feb2017-v1/MINIAOD"      , "CMS", ".*root", json, useAAA=True)
DoubleMuonLowMass_Run2016Hv2_03Feb2017     = kreator.makeDataComponent("DoubleMuonLowMass_Run2016Hv2_03Feb2017"    , "/DoubleMuonLowMass/Run2016H-03Feb2017_ver2-v1/MINIAOD" , "CMS", ".*root", json) #, useAAA=True)
DoubleMuonLowMass_Run2016Hv3_03Feb2017     = kreator.makeDataComponent("DoubleMuonLowMass_Run2016Hv3_03Feb2017"    , "/DoubleMuonLowMass/Run2016H-03Feb2017_ver3-v1/MINIAOD" , "CMS", ".*root", json, useAAA=True)

datasamplesDoubleMuLowMass03Feb2017 = [
    DoubleMuonLowMass_Run2016Bv1_03Feb2017,
    DoubleMuonLowMass_Run2016Bv2_03Feb2017,
    DoubleMuonLowMass_Run2016C_03Feb2017  ,
    DoubleMuonLowMass_Run2016D_03Feb2017  ,
    DoubleMuonLowMass_Run2016E_03Feb2017  ,
    DoubleMuonLowMass_Run2016F_03Feb2017  ,
    DoubleMuonLowMass_Run2016G_03Feb2017  ,
    DoubleMuonLowMass_Run2016Hv2_03Feb2017,
    DoubleMuonLowMass_Run2016Hv3_03Feb2017,
]



DoubleMuonLowMass_Run2016Bv1_18Apr2017 = kreator.makeDataComponent("DoubleMuonLowMass_Run2016Bv1_18Apr2017" , "/DoubleMuonLowMass/Run2016B-18Apr2017_ver1-v1/MINIAOD" , "CMS", ".*root", json, useAAA=True)
DoubleMuonLowMass_Run2016Bv2_18Apr2017 = kreator.makeDataComponent("DoubleMuonLowMass_Run2016Bv2_18Apr2017" , "/DoubleMuonLowMass/Run2016B-18Apr2017_ver2-v1/MINIAOD" , "CMS", ".*root", json, useAAA=True)
DoubleMuonLowMass_Run2016C_18Apr2017   = kreator.makeDataComponent("DoubleMuonLowMass_Run2016C_18Apr2017"   , "/DoubleMuonLowMass/Run2016C-18Apr2017-v1/MINIAOD"      , "CMS", ".*root", json, useAAA=True)
DoubleMuonLowMass_Run2016D_18Apr2017   = kreator.makeDataComponent("DoubleMuonLowMass_Run2016D_18Apr2017"   , "/DoubleMuonLowMass/Run2016D-18Apr2017-v1/MINIAOD"      , "CMS", ".*root", json, useAAA=True)
DoubleMuonLowMass_Run2016E_18Apr2017   = kreator.makeDataComponent("DoubleMuonLowMass_Run2016E_18Apr2017"   , "/DoubleMuonLowMass/Run2016E-18Apr2017-v1/MINIAOD"      , "CMS", ".*root", json, useAAA=True)
DoubleMuonLowMass_Run2016F_18Apr2017   = kreator.makeDataComponent("DoubleMuonLowMass_Run2016F_18Apr2017"   , "/DoubleMuonLowMass/Run2016F-18Apr2017-v1/MINIAOD"      , "CMS", ".*root", json, useAAA=True)
DoubleMuonLowMass_Run2016G_18Apr2017   = kreator.makeDataComponent("DoubleMuonLowMass_Run2016G_18Apr2017"   , "/DoubleMuonLowMass/Run2016G-18Apr2017-v1/MINIAOD"      , "CMS", ".*root", json, useAAA=True)
DoubleMuonLowMass_Run2016H_18Apr2017   = kreator.makeDataComponent("DoubleMuonLowMass_Run2016H_18Apr2017"   , "/DoubleMuonLowMass/Run2016H-18Apr2017-v1/MINIAOD"      , "CMS", ".*root", json, useAAA=True)

datasamplesDoubleMuLowMass = [
    DoubleMuonLowMass_Run2016Bv1_18Apr2017,
    DoubleMuonLowMass_Run2016Bv2_18Apr2017,
    DoubleMuonLowMass_Run2016C_18Apr2017  ,
    DoubleMuonLowMass_Run2016D_18Apr2017  ,
    DoubleMuonLowMass_Run2016E_18Apr2017  ,
    DoubleMuonLowMass_Run2016F_18Apr2017  ,
    DoubleMuonLowMass_Run2016G_18Apr2017  ,
    DoubleMuonLowMass_Run2016H_18Apr2017  ,
]
