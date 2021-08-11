import ROOT
import os

tool_dir = os.getcwd().split('/PhysicsTools', 1)[0] + '/PhysicsTools/UFHmmPhysicsTools/'
ROOT.gSystem.Load(tool_dir + 'src/RoccoR_cc.so')
from ROOT import RoccoR


class RochCorr():
    def __init__(self, _era):
        self.datafiles = {"2016aUL": tool_dir + "data/roccor/RoccoR2016aUL.txt",
                          "2016bUL": tool_dir + "data/roccor/RoccoR2016bUL.txt",
                          "2017UL" : tool_dir + "data/roccor/RoccoR2017UL.txt",
                          "2018UL" : tool_dir + "data/roccor/RoccoR2018UL.txt"
                         }
        self.era = _era
        self.rc = RoccoR(self.datafiles[_era])


    def pt_Roch(self, q = 0, pt = 0, eta = -99, phi = -99, genPt = 0, datatype = "None", sys_uncert = "central"):
        if q == 0: 
            print "Strange case: charge q = 0. Check Roch_pt input"
            return 0
        if pt == 0:
            print "Strange case: pt = 0. Check Roch_pt input"
            return 0
        if eta == -99:
            print "Strange case: eta = -99. Check Roch_pt input"
            return 0
        if phi == -99:
            print "Strange case: phi = -99. Check Roch_pt input"
            return 0
        if datatype != "data" and datatype != "MC":  # Assume datatype to be "data" or "MC". May change to other conventions in the future. -- XWZ 2021.08.11
           print "Strange case: do not recognize datatype as " + datatype
           return 0
        if datatype == "MC" and genPt == 0:
            "Strange case: genPt = 0 for MC. Check Roch_pt input"
            return 0
        # calculate Roch 
        sf = 0
        if datatype == "data":
            sf = self.rc.kScaleDT(q, pt, eta, phi)
            if sys_uncert == "up" or sys_uncert == "down":
                sf_err = self.rc.kScaleDTerror(q, pt, eta, phi)
                if sys_uncert == "up": sf = sf + sf_err
                else                 : sf = sf - sf_err
        else:
            sf = self.rc.kSpreadMC(q, pt, eta, phi, genPt)
            if sys_uncert == "up" or sys_uncert == "down":
                sf_err = self.rc.kSpreadMCerror(q, pt, eta, phi, genPt)
                if sys_uncert == "up": sf = sf + sf_err
                else                 : sf = sf - sf_err
        return pt * sf


