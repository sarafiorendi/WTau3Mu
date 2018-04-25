import numpy as np
import ROOT

wps      = np.array([0.65, 0.70, 0.75, 0.80, 0.82, 0.84, 0.86, 0.88, 0.89, 0.90, 0.91, 0.92, 0.94])
wps_e    = np.zeros(len(wps))
barrel_limits   = np.array([2.81867, 2.55552, 2.29428, 1.99327, 1.89269, 1.91608, 1.88469, 1.76336, 1.80577, 1.9062 , 1.78615, 1.94445, 3.05])
barrel_limits_e = np.array([0.0925592, 0.0197767, 0.0221227, 0.0203744, 0.0219458, 0.0149632, 0.0183493, 0.0451528, 0.0138079, 0.0148415, 0.0123472, 0.0216324, 0.024312])



# endcap_limits   = np.array([5.78571, 5.47774, 5.08777, 4.78788, 4.84398, 4.97659, 4.87085])
# endcap_limits_e = np.array([0.0976633, 0.0297398, 0.121979 , 0.217867 , 0.0502   , 0.0923287, 0.0353994])





c1 = ROOT.TCanvas('c1', 'c1', 700, 700)
g1 = ROOT.TGraphErrors(len(wps), wps, barrel_limits, wps_e, barrel_limits_e)
g1.SetTitle('')
g1.GetXaxis().SetTitle('BDT WP')
g1.GetYaxis().SetTitle('limit on BR(#tau#rightarrow3#mu) at 90% CL [Belle unit]')
g1.GetYaxis().SetTitleOffset(1.45)
g1.SetMarkerStyle(8)
g1.SetLineColor(ROOT.kRed)
g1.Draw('APL')
c1.SaveAs('limit_scan.pdf')



# 
# 
# Limit: r < 2.81867 +/- 0.0925592 @ 90% CL
# Limit: r < 2.55552 +/- 0.0197767 @ 90% CL
# Limit: r < 2.29428 +/- 0.0221227 @ 90% CL
# Limit: r < 1.99327 +/- 0.0203744 @ 90% CL
# Limit: r < 1.89269 +/- 0.0219458 @ 90% CL
# Limit: r < 1.91608 +/- 0.0149632 @ 90% CL
# Limit: r < 1.88469 +/- 0.0183493 @ 90% CL
# Limit: r < 1.76336 +/- 0.0451528 @ 90% CL
# Limit: r < 1.80577 +/- 0.0138079 @ 90% CL
# Limit: r < 1.9062  +/- 0.0148415 @ 90% CL
# Limit: r < 1.78615 +/- 0.0123472 @ 90% CL
# Limit: r < 1.94445 +/- 0.0216324 @ 90% CL
# Limit: r < 3.05    +/- 0.024312 @ 90% CL
# 
# 
# 
# 



