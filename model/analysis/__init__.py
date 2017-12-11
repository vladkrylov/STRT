import ROOT as r
import numpy as np

def fit_Landau(values, gap):
    gap = float(gap)
    bin_width = 1./gap
    xmin = min(values)/gap
    xmax = max(values)/gap
    nbins = int(np.fix((xmax - xmin)) / bin_width)
    xmax = xmin + nbins*bin_width
    h = r.TH1F('h', 'h', nbins, xmin, xmax)
    for v in values:
        h.Fill(v/gap)
    c = r.TCanvas("c", "c", 50, 50, 600, 600)
    c.SetGrid()
    h.Draw()
    h.Fit("landau")
    h.SetTitle("")
    h.GetXaxis().SetTitle("dN/dx [electrons/mm]")
    r.gStyle.SetOptStat("e")
    r.gStyle.SetOptFit(1101)
    stats1 = h.GetListOfFunctions().FindObject("stats")
    stats1.SetX1NDC(.6)
    stats1.SetX2NDC(.9)
    stats1.SetY1NDC(.6)
    stats1.SetY2NDC(.9)
    stats1.Draw()
    c.Update()
        
    raw_input("Press ENTER to stop the script")

