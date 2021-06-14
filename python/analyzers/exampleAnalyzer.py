from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True


class exampleAnalyzer(Module):
    def __init__(self):
        self.writeHistFile = True
        pass

    def beginJob(self, histFile=None, histDirName=None):
        Module.beginJob(self, histFile, histDirName)
        print("Starting Example Analysis Module")

        #Creating histogram TH1F
        self.nMuon = ROOT.TH1F('Plot Name', 'Plot Title', 10, -0.5, 9.5)
        #Adding histogram as an Object to be saved later
        self.addObject(self.nMuon)

        print("Finished Making Histograms")
        pass

    def exampleFunction(self, variables):
        """ An Example of a function that references self, this can be called by self.exampleFunction(variables) """
        print("Example Function: ", variables)
        pass

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""

        #Collects all the muons in the event - As long as the Muons collection is is kept in keep_and_drop.txt
        muons = Collection(event, "Muon")

        #Fill Histograms
        self.nMuon.Fill(len(muons))

        #This is where you would add selections, fill other histograms, or call functions that will run each event.

        return True
