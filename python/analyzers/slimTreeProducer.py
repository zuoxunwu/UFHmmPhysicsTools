import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.framework.output import OutputTree

from PhysicsTools.UFHmmPhysicsTools.helpers.eventSelector import EventSelector
from PhysicsTools.UFHmmPhysicsTools.helpers.objectSelector import MuonSelector, ElectronSelector

class slimTreeProducer(Module):
    def __init__(self):
        self.writeHistFile = True
        # declare eventsel, rochcorr here
        

    def beginJob(self, histFile=None, histDirName=None):
        pass

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree

        self.out.branch('muon_charge', 'I')
        self.out.branch('muon_pt_gen', 'F')
        self.out.branch('muon_pt_Roch', 'F')
        self.out.branch('muon_eta', 'F')
        self.out.branch('muon_phi', 'F')
        self.out.branch('muon_d0bs_micron', 'F')

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        muons = Collection(event, "Muon")
        genPart = Collection(event, "GenPart")

        print int(event.event)
        # trigger and event selection
        eventSel = EventSelector(_year = 2018, _trigger_name = "SingleMu",
                                 _mu_trig_pt_min = 26, _OS_muPair = True, _muPair_mass_min = 60) 
        if not eventSel.evalEvent(event):
            print "not save"
            return False

        muSel = MuonSelector(_year = 2018, _id_name = "medium", _iso_name = "PFIsoLoose",
                             _pt_corr = "Roch", _min_pt = 20, _max_eta = 2.4,
                             _max_d0PV = 0.05, _max_dzPV = 0.1, _min_lepMVA = -1)
        for mu in muons:
          if not muSel.evalMuon(mu): continue
          self.out.fillBranch('muon_charge', mu.charge)
          self.out.fillBranch('muon_eta', mu.eta)
          self.out.fillBranch('muon_phi', mu.phi)
          self.out.fillBranch('muon_d0bs_micron', mu.dxybs * 1e4)
          self.out.fillBranch('muon_pt_Roch', mu.pt) # to be updated with Roch -- XWZ 2021.07.26
          pt_gen = 0
          if mu.genPartFlav == 1: # check matching criteria in nanoAOD -- XWZ 2021.07.26
              pt_gen = genPart[mu.genPartIdx].pt
          self.out.fillBranch('muon_pt_gen', pt_gen)

        return True


# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed
slimTree = lambda: slimTreeProducer()

