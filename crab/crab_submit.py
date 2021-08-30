#!/usr/bin/env python
import random
import os
import PhysicsTools.UFHmmPhysicsTools.helpers.samples as samples


if __name__ == "__main__":

    from optparse import OptionParser
    parser = OptionParser(usage="%prog datasets")
    (options, args) = parser.parse_args()
    for dataset in args:
        print str(dataset)
        sample = samples.getSample(str(dataset))
        name = sample.name
        DAS_dataset = sample.DAS
        module = sample.module;
        outputFiles = sample.outputFiles;
        command = "crab submit PhysicsTools/UFHmmPhysicsTools/crab/crab_cfg.py "
        command = command + "General.requestName=\""+name+"_Nano" + str(int(random.random()*1000)) + "\" "
        command = command + "Data.inputDataset=\"" + DAS_dataset + "\" ";
        command = command + "JobType.scriptArgs=\"['dataset=" + name + "', 'module=" + module + "']\" "
        command = command + "JobType.outputFiles=\"['" + outputFiles + "']\""
        output = os.system(command)
        print output

   
