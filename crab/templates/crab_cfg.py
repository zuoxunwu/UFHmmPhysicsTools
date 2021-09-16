from WMCore.Configuration import Configuration
from CRABClient.UserUtilities import config, getUsername
import os

config = config()

config.section_("General")
#config.General.requestName = 'H2XX_Nano'
config.General.requestName = 'STR'
config.General.workArea = 'CRAB_logs'
config.General.transferLogs = True
config.General.transferOutputs = True #Not really needed, default is True

config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = '%s/src/PhysicsTools/UFHmmPhysicsTools/crab/templates/PSet.py'%os.environ['CMSSW_BASE']
config.JobType.scriptExe = '%s/src/PhysicsTools/UFHmmPhysicsTools/crab/crab_script.sh'%os.environ['CMSSW_BASE']
# hadd nano will not be needed once nano tools are in cmssw
config.JobType.inputFiles = ['%s/src/PhysicsTools/UFHmmPhysicsTools/crab/crab_script.py'%os.environ['CMSSW_BASE'], '%s/src/PhysicsTools/NanoAODTools/scripts/haddnano.py'%os.environ['CMSSW_BASE']]
# Specify this output name only once, so it is not lost in CRAB.
#config.JobType.scriptArgs = ['dataset=ggH', 'modules=analyzers.hmmAnalyzer']
config.JobType.scriptArgs = []
config.JobType.outputFiles = []
config.JobType.sendPythonFolder = True

config.section_("Data")
#config.Data.inputDataset = '/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM'
config.Data.inputDataset = 'STR'
config.Data.inputDBS = 'DBS'
# config.Data.lumiMask = 'STR'
#config.Data.splitting = 'Automatic'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 2
#config.Data.totalUnits = 10 # total files to process (for FileBased splitting). Should not enable for large jobs.

#getUsernameFromSiteDB() is precedented by getUsername(). See https://github.com/dmwm/CRABClient/blob/6c34a951989a037a9493d81afea0dbe6f36fbf4e/src/python/CRABClient/UserUtilities.py#L31  
#config.Data.outLFNDirBase = '/store/user/%s/H2XXNanoPost' % (getUsername())  
config.Data.outLFNDirBase = 'STR'
config.Data.publication = False
config.Data.outputDatasetTag = 'STR'

config.section_("Site")
config.Site.storageSite = 'T2_CH_CERN'
#Need to find a stoarge site that you have permission to write to!
