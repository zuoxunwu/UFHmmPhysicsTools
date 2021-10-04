#! /usr/bin/env python

# This script is modified from the script in UF Ntupliser https://github.com/UFLX2MuMu/Ntupliser/blob/master_2017_94X/DiMuons/crab/make_crab_script.py
import sys, os
sys.path.append(os.getcwd())

import PhysicsTools.UFHmmPhysicsTools.helpers.samples as samples

import time 
import subprocess
# from https://stackoverflow.com/questions/15753701/argparse-option-for-passing-a-list-as-option
import argparse # for options parsing

# Default list for test runs or special runs
SAMPS = [samples.DY_17_amc, samples.DY_17_mg, samples.DY_17_mg_ext1]
# Default list for modules to tun. The last name is the module instance name, it can be different from the module class name. 
#MODS  =    ['analyzers.hmmAnalyzer.hmmAnalyzer'] 
OUTFILE = 'hist_out.root'

MODS = ['producers.slimTreeProducer.slimTree', 'producers.roccorProducer.roccor2018V5']

parser = argparse.ArgumentParser(description="Pass arguments")
parser.add_argument("-s", "--samples", nargs='*', dest='samps', default  = SAMPS,
                 help = "List of samples")
parser.add_argument("-m", "--modules", nargs='*', dest="mods", default = MODS,
                 help = "List of modules to run")                 
parser.add_argument("-o", "--outfile", dest='outfile', default = OUTFILE,
                 help = "Output file name produces by modules") #nano postprocessor only supports one file name
parser.add_argument("-y", "--year", dest="year", default = '2018',
                 help = "Data taking era of samples")
args = parser.parse_args()


## Read the code tag for the production.
def get_prod_version():
  try: ## try with an annotated tag
    print('Getting annotated tag...')
    return subprocess.check_output(["git","describe"]).strip()
  except: 
    print('No annotated tag. Trying with lightweighted tag.')
    pass 
  try: ## otherwise try with a lightweighted tag
    print('Getting lightweighted tag...')
    return subprocess.check_output(["git","describe","--tag"]).strip()
  except:  
    print('No lightweighted tag. Using latest committ.')
    pass  
  ## otherwise pick the latest commit
  return subprocess.check_output(["git","rev-parse","--short"]).strip()

prod_version = get_prod_version()
print("Production using code version {0} starting" .format(prod_version))

homedir = os.environ['HOME']
username = homedir.split('/')[-1]
# Try to avoid having decimal point '.' in the LFN directory - XWZ Sep 16 2021
# Decimal point '.' can only appear in the first-tier or fifth tier subdictories under /user
# CRAB recognizes regular expression /store/(temp/)*(user|group)/(([a-zA-Z0-9\.]+)|([a-zA-Z0-9\-_]+))/([a-zA-Z0-9\-_]+)/([a-zA-Z0-9\-_]+)/([a-zA-Z0-9\-_]+)/([a-zA-Z0-9\-\._]+)
output_dir = '/store/user/{0}/H2XXNanoPost/{1}/{2}'.format(username, args.year, prod_version.replace('.','p')) 
print("Production output dir {0}".format(output_dir))

samps = []
if args.samps != SAMPS:
    for sample_to_add in args.samps:
#        samps.append(samples_dictionary[sample_to_add]) # This is a better way. To be implemented
        samps.append(samples.getSample(sample_to_add))
else:
    samps = args.samps
   
## Get the samples you want to make a crab config file for 
version_str = '_prod_{0}_{1}'.format(args.year, prod_version.replace('.','p'))
print("Sample list: {0}".format(samps))

crab_prod_dir = 'CRAB_%s-%s'%(time.strftime('%Y_%m_%d_%H_%M'),prod_version)
crab_configs_dir = crab_prod_dir+'/configs'
print('crab production directory = ' + crab_prod_dir)
os.mkdir(crab_prod_dir)
os.mkdir(crab_configs_dir)

cms_dir = os.environ['CMSSW_BASE']
print cms_dir

for samp in samps:
    print '\nCreating crab config for %s' % samp.name

    ## Open the crab submission template to change
    in_file = open('crab/templates/crab_cfg.py', 'r')
    out_file = open('%s/%s.py' %(crab_configs_dir,samp.name), 'w')
    
    # Read in the template and replace the parameters to make a
    # crab submission file that uses the above CMSSW analyzer
    for line in in_file:
        if 'requestName' in line:
            line = line.replace("= 'STR'", "= '%s_%s%s'" % (samp.name, time.strftime('%Y_%m_%d_%H_%M'), version_str) ) 

        if 'scriptArgs' in line:
            line = line.replace("= []", "= ['modules=%s', 'outfile=%s']" %(','.join(args.mods), args.outfile)) 
 
        if 'outputFiles' in line:
            line = line.replace("= []", "= ['%s']" %(args.outfile))

        if 'inputDataset' in line:
            line = line.replace("= 'STR'", "= '%s'" % samp.DAS)

        if samp.isData and 'lumiMask' in line: 
            line = line.replace('# config.Data.lumiMask', 'config.Data.lumiMask')
            line = line.replace("= 'STR'", "= '%s'" % samp.JSON)

        # With Automatic splitting, the output files of the first few jobs are not transfered.
        # Use 'FileBased' splitting for MC. For data 'LumiBased' is recommended. 
        # But NanoAOD files are already merged comparing to their MiniAOD parents. So maybe 'FileBased' is also good for data. To be tested. - XWZ Sep 15 2021

#        if 'splitting' in line:
#            line = line.replace('FileBased', 'Automatic')

        if 'unitsPerJob' in line: # Number of files per job for MC, or lumisections per job for data.
            if samp.isData:
                line = line.replace('unitsPerJob = 2', 'unitsPerJob = 2')
            else:
                line = line.replace('unitsPerJob = 2', 'unitsPerJob = 2')

        if 'inputDBS' in line:
            line = line.replace("= 'DBS'", "= '%s'"  % samp.inputDBS)

        if 'outputDatasetTag' in line:
            line = line.replace("= 'STR'", "= '%s'" % samp.name)

        if 'outLFNDirBase' in line:
            line = line.replace("= 'STR'", "= '{0}/'".format(output_dir))

        out_file.write(line)
    
    print '  * Wrote %s' % out_file.name
    out_file.close()
    in_file.close()


print '\nCreating submit_all.sh and check_all.sh scripts'

out_file = open('%s/submit_all.sh' % crab_prod_dir, 'w')
out_file.write('#!/bin/bash\n')
out_file.write('\n')
#out_file.write('source /cvmfs/cms.cern.ch/crab3/crab.csh\n')
out_file.write('voms-proxy-init --voms cms --valid 168:00\n')
out_file.write('\n')
for samp in samps:
    out_file.write('crab submit -c %s/%s.py\n' % (crab_configs_dir, samp.name))
out_file.close()
os.chmod('%s/submit_all.sh' % crab_prod_dir, 0o744)

out_file = open('%s/check_all.sh' % crab_prod_dir, 'w')
out_file.write('#!/bin/bash\n')
out_file.write('\n')
# out_file.write('source /cvmfs/cms.cern.ch/crab3/crab.csh\n')
# out_file.write('voms-proxy-init --voms cms --valid 168:00\n')
out_file.write('\n')
for samp in samps:
    out_file.write('crab status -d CRAB_logs/crab_%s_%s%s\n' % (samp.name, time.strftime('%Y_%m_%d_%H_%M'), version_str) )
out_file.close()
os.chmod('%s/check_all.sh' % crab_prod_dir, 0o744)
