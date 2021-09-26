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
    parser = OptionParser(usage="%prog [options] outputDir inputFiles")
    parser.add_option("-s", "--postfix", dest="postfix", type="string", default=None,
                      help="Postfix which will be appended to the file name (default: _Friend for friends, _Skim for skims)")
    parser.add_option("-J", "--json", dest="json", type="string",
                      default=None, help="Select events using this JSON file")
    parser.add_option("-c", "--cut", dest="cut", type="string",
                      default="0==0", help="Cut string")
    parser.add_option("--hdir", "--hist-dir-name", dest="histDirName",
                      type="string", default="plots", help="Output directory for Histograms")
    parser.add_option("--hfile", "--hist-file-name", dest="histFileName",
                      type="string", default="hist_out.root", help="Histogram output file")
    parser.add_option("-b", "--branch-selection", dest="branchsel",
                      type="string", default=None, help="Branch selection")
    parser.add_option("--bi", "--branch-selection-input", dest="branchsel_in",
                      type="string", default="PhysicsTools/UFHmmPhysicsTools/scripts/keep_and_drop_input.txt", help="Branch selection input")
    parser.add_option("--bo", "--branch-selection-output", dest="branchsel_out",
                      type="string", default="PhysicsTools/UFHmmPhysicsTools/scripts/keep_and_drop_output.txt", help="Branch selection output")
    parser.add_option("--friend", dest="friend", action="store_true", default=False,
                      help="Produce friend trees in output (current default is to produce full trees)")
    parser.add_option("--full", dest="friend", action="store_false", default=False,
                      help="Produce full trees in output (this is the current default)")
    parser.add_option("--noout", dest="noOut", action="store_true",
                      default=False, help="Do not produce output, just run modules")
    parser.add_option("-P", "--prefetch", dest="prefetch", action="store_true", default=False,
                      help="Prefetch input files locally instead of accessing them via xrootd")
    parser.add_option("--long-term-cache", dest="longTermCache", action="store_true", default=False,
                      help="Keep prefetched files across runs instead of deleting them at the end")
    parser.add_option("-N", "--max-entries", dest="maxEntries", type="long", default=None,
                      help="Maximum number of entries to process from any single given input tree")
    parser.add_option("--first-entry", dest="firstEntry", type="long", default=0,
                      help="First entry to process in the three (to be used together with --max-entries)")
    parser.add_option("--justcount", dest="justcount", default=False,
                      action="store_true", help="Just report the number of selected events")
    parser.add_option("-I", "--import", dest="imports", type="string", default=[], action="append",
                      nargs=2, help="Import modules (python package, comma-separated list of ")
    parser.add_option("--ds", "--dataset", dest="dataset", type="string", default=None,
                      help="Dataset to fetch files from (check dataset_config.txt)")
    parser.add_option("-z", "--compression", dest="compression", type="string",
                      default=("LZMA:9"), help="Compression: none, or (algo):(level) ")

    (options, args) = parser.parse_args()
    if(options.dataset):
        config_file = open("PhysicsTools/UFHmmPhysicsTools/scripts/dataset_config_xunwu.txt", "r")
        config_file_contents = config_file.read()
        config = json.loads(config_file_contents)
        # check internet host
        import socket
        host = socket.getfqdn()
        prefix = 'root://cmsxrootd.fnal.gov//'
        if 'cern.ch' in host:
          prefix = 'root://xrootd-cms.infn.it//'
        for f in config[options.dataset]["files"]:
#            args.append(config[options.dataset]["outputDir"])  # Small bug, see L79, outputs will be taken as inputs. Comment out for now. To be discussed: this functionality probably not needed anyway. - XWZ Sep 07 2021
            args.append(prefix + f)
        if(len(args)==0):
            args.append("True")

    print(args)

    if options.friend:
        if options.cut or options.json:
            raise RuntimeError(
                "Can't apply JSON or cut selection when producing friends")

    if len(args) < 2:
        parser.print_help()
        sys.exit(1)
    outdir = args[0]
    args = args[1:]

    if(options.histFileName):
        if(not options.histFileName.split("/")[0] is outdir):
            options.histFileName = outdir + "/" + options.histFileName
        if(not options.histFileName.split(".")[len(options.histFileName.split("."))-1] is "root"):
            options.histFileName = options.histFileName + ".root"

    modules = []
    for mod, names in options.imports:
        import_module(mod)
        obj = sys.modules[mod]
        selnames = names.split(",")
        mods = dir(obj)
        for name in selnames:
            if name in mods:
                print("Loading %s from %s " % (name, mod))
                if type(getattr(obj, name)) == list:
                    for mod in getattr(obj, name):
                        modules.append(mod())
                else:
                    modules.append(getattr(obj, name)())
    if options.noOut:
        if len(modules) == 0:
            raise RuntimeError(
                "Running with --noout and no modules does nothing!")
    if options.branchsel != None:
        options.branchsel_in = options.branchsel
        options.branchsel_out = options.branchsel
    p = PostProcessor(outdir, args,
                      cut=options.cut,
                      branchsel=options.branchsel_in,
                      modules=modules,
                      histFileName=options.histFileName,
                      histDirName=options.histDirName,
                      compression=options.compression,
                      friend=options.friend,
                      postfix=options.postfix,
                      jsonInput=options.json,
                      noOut=options.noOut,
                      justcount=options.justcount,
                      prefetch=options.prefetch,
                      longTermCache=options.longTermCache,
                      maxEntries=options.maxEntries,
                      firstEntry=options.firstEntry,
                      outputbranchsel=options.branchsel_out)
    p.run()


