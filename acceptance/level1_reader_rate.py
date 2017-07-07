import ROOT
from DataFormats.FWLite import Events, Handle
from PhysicsTools.HeppyCore.utils.deltar import deltaR, deltaPhi
from itertools import product, combinations
from collections import OrderedDict
from math import cos, cosh, sqrt
from array import array

# ROOT.gROOT.SetBatch()
ROOT.gStyle.SetOptStat(0)

events = Events([    
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/040A544E-0453-E711-A625-02163E013655.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/0864A5B3-3058-E711-886F-02163E0141B0.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/0AB055D3-2B53-E711-B336-02163E013945.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/0C2CB6FF-0253-E711-A114-02163E01A621.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/0EB1FB4A-0453-E711-8880-02163E013817.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/0EDDB396-3D58-E711-A702-02163E01A2DE.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/12ACB347-1953-E711-9BF1-02163E01386F.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/141F32BA-3058-E711-9724-02163E01A347.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/144B7B2A-1953-E711-9654-02163E0144CA.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/14ACA168-1753-E711-8DD4-02163E0142B4.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/16C9A83C-0E53-E711-8229-02163E014761.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/2055146E-3A53-E711-ACEB-02163E01385A.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/2225999D-2253-E711-87D9-02163E013586.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/2227814A-0453-E711-91F1-02163E013768.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/2267D8C2-3058-E711-AABB-02163E011875.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/22BD828E-1953-E711-AB1E-02163E01464C.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/2AF6EF93-0653-E711-AE5B-02163E0138BC.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/2E11A0BA-1553-E711-92C0-02163E011EF1.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/307471F6-4353-E711-A1F0-02163E014541.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/309252AD-0653-E711-BF3B-02163E011CAB.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/32CD7FF5-3058-E711-8911-02163E0144E6.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/346F3101-0753-E711-8D68-02163E01379F.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/34A3FF2F-0353-E711-80CE-02163E011F19.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/34F68AB0-3058-E711-BE14-02163E019E70.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/382868A6-0453-E711-98D6-02163E01264B.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/3A24F0B2-3058-E711-B90F-02163E019E64.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/3AA83C76-0653-E711-97B2-02163E0124BA.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/3C5D7B1D-0F53-E711-9282-02163E013630.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/3E7D5154-0353-E711-9F97-02163E0125D5.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/4262E841-0453-E711-982E-02163E01356C.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/46820554-0653-E711-9EFC-02163E0136D3.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/46A278BE-3058-E711-889B-02163E01A453.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/48AC3AF8-2353-E711-9504-02163E011867.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/4C4D26B5-3058-E711-AADD-02163E013613.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/4CDBF9B0-2D53-E711-8981-02163E0119C1.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/4CDC23BA-3058-E711-9BE2-02163E01A30E.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/4E2A9A8E-0453-E711-8001-02163E01339A.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/4E4C639F-3058-E711-8008-02163E014779.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/50A550D8-0453-E711-A8F6-02163E011D9F.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/5287E3F9-0253-E711-97DA-02163E014188.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/529EDC1B-0353-E711-B36B-02163E013613.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/549C897F-0653-E711-B4D3-02163E013577.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/58A2545E-2053-E711-A3BA-02163E013810.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/5E14B0B6-0D53-E711-8191-02163E01A6C9.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/5E44A881-0653-E711-9F78-02163E013623.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/60940EB7-0453-E711-AAEE-02163E011FB1.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/60A9A783-1653-E711-B4CE-02163E01372F.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/62ADFCBD-3058-E711-86D8-02163E014208.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/660962B7-3058-E711-B0F7-02163E019E81.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/68252B57-1D53-E711-BD39-02163E0146F8.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/68F69380-1953-E711-A307-02163E01422D.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/6A131587-3153-E711-A80F-02163E013911.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/6A4C2BD4-3058-E711-8D36-02163E019E6F.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/6A69817C-1553-E711-9999-02163E011807.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/6C3E9D5D-2353-E711-A1C2-02163E013627.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/708A12CC-2153-E711-BBF2-02163E013768.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/70909DD0-1D53-E711-903B-02163E014242.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/709AD9DD-0653-E711-B91D-02163E012348.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/70A7D0FD-0553-E711-9DD2-02163E014204.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/70C2DF2C-1B53-E711-A3E2-02163E013959.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/729A2F07-3553-E711-8F6A-02163E011BA9.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/72B6B464-0453-E711-86B5-02163E013765.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/72B8BA7D-0653-E711-8592-02163E011C64.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/7415F802-0353-E711-9354-02163E0121E4.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/7621E709-1853-E711-AF98-02163E013406.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/7AABE626-0453-E711-A995-02163E0142F3.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/7AF49E22-4353-E711-BF8B-02163E0133EB.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/7C4752E5-0453-E711-B668-02163E014522.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/7C9FC39D-0553-E711-BFD4-02163E014235.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/7E3ACCDB-1253-E711-95A8-02163E014106.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/7EA664CA-0653-E711-9DEA-02163E011CB0.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/801CE3C7-3058-E711-B962-02163E01A1E9.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/8047A2A1-1753-E711-B4EF-02163E0141F1.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/82B206D0-3058-E711-A232-02163E014210.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/82F2DABA-0453-E711-9B6F-02163E0144AD.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/866B7DB0-3058-E711-95EA-02163E0144DB.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/8688D128-0653-E711-ADA4-02163E01289A.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/869C9420-0F53-E711-BBDD-02163E013703.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/889987BC-3058-E711-A11A-02163E014574.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/88C4C7C4-2B53-E711-9857-02163E0128F8.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/8C8073B7-3158-E711-98CA-02163E014575.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/8C86EF8A-0453-E711-BCC2-02163E011A37.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/8E657D20-1953-E711-ADFB-02163E01461B.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/8EFF47EC-0653-E711-8046-02163E014781.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/9029AB65-3F58-E711-95B4-02163E01445B.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/9416A1F1-3058-E711-8012-02163E012384.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/94552EE1-0153-E711-A7C1-02163E011D43.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/94BEA737-0F53-E711-99C4-02163E01394B.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/9677A779-0353-E711-8689-02163E014712.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/96C7F833-0253-E711-892E-02163E014371.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/96E83E20-0453-E711-8B8E-02163E01415D.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/9845B1E5-3058-E711-9320-02163E013885.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/987F6D66-0553-E711-9564-02163E014787.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/9889648D-1953-E711-AF82-02163E0122B6.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/9AA26D40-2E53-E711-8982-02163E0128B7.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/9C382544-0353-E711-B786-02163E012345.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/9C7957D7-0653-E711-AB5D-02163E011988.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/9E6D5F00-0353-E711-BE60-02163E0136AE.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/9E9E25D8-0653-E711-BF02-02163E014444.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/9EBC6CC6-3058-E711-99D0-02163E01A1C5.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/A0063992-0653-E711-9C4F-02163E013523.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/A04E3BA3-0553-E711-A5D1-02163E012204.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/A2A7DEBA-3058-E711-87D9-02163E019B4A.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/A4C9C6AC-0553-E711-B29F-02163E014536.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/A4EF3F76-0653-E711-8C1F-02163E013555.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/A6131646-0353-E711-BABF-02163E0143A1.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/A6792BAE-0653-E711-95CB-02163E014613.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/AC71308A-0453-E711-91F5-02163E014180.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/AEBD5F83-0653-E711-AC16-02163E013759.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/B44F95B9-1153-E711-9FB0-02163E014105.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/B82381A3-C753-E711-9C9D-02163E0119FB.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/B8656A9B-3158-E711-B23C-02163E013468.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/B8FCCCD4-3058-E711-9A50-02163E0146B0.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/BA18DD13-0553-E711-921B-02163E0135AB.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/BC0D4DB3-3058-E711-8801-02163E013392.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/BE67F01E-0753-E711-8ECD-02163E014351.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/BE96F979-1953-E711-B842-02163E0140D5.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/BEC2B9B3-1153-E711-82FA-02163E011C99.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/C2432083-1A53-E711-A379-02163E014255.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/C298E4BF-0553-E711-AA29-02163E0118F2.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/C2C707B6-3058-E711-8FF6-02163E01385F.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/C608966C-0653-E711-9E8C-02163E0139CE.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/C83C6C79-0653-E711-8E54-02163E01420D.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/CC50AA91-4C53-E711-A311-02163E0140ED.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/CE128EB5-3058-E711-9D8F-02163E011D21.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/D24E5541-5758-E711-893E-02163E014200.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/D4CC3F00-3353-E711-94CC-02163E0141FC.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/D6641D9F-3058-E711-9AF6-02163E01A76C.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/D67303AD-1953-E711-829B-02163E0137EB.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/D6E036B9-3058-E711-8C4A-02163E013673.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/D87EFFED-2953-E711-99B2-02163E01362B.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/D8808C36-0253-E711-9869-02163E014352.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/D89E51CA-3058-E711-BD21-02163E01A5BE.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/D8D14E60-0653-E711-81ED-02163E013591.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/DC9A3D7B-1653-E711-9885-02163E01416A.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/DCC8F6AD-0653-E711-8570-02163E014290.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/DCC97E0E-3B53-E711-81C0-02163E0144F6.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/E05AF6DE-3058-E711-8929-02163E019DA2.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/E259459C-2853-E711-B306-02163E013475.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/E471E100-3153-E711-BA77-02163E011C31.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/E4D925A4-0453-E711-A841-02163E01364A.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/E69D650D-3B53-E711-9827-02163E0136AE.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/E84C7436-3953-E711-A0C1-02163E014145.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/E8EB67AC-3058-E711-A4F4-02163E01A48B.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/EA707DDA-FC52-E711-A37F-02163E0140F3.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/EAC758A1-8058-E711-8883-02163E0145DE.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/EC9F9262-0653-E711-B354-02163E013677.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/F04EB8CD-3058-E711-9C51-02163E01A48D.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/F251E3CD-0553-E711-9C52-02163E0140D5.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/F2704EB9-3058-E711-B558-02163E014667.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/F28CA3E8-3058-E711-9760-02163E011BEA.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/F28CE79F-0353-E711-8345-02163E0136BA.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/F2C141BB-3058-E711-B1E7-02163E0146DC.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/F4B074CE-3058-E711-884D-02163E013555.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/F6ED1719-1853-E711-BFE9-02163E0135B1.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/F8528835-0653-E711-B598-02163E014757.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/FABABEAB-3058-E711-B916-02163E011BBE.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/FAD71D34-1853-E711-AEBA-02163E013793.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/FC32ACDB-0253-E711-972A-02163E0144AA.root',
    'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/FE43B171-6D58-E711-86BC-02163E011865.root',




#     'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/786/00000/040A544E-0453-E711-A625-02163E013655.root',
#     'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RECO/PromptReco-v3/000/296/663/00000/0C40FCDC-5C58-E711-8393-02163E01A50C.root',
#     'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RAW/v1/000/296/786/00000/02543371-0751-E711-9761-02163E01369C.root',
#     'root://cms-xrd-global.cern.ch//store/data/Run2017A/ZeroBias1/RAW/v1/000/296/786/00000/04A28D56-FF50-E711-B627-02163E01440A.root',
][:20])


