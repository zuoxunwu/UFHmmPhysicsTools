from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Event, Object, Collection
from PhysicsTools.UFHmmPhysicsTools.python.helpers.objectSelector import MuonSelector, ElectronSelector


def _trigSelector(event, year = None, trigger_name = None):
    muons = Collection(event, "Muon")
    trigObjs = Collection(event, "TrigObj")

    def _trigMatch(trigObj, obj):
        dR2 = (trigObj.eta - obj.eta) ** 2 + (trigObj.phi - obj.phi) ** 2 
        if dR2 < 0.01 : return True
        else:           return False

    if trigger_name == "SingleMu":
        trig_pt_min = 26
        if year = 2017: trig_pt_min = 29
        muSel = MuonSelector(_year = year, _id_name = "medium", _iso_name = "PFIsoLoose",
                             _pt_corr = "Roch", _min_pt = trig_pt_min, _max_eta = 2.4,
                             _max_d0PV = 0.05, _max_dzPV = 0.1, _min_lepMVA = -1)
        for trig in trigObjs:
            if abs(trig.id) != 13 or (trig.filterBits / 8) % 2 != 1: continue
            for muon in muons:
                if not muSel.evalMuon(muon): continue
                if _trigMatch(trig, muon): return True
    ## More trigger paths to be added here. -- XWZ 2021.07.23
    else: 
        print "****** Trigger name not recognized. Selecting no event. ******"
        
    return False


def triggerSelector(event, year = None, trigger_name = None):
    if trigger_name == None:
        print "****** Weird case: No trigger specified. Selecting no event. ******"
        return False
    if year == None:
        print "****** Weird case: No year specified. Use 2018 setup. ******"
        year = 2018

    trig_pass = False
    if isinstance(trigger_name, list):
        for trig_name in trigger_name:
            if _trigSelector(event, year, trig_name):
                trig_pass = True
    else:
        if _trigSelector(event, year, trigger_name):
            trig_pass = True
    return trig_pass

