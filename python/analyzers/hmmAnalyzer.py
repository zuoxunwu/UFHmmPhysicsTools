
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True


class hmmAnalyzer(Module):
    def __init__(self):
        self.writeHistFile = True
        pass

    def beginJob(self, histFile=None, histDirName=None):
        Module.beginJob(self, histFile, histDirName)

        self.h_nMu = ROOT.TH1F('nMuons', 'nMuons', 10, 0, 10)
        self.h_dimu_mass = ROOT.TH1F('dimu_mass', 'dimu_mass', 200, 0, 200)
        self.addObject(self.h_nMu)
        self.addObject(self.h_dimu_mass)

        pass

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        muons = Collection(event, "Muon")
        self.h_nMu.Fill(len(muons))
        nMu = 0
        for mu in muons:
            if mu.p4().Pt() > 25:
                nMu += 1

        if nMu == 2:
            if muons[0].charge*muons[1].charge == -1:
                dimu = muons[0].p4() + muons[1].p4()
                self.h_dimu_mass.Fill(dimu.M())



        return True


# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed
#hmmAnalyzer = lambda: hmmAnalyzer()

