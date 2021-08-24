
class ObjectSelector:
    def __init__(self, _year = "None" ):
        self.year = _year


class MuonSelector(ObjectSelector):
    def __init__(self, _year = "None", _id_name = "medium", _iso_name = "PFIsoLoose",
                 _pt_corr = "Roch", _min_pt = 20, _max_eta = 2.4, 
                 _max_d0PV = 0.05, _max_dzPV = 0.1, _min_lepMVA = -1):

        self.year = _year
        self.id_name  = _id_name
        self.iso_name = _iso_name
        self.pt_corr  = _pt_corr
        self.min_pt   = _min_pt
        self.max_eta  = _max_eta
        self.max_d0PV   = _max_d0PV
        self.max_dzPV   = _max_dzPV
        self.min_lepMVA = _min_lepMVA

    # Add these functions if the user prefers to protect these variables, 
    # otherwise I think setattr(object, name, value) is simple enough -- XWZ 2021.07.23 
    def setCutPt(self, val):
        self.min_pt = val

    def setCutLepMVA(self, val):
        self.min_lepMVA = val

    def evalMuon(self, muon):
        # ID
        if   self.iso_name == "medium" and not muon.mediumId: return False
        # Iso
        if   self.iso_name == "PFIsoLoose"   and muon.pfIsoId < 2:   return False
        elif self.iso_name == "MiniIsoLoose" and muon.miniIsoId < 1: return False
        # pt
        if self.pt_corr == "Roch":
            if muon.pt < self.min_pt: return False ## Roch not implemented in this framework. To be updated -- XWZ 2021.07.23
        else:
            if muon.pt < self.min_pt: return False
        # others
        if abs(muon.eta) > self.max_eta: return False
        if abs(muon.dxy) > self.max_d0PV: return False
        if abs(muon.dz)  > self.max_dzPV: return False
        # lepMVA not implemented in this framework. To be updated -- XWZ 2021.07.23
        return True



class ElectronSelector(ObjectSelector):
    def __init__(self, _year = "None", _id_name = "mvaIsoWP90",  _convVeto = True,
                 _min_pt = 20, _max_eta = 2.5, 
                 _max_d0PV = 0.05, _max_dzPV = 0.1, _min_lepMVA = -1):

        self.year = _year
        self.id_name  = _id_name
        self.convVeto = _convVeto
        self.min_pt   = _min_pt
        self.max_eta  = _max_eta
        self.max_d0PV   = _max_d0PV
        self.max_dzPV   = _max_dzPV
        self.min_lepMVA = _min_lepMVA

    # Add these functions if the user prefers to protect these variables, 
    # otherwise I think setattr(object, name, value) is simple enough -- XWZ 2021.07.23 
    def setCutPt(self, val):
        self.min_pt = val

    def setCutLepMVA(self, val):
        self.min_lepMVA = val

    def evalEle(self, ele):
        # ID and Iso
        if self.iso_name == "mvaIsoWP90" and not ele.mvaFall17V1Iso_WP90: return False
        if self._convVeto and not ele.convVeto: return False
        # pt
        if ele.pt < self.min_pt: return False
        # others
        if abs(ele.eta) > self.max_eta: return False
        if abs(ele.dxy) > self.max_d0PV: return False
        if abs(ele.dz)  > self.max_dzPV: return False
        # lepMVA not implemented in this framework. To be updated -- XWZ 2021.07.23
        return True


