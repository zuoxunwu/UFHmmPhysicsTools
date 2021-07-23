
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True


class slimTreeProducer(Module):
    def __init__(self):
        self.writeHistFile = True
        # declare eventsel, rochcorr here
        pass

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


    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        muons = Collection(event, "Muon")
        trigObj = Collection(event, "TrigObj")
        genPart = Collection(event, "GenPart")

        for mu in muons:
          self.out.fillBranch('muon_charge', mu.charge)
          self.out.fillBranch('muon_eta', mu.eta)
          self.out.fillBranch('muon_phi', mu.phi)
          self.out.fillBranch('muon_d0bs_micron', mu.dxybs * 1e4)
          self.out.fillBranch('', mu.)
          self.out.fillBranch('', mu.)
          self.out.fill()

        return True


# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed
#slimTreeProducer = lambda: slimTreeProducer()