# handle_L1muons = Handle('BXVector<l1t::Muon>')
# label_L1muon   = ('gtStage2Digis', 'Muon') 

handle_L1muons = Handle('BXVector<l1t::Muon>')
label_L1muon   = ('gmtStage2Digis', 'Muon') 



acceptance = ROOT.TH1F('L1acceptance_rate', 'L1acceptance_rate', 25, 0, 25)


mykeys = [
    'L1_SingleMu_25_qual12',
    'L1_DoubleMu_0_0_qual8',
    'L1_DoubleMu_0_0_qual12',
    'L1_DoubleMu_11_4_qual8',
    'L1_DoubleMu_11_4_qual12',
    'L1_DoubleMu_13_6_qual8',
    'L1_DoubleMu_13_6_qual12',
    'L1_DoubleMu_15_8_qual8',
    'L1_DoubleMu_15_8_qual12',
    'L1_DoubleMu_10_5_qual8_maxMass4',
    'L1_DoubleMu_10_5_qual12_maxMass4',
    'L1_DoubleMu_10_5_qual8_maxApproxMass4',
    'L1_DoubleMu_10_5_qual12_maxApproxMass4',
    'L1_DoubleMu_10_5_qual8_maxDR1p0',
    'L1_DoubleMu_10_5_qual12_maxDR1p0',
    'L1_DoubleMu_8_3_qual8_maxMass4',
    'L1_DoubleMu_8_3_qual12_maxMass4',
    'L1_DoubleMu_8_3_qual8_maxApproxMass4',
    'L1_DoubleMu_8_3_qual12_maxApproxMass4',
    'L1_DoubleMu_8_3_qual8_maxDR1p0',
    'L1_DoubleMu_8_3_qual12_maxDR1p0', 
    'L1_TripleMu_8_3_0_qual8_maxMass4',
    'L1_TripleMu_8_3_0_qual12_maxMass4',
    'L1_TripleMu_8_3_0_qual8_maxApproxMass4',
    'L1_TripleMu_8_3_0_qual12_maxApproxMass4',
]


