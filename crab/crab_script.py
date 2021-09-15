#!/usr/bin/env python
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles, runsAndLumis
from importlib import import_module
import os
import sys
import ROOT
import json
ROOT.PyConfig.IgnoreCommandLineOptions = True

if __name__ == "__main__":
    import argparse
    print sys.argv

    parser = argparse.ArgumentParser()
    parser.add_argument("jobID", help = "dummy arg to take jobID. Not used in this script.")
    parser.add_argument("-m", "--modules", nargs='*', dest="modules", default  = [],
                 help = "modules to run")
    parser.add_argument("-o", "--outfile", dest="outfile", default  = None,
                 help = "histFileName")

    args = parser.parse_args()
    if not args.modules:
        print 'No module to run. Exiting.'
        sys.exit()    

    modules = []
    for names in args.modules:
        mod = "PhysicsTools.UFHmmPhysicsTools." + names.rsplit('.', 1)[0]
        name = names.rsplit('.', 1)[1]
        import_module(mod)
        obj = sys.modules[mod]
        mods = dir(obj)        
        if name in mods:
            print("Loading %s from %s " % (name, mod))
            if type(getattr(obj, name)) == list: # Not sure when it shall be a list. To ask John - XWZ Sep 15 2021
                for m in getattr(obj, name):
                    modules.append(m())
            else:
                    modules.append(getattr(obj, name)())

    p = PostProcessor(".", inputFiles(),
                      cut="0==0",
                      modules=modules,
                      provenance=True,
                      fwkJobReport=True, # This option is essential for the NanoAOD Tool to make a FrameworkJobReport.xml
                      histFileName=args.outfile,
                      histDirName='plots',
#                      noOut=noOut,
                      jsonInput=runsAndLumis() # Will need json for lumi when running on data. Json should be given in PSet.py. If no json is found it returns None, which is the default value of this arg.
                      )
    p.run()
