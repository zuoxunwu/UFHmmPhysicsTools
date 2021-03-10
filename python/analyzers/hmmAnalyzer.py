from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from importlib import import_module
import os
import sys
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
        # electrons = Collection(event, "Electron")
        muons = Collection(event, "Muon")
        # jets = Collection(event, "Jet")
        # eventSum = ROOT.TLorentzVector()
        # print "n muons: %d" % len(muons)
        self.h_nMu.Fill(len(muons))
        nMu = 0
        for mu in muons:
            if mu.p4().Pt() > 25:
                nMu += 1

        if nMu == 2:
            if muons[0].charge*muons[1].charge == -1:
                dimu = muons[0].p4() + muons[1].p4()
                self.h_dimu_mass.Fill(dimu.M())



        # self.out.fillBranch("EventMass", eventSum.M())
        return True


# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed

# hmmAnalyzerConstr = lambda: hmmAnalyzer()

# preselection = "Jet_pt[0] > 250"
files = ["root://cms-xrd-global.cern.ch//store/mc/RunIIAutumn18NanoAODv7/GluGluHToMuMu_M125_TuneCP5_PSweights_13TeV_amcatnloFXFX_pythia8/NANOAODSIM/Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/100000/4FA4D948-38F7-6A4C-BBD6-33FA5A37EEA9.root"]
p = PostProcessor(".", files, cut="0==0", branchsel="../../UFHmmPhysicsTools/analyzers/keep_and_drop_input.txt", modules=[
                  hmmAnalyzer()], noOut=True, histFileName="histOut.root", histDirName="plots", maxEntries=1000)
p.run()


