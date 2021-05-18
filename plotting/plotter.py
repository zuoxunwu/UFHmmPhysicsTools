#!/usr/bin/env python
from importlib import import_module
import os
import sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

def prefix_match(key, prefixes):
    prefix_list = prefixes.split(",")
    for prefix in prefix_list:
        prefix = prefix.replace(" ", "")
        prefix_tuple = tuple(prefix)
        if key.startswith(prefix):
            return prefix
    return ""

if __name__ == "__main__":
    ROOT.gROOT.SetBatch(ROOT.kTRUE)
    from optparse import OptionParser
    parser = OptionParser(usage="%prog [options] outputDir plotDirectory inputFiles")

    parser.add_option("--m", "--match", dest="match",
                      type="string", default="none", help="Method of Plot Matching")

    parser.add_option("--pfs", "--prefixes", dest="plot_prefixes",
                      type="string", default="", help="Plot Name Prefixes for Matching")

    (options, args) = parser.parse_args()
    if(len(args) < 3):
        raise Exception("Please add an Output Directory, Root Directory of Plots, and Input Files to your command line call.")
   
    inputFiles = args[2:]

    print(args[0], args[1], inputFiles)

    matched_plots = {}
    root_plots = []
    for f in inputFiles:
        root_file = ROOT.TFile.Open(f, "READ")
        root_dir = root_file.GetDirectory(args[1])
        root_keys = root_dir.GetListOfKeys()
	for key in root_keys:
            k = key.GetTitle()
            plot = root_dir.Get(key.GetTitle())
            if(not plot):
                continue
            plot.SetDirectory(0)
            match_key = ""
            if(options.match == "name-bet-files"):
                match_key = k
            if(options.match == "name-in-files"):
                match_key = f+prefix_match(k, options.plot_prefixes)
            if(options.match == "name-bet-in-files" or options.match is "name-in-bet-files"):
                match_key = prefix_match(k, options.plot_prefixes)

            if(matched_plots.has_key(match_key)):
                matched_plots[match_key].append(plot)
            else:
                matched_plots[match_key] = [plot]
            root_plots.append(plot)
        root_file.Close()

    print(matched_plots)

    canv2 = ROOT.TCanvas("overlay","Stack canvas",400,400)
    try:
        os.mkdir("."+args[0])
        open("."+args[0] + "/plots.pdf", 'a').close()
    except:
        open("."+args[0] + "/plots.pdf", 'a').close()
    canv2.Print( "."+args[0] + "/plots.pdf" +"[")
    for k in matched_plots.keys():
        line_color_index = 1
        stack = ROOT.THStack("stack","stack")
        legend = ROOT.TLegend (0.7 ,0.6 ,0.85 ,0.75)
        for plot in matched_plots[k]:
            plot.SetLineColor(line_color_index)
            line_color_index = line_color_index + 1
            if(line_color_index in [10, 5, 16,17,18,19,41]):
                line_color_index = line_color_index + 1;
            stack.Add(plot)
            legend.AddEntry (plot,k + " " + plot.GetTitle())
        stack.Draw("nostack")
        legend.SetLineWidth (0)
        legend.Draw ("same")
        canv2.Print("."+args[0] + "/plots.pdf")

    canv2.Print("."+args[0] + "/plots.pdf" +"]")

    print(root_plots)
    print(matched_plots)
    print(options, args);
