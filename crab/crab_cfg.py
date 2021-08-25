from WMCore.Configuration import Configuration
from CRABClient.UserUtilities import config, getUsernameFromSiteDB

config = Configuration()

config.section_("General")
config.General.requestName = 'H2XX_Nano'
config.General.transferLogs = True

config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'pset.py'
config.JobType.scriptExe = 'crab_script.sh'
# hadd nano will not be needed once nano tools are in cmssw
config.JobType.inputFiles = ['crab_script.py']
config.JobType.scriptArgs = ['dataset=ggH', 'modules=analyzers.hmmAnalyzer']
config.JobType.sendPythonFolder = True

config.section_("Data")
config.Data.inputDataset = '/DYJetsToLL_1J_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIFall17NanoAOD-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/NANOAODSIM'
#config.Data.inputDBS = 'phys03'
config.Data.inputDBS = 'global'
config.Data.splitting = 'FileBased'
#config.Data.splitting = 'EventAwareLumiBased'
config.Data.unitsPerJob = 2
config.Data.totalUnits = 10
config.Data.outLFNDirBase = '/store/user/%s/NanoPost' % (
    getUsernameFromSiteDB())
config.Data.publication = False
config.Data.outputDatasetTag = 'H2XXPost'
config.section_("Site")
config.Site.storageSite = "T2_CH_CERN"

#config.Site.storageSite = "T2_CH_CERN"
# config.section_("User")
#config.User.voGroup = 'dcms'
