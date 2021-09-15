#!/usr/bin/env python
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
#from PhysicsTools.UFHmmPhysicsTools.helpers.crabHelper import inputFiles, runsAndLumis
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles, runsAndLumis
from importlib import import_module
import os
import sys
import ROOT
import json
ROOT.PyConfig.IgnoreCommandLineOptions = True

if __name__ == "__main__":
    from optparse import OptionParser
    print sys.argv

    jobNumber = sys.argv[1]
    dataset = sys.argv[2]
    module_names = [sys.argv[3]]
    if(len(sys.argv[3].split("=")) > 1):
        module_names = [sys.argv[3].split("=")[1]]

    print jobNumber, dataset, module_names

    outputDir = "."
    cut = "0==0"
    histFileName = "hist_out.root"
    histDirName = "plots"
    noOut = True

    modules = []
    for names in module_names:
        mod = "PhysicsTools.UFHmmPhysicsTools." + names
        import_module(mod)
        obj = sys.modules[mod]
        name = names.split(".")[1]
        mods = dir(obj)
        if name in mods:
            print("Loading %s from %s " % (name, mod))
            if type(getattr(obj, name)) == list:
                for mod in getattr(obj, name):
                    modules.append(mod())
            else:
                    modules.append(getattr(obj, name)())

    p = PostProcessor(outputDir, inputFiles(),
                      cut=cut,
                      modules=modules,
                      provenance=True,
                      fwkJobReport=True, # This option is essential for the NanoAOD Tool to make a FrameworkJobReport.xml
                      histFileName=histFileName,
                      histDirName=histDirName,
#                      noOut=noOut,
                      jsonInput=runsAndLumis() # Will need json for lumi when running on data. Json should be given in PSet.py. If no json is found it returns None, which is the default value of this arg.
                      )
    p.run()
