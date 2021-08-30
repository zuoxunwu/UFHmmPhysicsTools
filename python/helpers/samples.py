class sample:
    def __init__(self, name='', DAS='', inputDBS='global', nEvt=0, files=[], GT='94X_mc2017_realistic_v12',
                 JEC='Fall17_17Nov2017_V4_MC', runs=[], JSON=[], isData=False, module='', outputFiles='hist_out.root'):
        self.name   = name       ## User-assigned dataset name
        self.DAS    = DAS        ## DAS directory
        self.inputDBS = inputDBS  # to be used in crab in case of private production. config.Data.inputDBS = 'global' or 'phys03'
        self.nEvt   = nEvt       ## Number of events in dataset
        self.files  = files      ## Local files for testing
        self.GT     = GT         ## Global tag
        self.JEC    = JEC        ## Jet energy corrections global tag
        self.runs   = runs       ## Run range
        self.JSON   = JSON       ## JSON file
        self.isData = isData     ## Is data
        self.module = module   ## Input Modules (Analyzers & Producers)
        self.outputFiles = outputFiles #To collect specific output files from modules

# =======================================================================================================
# ------------------------------- DATA ------------------------------------------------------------------
# =======================================================================================================

ggH = sample( name = 'ggH',
              DAS = '/GluGluHToMuMu_M125_TuneCP5_PSweights_13TeV_amcatnloFXFX_pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM',
              isData = False,
              module = "analyzers.hmmAnalyzer",
              outputFiles = "hist_out.root")


def getSample(sample):
    if sample == "ggH":
        return ggH
