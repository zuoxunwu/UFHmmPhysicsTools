from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Event, Object, Collection
from PhysicsTools.UFHmmPhysicsTools.python.helpers.objectSelector import MuonSelector, ElectronSelector
from PhysicsTools.UFHmmPhysicsTools.python.helpers.triggerSelector import triggerSelector


class EventSelector:
    def __init__(self, _year = None, _trigger_name = "SingleMu", 
                 _mu_trig_pt_min = 26, _OS_muPair = True, _muPair_mass_min = 60):

        self.year = _year
        self.trigger_name    = _trigger_name
        self.mu_trig_pt_min  = _mu_trig_pt_min
        self.OS_muPair       = _OS_muPair
        self.muPair_mass_min = _muPair_mass_min


    def evalEvent(self, event):
        muons = Collection(event, "Muon")

        # trigger sel
        if not triggerSelector(event, self.year, self.trigger_name)
            return False




