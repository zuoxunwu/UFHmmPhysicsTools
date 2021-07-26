import ROOT

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Event, Object, Collection

from PhysicsTools.UFHmmPhysicsTools.helpers.objectSelector import MuonSelector, ElectronSelector
from PhysicsTools.UFHmmPhysicsTools.helpers.triggerSelector import triggerSelector


class EventSelector:
    def __init__(self, _year = None, _trigger_name = "SingleMu", 
                 _mu_trig_pt_min = 26, _OS_muPair = True, _muPair_mass_min = 60):

        self.year = _year
        self.trigger_name    = _trigger_name
        self.mu_trig_pt_min  = _mu_trig_pt_min
        self.OS_muPair       = _OS_muPair
        self.muPair_mass_min = _muPair_mass_min


    def evalEvent(self, event):
        eventPass = False
        muons = Collection(event, "Muon")

        # trigger selection
        if not triggerSelector(event, self.year, self.trigger_name):
            return False

        muSel = MuonSelector(_year = self.year, _id_name = "medium", _iso_name = "PFIsoLoose",
                             _pt_corr = "Roch", _min_pt = 20, _max_eta = 2.4,
                             _max_d0PV = 0.05, _max_dzPV = 0.1, _min_lepMVA = -1)
        # muPair selection
        for iMu1, Mu1 in enumerate(muons):
            if not muSel.evalMuon(Mu1): continue
            for iMu2, Mu2 in enumerate(muons):
                if iMu2 <= iMu1: continue
                if not muSel.evalMuon(Mu2): continue 
                if self.OS_muPair and Mu1.charge == Mu2.charge: continue
                vec1 = ROOT.TLorentzVector(0,0,0,0)
                vec2 = ROOT.TLorentzVector(0,0,0,0)
                vec1.SetPtEtaPhiM(Mu1.pt, Mu1.eta, Mu1.phi, Mu1.mass)
                vec2.SetPtEtaPhiM(Mu2.pt, Mu2.eta, Mu2.phi, Mu2.mass)
                sumvec = vec1 + vec2
                if sumvec.M() < self.muPair_mass_min: continue
                eventPass = True

        return eventPass







