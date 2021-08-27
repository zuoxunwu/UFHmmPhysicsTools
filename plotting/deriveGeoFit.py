import os
import numpy as np

import ROOT

from CMS_style import setTDRStyle
from PhysicsTools.UFHmmPhysicsTools.helpers.utils import findFWHM


FILE_LOC = "/afs/cern.ch/work/x/xzuo/UF_NanoAODTool_10619p2/src/outputs" 
FILES = ['DYMG18UL2M.root']
YEAR  = '2018'
TREE  = 'Events'


def DrawCanv(out_file, graph):
    setTDRStyle()
    ROOT.gStyle.SetOptFit(0)
    ROOT.gStyle.SetLegendBorderSize(0)
    ROOT.gStyle.SetLegendFont(42)
    ROOT.gStyle.SetLegendTextSize(0.035) 
    ROOT.gStyle.SetErrorX(0.0)

    out_file.cd()

    graph_name = graph.GetName()
    canv = ROOT.TCanvas(graph_name, graph_name, 600, 600)
    canv.SetLeftMargin(0.15)
    canv.SetTopMargin(0.08)
    canv.cd()

    graph.GetXaxis().SetTitle("d0_{BS} * charge (\mu^{}m)")
    graph.GetXaxis().SetTitleSize(0.035)
    graph.GetXaxis().SetTitleOffset(1.2)
    graph.GetXaxis().SetLabelSize(0.03)
    graph.GetYaxis().SetTitle("(p_{T}^{Roch} - p_{T}^{gen})/(p_{T}^{gen})^{2}")
    graph.GetYaxis().SetTitleSize(0.035)
    graph.GetYaxis().SetTitleOffset(1.9)
    graph.GetYaxis().SetLabelSize(0.03)

    graph.SetMaximum(0.005)
    graph.SetMinimum(-0.003)
    graph.SetMarkerStyle(8)
    graph.SetMarkerSize(0.8)

    eta_min = graph_name.split('_')[1].replace('p', '.')
    eta_max = graph_name.split('_')[2].replace('p', '.')
    eta_label = eta_min + ' < |\eta| < ' + eta_max

    leg = ROOT.TLegend(0.2, 0.65, 0.7, 0.78)
    leg.SetHeader(eta_label, "C")
    leg_str = 'y = %.2e + (%.2e \pm %.1e) * d0' %(graph.GetFunction('line').GetParameter(1), graph.GetFunction('line').GetParameter(0), graph.GetFunction('line').GetParError(0))
    leg.AddEntry( graph.GetFunction('line'), leg_str)

    graph.Draw("APZ")
    leg.Draw("SAME")

    cms_latex = ROOT.TLatex()
    cms_latex.SetTextAlign(11)
    cms_latex.SetTextSize(0.025)
    cms_latex.DrawLatexNDC(0.2, 0.82, '#scale[2.0]{CMS #bf{#it{Preliminary}}}')
    cms_latex.DrawLatexNDC(0.8, 0.94,'#font[42]{#scale[1.5]{%sDY}}'%YEAR)
    

    canv.SaveAs('outputs/geofit/'+graph_name+'.pdf')


def PlotGeoFit(out_file, samp_files, tree_name):
    d0_bins = np.linspace(-100, 100, 20)
    eta_bins = np.array([0, 0.9, 1.7, 2.4])
    print d0_bins    
    hists = {}
    graphs = {}

    in_tree = ROOT.TChain(tree_name,"chain")
    for file_name in samp_files:
        in_tree.Add(file_name)
    out_file.cd()

    pt_str = "muon_charge * (muon_pt_Roch - muon_pt_gen) / muon_pt_gen^2"
    for ieta in range( len(eta_bins) - 1 ):
        eta_str = "(%.1f <= abs(muon_eta) && abs(muon_eta) < %.1f)" %(eta_bins[ieta], eta_bins[ieta+1])
        graph_name = ("eta_%.1f_%.1f"%(eta_bins[ieta], eta_bins[ieta+1])).replace('.', 'p')
        graphs[graph_name] = ROOT.TGraphAsymmErrors()
        graphs[graph_name].SetName(graph_name)
        for id0 in range( len(d0_bins) - 1 ):
            d0_str = "(%.0f < muon_d0bs_micron && muon_d0bs_micron < %.0f)"%(d0_bins[id0], d0_bins[id0+1])
            in_tree.Draw( "%s >> eta%d_d0%d(100, -0.005, 0.005)"%(pt_str, ieta+1, id0+1), "%s && %s"%(eta_str, d0_str) )

            hists["eta%d_d0%d"%(ieta+1, id0+1)] = ROOT.gDirectory.Get("eta%d_d0%d"%(ieta+1, id0+1))
            d0_center = (d0_bins[id0] + d0_bins[id0+1]) / 2 
            d0_err    = (d0_bins[id0+1] - d0_bins[id0]) / 2
            pt_center = hists["eta%d_d0%d"%(ieta+1, id0+1)].GetMean()
            lo_bin, hi_bin = findFWHM(hists["eta%d_d0%d"%(ieta+1, id0+1)]) 
            pt_lo_err = pt_center - hists["eta%d_d0%d"%(ieta+1, id0+1)].GetBinCenter(lo_bin)
            pt_hi_err = hists["eta%d_d0%d"%(ieta+1, id0+1)].GetBinCenter(hi_bin) - pt_center
            if pt_lo_err < 0 or pt_hi_err < 0:
                print "Weird case for eta bin %d, d0 bin %d" %(ieta, id0)
                print "pt_lo_err = %f, pt_hi_err = %f" %(pt_lo_err, pt_hi_err)
                pt_lo_err = 1
                pt_hi_err = 1           
 
            graphs[graph_name].SetPoint(id0, d0_center, pt_center)
            graphs[graph_name].SetPointError(id0, d0_err, d0_err, pt_lo_err, pt_hi_err)
            hists["eta%d_d0%d"%(ieta+1, id0+1)].Write()

        F_line = ROOT.TF1("line", "[0]*x+[1]", -100, 100)
        F_line.SetParNames("Slope", "Intercept")
        F_line.SetParameters( 1e-2, 0)

        for i in range(10):
            graphs[graph_name].Fit("line", "QR")
            F_line.SetParameters( F_line.GetParameter(0), F_line.GetParameter(1) )

        ROOT.gStyle.SetOptFit(0111)
        graphs[graph_name].GetFunction("line").SetLineColor(ROOT.kBlue)
        graphs[graph_name].GetFunction("line").SetLineWidth(2)
        graphs[graph_name].Write()
        DrawCanv(out_file, graphs[graph_name])

    print "GeoFit parameters derived."
    return 0


def main():
    samp_files = []
    for f in FILES:
        samp_files.append(FILE_LOC + '/' + f)
    if not os.path.exists('outputs/geofit'):
        os.makedirs('outputs/geofit')
    out_file = ROOT.TFile("outputs/geofit/GeoFitParams.root", "RECREATE")

    PlotGeoFit(out_file, samp_files, TREE)

if __name__ == '__main__':
    main()

