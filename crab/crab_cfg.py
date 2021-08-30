from WMCore.Configuration import Configuration
from CRABClient.UserUtilities import config

config = Configuration()

config.section_("General")
config.General.requestName = 'H2XX_Nano'
config.General.transferLogs = True

config.section_("JobType")
config.JobType.pluginName = 'Analysis'
#config.User.voGroup = 'dcms'
config.JobType.psetName = 'PhysicsTools/UFHmmPhysicsTools/crab/PSet.py'
config.JobType.scriptExe = 'PhysicsTools/UFHmmPhysicsTools/crab/crab_script.sh'
# hadd nano will not be needed once nano tools are in cmssw
config.JobType.inputFiles = ['PhysicsTools/UFHmmPhysicsTools/crab/crab_script.py']
config.JobType.scriptArgs = ['dataset=ggH', 'modules=analyzers.hmmAnalyzer']
config.JobType.sendPythonFolder = True

config.section_("Data")
config.Data.inputDataset = '/DYJetsToLL_1J_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIFall17NanoAOD-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/NANOAODSIM'
config.Data.inputDBS = 'global'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 2
config.Data.totalUnits = 10
#Edit below with a path you have write permissions to on the storage site!
config.Data.outLFNDirBase = '/store/user/%s/H2XXNanoPost' % ("USER")
config.Data.publication = False
config.Data.outputDatasetTag = 'H2XXPost'
config.section_("Site")
config.Site.storageSite = "T3_US_FNALLPC"
#Need to find a stoarge site that you have permission to write to!
