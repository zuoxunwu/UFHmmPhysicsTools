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

        print "initiating branches"
        self.out.branch('nmuons', 'I')
        self.out.branch('muon_pass', 'I', lenVar = 'nmuons')
        self.out.branch('muon_charge', 'I', lenVar = 'nmuons')
        self.out.branch('muon_pt_gen', 'F', lenVar = 'nmuons')
        self.out.branch('muon_eta', 'F', lenVar = 'nmuons')
        self.out.branch('muon_phi', 'F', lenVar = 'nmuons')
        self.out.branch('muon_d0bs_micron', 'F', lenVar = 'nmuons')
        print "initiated branches"

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        muons = Collection(event, "Muon")
        genPart = Collection(event, "GenPart")

        # trigger and event selection
        eventSel = EventSelector(_year = 2018, _trigger_name = "SingleMu",
                                 _mu_trig_pt_min = 26, _OS_muPair = True, _muPair_mass_min = 60) 
        if not eventSel.evalEvent(event):
            return False

        muSel = MuonSelector(_year = 2018, _id_name = "medium", _iso_name = "PFIsoLoose",
                             _pt_corr = "Roch", _min_pt = 20, _max_eta = 2.4,
                             _max_d0PV = 0.05, _max_dzPV = 0.1, _min_lepMVA = -1)

        mu_pass    = []
        mu_charge  = []
        mu_eta     = []
        mu_phi     = []
        mu_d0      = []
        mu_pt_gen  = []

        for mu in muons:
            if muSel.evalMuon(mu): mu_pass.append(1)
            else:                  mu_pass.append(0)
            mu_charge.append(mu.charge)
            mu_eta   .append(mu.eta)
            mu_phi   .append(mu.phi)
            mu_d0    .append(mu.dxybs * 1e4)
            pt_gen = 0
            if mu.genPartFlav == 1:  pt_gen = genPart[mu.genPartIdx].pt  #check matching criteria in nanoAOD -- XWZ 2021.07.27
            mu_pt_gen.append(pt_gen)

        self.out.fillBranch('muon_pass', mu_pass)
        self.out.fillBranch('muon_charge', mu_charge)
        self.out.fillBranch('muon_eta', mu_eta)
        self.out.fillBranch('muon_phi', mu_phi)
        self.out.fillBranch('muon_d0bs_micron', mu_d0)
        self.out.fillBranch('muon_pt_gen', mu_pt_gen)
        #  Do not write line: self.out.fill()
        #  otherwise it fills the same event twice -- XWZ 2021.07.27

        return True


# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed
slimTree = lambda: slimTreeProducer()

