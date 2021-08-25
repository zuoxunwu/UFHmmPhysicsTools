#!/usr/bin/env python
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from importlib import import_module
import os
import sys
import ROOT
import json
ROOT.PyConfig.IgnoreCommandLineOptions = True

if __name__ == "__main__":
    from optparse import OptionParser
    parser = OptionParser(usage="%prog job_id dataset imports")

    args = parser.parse_args()

    outputDir = ""
    files = []
    cut = "0==0"
    histFileName = ""
    histDirName = ""
    noOut = True
    branchsel_in = "PhysicsTools/UFHmmPhysicsTools/scripts/keep_and_drop_input.txt"
    branchsel_out = "PhysicsTools/UFHmmPhysicsTools/scripts/keep_and_drop_output.txt"

    if(args[1]):
        config_file = open("PhysicsTools/UFHmmPhysicsTools/scripts/dataset_config.txt", "r")
        config_file_contents = config_file.read()
        config = json.loads(config_file_contents)
        # check internet host
        import socket
        host = socket.getfqdn()
        prefix = 'root://cmsxrootd.fnal.gov//'
        if 'cern.ch' in host:
          prefix = 'root://xrootd-cms.infn.it//'
        for f in config[args[1]]["files"]:
            outputDir = config[args[1]]["outputDir"]
            files.append(prefix + f)
            histFileName = config[args[1]]["histFileName"]
            histFileName = config[args[1]]["histDirName"]
        if(len(args)==0):
            args.append("True")

                "Can't apply JSON or cut selection when producing friends")

    if(histFileName):
        if(not histFileName.split("/")[0] is outdir):
            histFileName = outputDir + "/" + histFileName
        if(not histFileName.split(".")[len(histFileName.split("."))-1] is "root"):
            histFileName = histFileName + ".root"

    modules = []
    for names in args[2]:
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

    p = PostProcessor(outputDir, files,
                      cut=cut,
                      branchsel=branchsel_in,
                      modules=modules,
                      histFileName=histFileName,
                      histDirName=histDirName,
                      noOut=noOut,
                      outputbranchsel=branchsel_out)
    p.run()
