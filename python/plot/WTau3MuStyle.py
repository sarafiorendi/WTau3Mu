from ROOT import TColor, kViolet, kBlue, kRed, kAzure

class Style:

    def __init__(self,
                 markerStyle=8,
                 markerColor=1,
                 markerSize=1,
                 lineStyle=1,
                 lineColor=1,
                 lineWidth=2,
                 fillColor=None,
                 fillStyle=1001,
                 drawAsData=False):
        self.markerStyle = markerStyle
        self.markerColor = markerColor
        self.markerSize = markerSize
        self.lineStyle = lineStyle
        self.lineColor = lineColor
        self.lineWidth = lineWidth
        if fillColor is None:
            self.fillColor = lineColor
        else:
            self.fillColor = fillColor
        self.fillStyle = fillStyle
        self.drawAsData = drawAsData

    def formatHisto(self, hist, title=None):
        hist.SetMarkerStyle(self.markerStyle)
        hist.SetMarkerColor(self.markerColor)
        hist.SetMarkerSize(self.markerSize)
        hist.SetLineStyle(self.lineStyle)
        hist.SetLineColor(self.lineColor)
        hist.SetLineWidth(self.lineWidth)
        hist.SetFillColor(self.fillColor)
        hist.SetFillStyle(self.fillStyle)
        if title != None:
            hist.SetTitle(title)
        return hist

# the following standard files are defined and ready to be used.
# more standard styles can be added on demand.
# user defined styles can be created in the same way in any python module

sBlack  = Style()
sData   = Style(fillStyle=0, markerSize=1.3, drawAsData=True)
sBlue   = Style(markerColor=4, fillColor=4)
sGreen  = Style(markerColor=8, fillColor=8)
sRed    = Style(markerColor=2, fillColor=2)
sYellow = Style(lineColor=1, markerColor=5, fillColor=5)
sViolet = Style(lineColor=1, markerColor=kViolet, fillColor=kViolet)

# John's colours
qcdcol     = TColor.GetColor(250,202,255)
dycol      = TColor.GetColor(248,206,104)
wcol       = TColor.GetColor(222,90,106)
ttcol      = TColor.GetColor(155,152,204)
zlcol      = TColor.GetColor(100,182,232)
dibosoncol = TColor.GetColor(222,90,106)


# Signals
sWT3M_Signal = Style(lineColor=kBlue, markerColor=0, lineStyle=2, fillColor=0, lineWidth=3)


sBlackSquares = Style(markerStyle=21)
sBlueSquares  = Style(lineColor=4, markerStyle=21, markerColor=4)
sGreenSquares = Style(lineColor=8, markerStyle=21, markerColor=8)
sRedSquares   = Style(lineColor=2, markerStyle=21, markerColor=2)


styleSet = [sBlue, sGreen, sRed, sYellow, sViolet, sBlackSquares, sBlueSquares, sGreenSquares, sRedSquares]
iStyle = 0

def nextStyle():
    global iStyle
    style = styleSet[iStyle]
    iStyle = iStyle+1
    if iStyle >= len(styleSet):
        iStyle = 0
    return style

histPref = {}
histPref['Data'  ] = {'style':sData, 'layer':2999, 'legend':'Observed'}
histPref['data_*'] = {'style':sData, 'layer':2999, 'legend':'Observed'}
histPref['Signal'] = {'style':sWT3M_Signal, 'layer':1001, 'legend':'W#rightarrow#tau#nu, #tau#rightarrow#mu#mu#mu BR = 10^{-7}'}