ntuple = ROOT.TNtuple('tree','tree',':'.join(mykeys))
f = ROOT.TFile('acceptance_rate.root', 'recreate')

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
        seeds[kk] = 0

    for mu in L1_muons:
        if mu.pt()>25. and mu.hwQual()>=12: seeds['L1_SingleMu_25_qual12'  ] += 1

    qual8muons = [mm for mm in L1_muons if mm.hwQual()>=8]
    for mu_1, mu_2 in combinations(qual8muons, 2):
        
        mu_1_p4_atVtx = ROOT.TLorentzVector()
        mu_1_p4_atVtx.SetPtEtaPhiM(mu_1.pt(), mu_1.etaAtVtx(), mu_1.phiAtVtx(), 0.105658)

        mu_2_p4_atVtx = ROOT.TLorentzVector()
        mu_2_p4_atVtx.SetPtEtaPhiM(mu_2.pt(), mu_2.etaAtVtx(), mu_2.phiAtVtx(), 0.105658)
    
        mass        = (mu_1_p4_atVtx + mu_2_p4_atVtx).M()
        mass_approx = sqrt(2. * mu_1.pt() * mu_2.pt() * (cosh(mu_1.etaAtVtx() - mu_2.etaAtVtx()) - cos(mu_1.phiAtVtx() - mu_2.phiAtVtx())))
        dR          = mu_1_p4_atVtx.DeltaR(mu_2_p4_atVtx)
    
        if mu_1.pt() >  0. and mu_2.pt() > 0.                     : seeds['L1_DoubleMu_0_0_qual8'                 ] += 1
        if mu_1.pt() > 11. and mu_2.pt() > 4.                     : seeds['L1_DoubleMu_11_4_qual8'                ] += 1
        if mu_1.pt() > 13. and mu_2.pt() > 6.                     : seeds['L1_DoubleMu_13_6_qual8'                ] += 1
        if mu_1.pt() > 15. and mu_2.pt() > 8.                     : seeds['L1_DoubleMu_15_8_qual8'                ] += 1
        if mu_1.pt() > 10. and mu_2.pt() > 5. and mass < 4.       : seeds['L1_DoubleMu_10_5_qual8_maxMass4'       ] += 1
        if mu_1.pt() > 10. and mu_2.pt() > 5. and mass_approx < 4.: seeds['L1_DoubleMu_10_5_qual8_maxApproxMass4' ] += 1
        if mu_1.pt() > 10. and mu_2.pt() > 5. and dR < 1.         : seeds['L1_DoubleMu_10_5_qual8_maxDR1p0'       ] += 1
        if mu_1.pt() >  8. and mu_2.pt() > 3. and mass < 4.       : seeds['L1_DoubleMu_8_3_qual8_maxMass4'        ] += 1
        if mu_1.pt() >  8. and mu_2.pt() > 3. and mass_approx < 4.: seeds['L1_DoubleMu_8_3_qual8_maxApproxMass4'  ] += 1
        if mu_1.pt() >  8. and mu_2.pt() > 3. and dR < 1.         : seeds['L1_DoubleMu_8_3_qual8_maxDR1p0'        ] += 1
        if mu_1.pt() >  8. and mu_2.pt() > 3. and mass < 4.        and len(qual8muons)>=3: seeds['L1_TripleMu_8_3_0_qual8_maxMass4'        ] += 1
        if mu_1.pt() >  8. and mu_2.pt() > 3. and mass_approx < 4. and len(qual8muons)>=3: seeds['L1_TripleMu_8_3_0_qual8_maxApproxMass4'  ] += 1

    qual12muons = [mm for mm in L1_muons if mm.hwQual()>=12]
    for mu_1, mu_2 in combinations(qual12muons, 2):
        
        mu_1_p4_atVtx = ROOT.TLorentzVector()
        mu_1_p4_atVtx.SetPtEtaPhiM(mu_1.pt(), mu_1.etaAtVtx(), mu_1.phiAtVtx(), 0.105658)

        mu_2_p4_atVtx = ROOT.TLorentzVector()
        mu_2_p4_atVtx.SetPtEtaPhiM(mu_2.pt(), mu_2.etaAtVtx(), mu_2.phiAtVtx(), 0.105658)
    
        mass        = (mu_1_p4_atVtx + mu_2_p4_atVtx).M()
        mass_approx = sqrt(2. * mu_1.pt() * mu_2.pt() * (cosh(mu_1.etaAtVtx() - mu_2.etaAtVtx()) - cos(mu_1.phiAtVtx() - mu_2.phiAtVtx())))
        dR          = mu_1_p4_atVtx.DeltaR(mu_2_p4_atVtx)
    
        if mu_1.pt() >  0. and mu_2.pt() > 0.                     : seeds['L1_DoubleMu_0_0_qual12'                ] += 1
        if mu_1.pt() > 11. and mu_2.pt() > 4.                     : seeds['L1_DoubleMu_11_4_qual12'               ] += 1
        if mu_1.pt() > 13. and mu_2.pt() > 6.                     : seeds['L1_DoubleMu_13_6_qual12'               ] += 1
        if mu_1.pt() > 15. and mu_2.pt() > 8.                     : seeds['L1_DoubleMu_15_8_qual12'               ] += 1
        if mu_1.pt() > 10. and mu_2.pt() > 5. and mass < 4.       : seeds['L1_DoubleMu_10_5_qual12_maxMass4'      ] += 1
        if mu_1.pt() > 10. and mu_2.pt() > 5. and mass_approx < 4.: seeds['L1_DoubleMu_10_5_qual12_maxApproxMass4'] += 1
        if mu_1.pt() > 10. and mu_2.pt() > 5. and dR < 1.         : seeds['L1_DoubleMu_10_5_qual12_maxDR1p0'      ] += 1
        if mu_1.pt() >  8. and mu_2.pt() > 3. and mass < 4.       : seeds['L1_DoubleMu_8_3_qual12_maxMass4'       ] += 1
        if mu_1.pt() >  8. and mu_2.pt() > 3. and mass_approx < 4.: seeds['L1_DoubleMu_8_3_qual12_maxApproxMass4' ] += 1
        if mu_1.pt() >  8. and mu_2.pt() > 3. and dR < 1.         : seeds['L1_DoubleMu_8_3_qual12_maxDR1p0'       ] += 1
        if mu_1.pt() >  8. and mu_2.pt() > 3. and mass < 4.        and len(qual12muons)>=3: seeds['L1_TripleMu_8_3_0_qual12_maxMass4'        ] += 1
        if mu_1.pt() >  8. and mu_2.pt() > 3. and mass_approx < 4. and len(qual12muons)>=3: seeds['L1_TripleMu_8_3_0_qual12_maxApproxMass4'  ] += 1

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


