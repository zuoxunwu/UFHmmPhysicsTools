from WMCore.Configuration import Configuration
from CRABClient.UserUtilities import config, getUsername

config = config()

config.section_("General")
config.General.requestName = 'H2XX_Nano'
config.General.transferLogs = True
config.General.transferOutputs = True #Not really needed, default is True

config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'PhysicsTools/UFHmmPhysicsTools/crab/PSet.py'
config.JobType.scriptExe = 'PhysicsTools/UFHmmPhysicsTools/crab/crab_script.sh'
# hadd nano will not be needed once nano tools are in cmssw
config.JobType.inputFiles = ['PhysicsTools/UFHmmPhysicsTools/crab/crab_script.py', 'PhysicsTools/NanoAODTools/scripts/haddnano.py']
# Specify this output name only once, so it is not lost in CRAB.
config.JobType.outputFiles = ['hist_out.root']
config.JobType.scriptArgs = ['dataset=ggH', 'modules=analyzers.hmmAnalyzer']
config.JobType.sendPythonFolder = True

config.section_("Data")
config.Data.inputDataset = '/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM'
config.Data.inputDBS = 'global'
#Best not to use Automatic splitting. More details in Crab_README - XWZ Sep 10 2021
#config.Data.splitting = 'Automatic'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 2
config.Data.totalUnits = 10

#getUsernameFromSiteDB() is precedented by getUsername(). See https://github.com/dmwm/CRABClient/blob/6c34a951989a037a9493d81afea0dbe6f36fbf4e/src/python/CRABClient/UserUtilities.py#L31  
config.Data.outLFNDirBase = '/store/user/%s/H2XXNanoPost' % (getUsername())  
config.Data.publication = False
config.Data.outputDatasetTag = 'H2XXPost'

config.section_("Site")
config.Site.storageSite = "T2_CH_CERN"
#Need to find a stoarge site that you have permission to write to!
