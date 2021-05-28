
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
        print("starting module")

        self.nMuon_raw = ROOT.TH1F('rnMuon_raw', 'No Selection', 10, -0.5, 9.5)
        self.eta_raw = ROOT.TH1F('reta_raw', 'No Selection', 100, -5, 5)
        self.pt_raw = ROOT.TH1F('rpt_raw', 'No Selection', 200, 0, 200)

	self.eta_kin_cut = ROOT.TH1F('eta_kin_cut', '26 GeV pT Cut', 100, -5, 5)
        self.pt_kin_cut = ROOT.TH1F('pt_kin_cut', '26 GeV pT Cut', 200, 0, 200)
        self.dimu_kin_cut = ROOT.TH1F('dimu_kin_cut', '26 GeV pT Cut', 200, 0, 200)

        self.eta_trig_cut = ROOT.TH1F('eta_trig_cut', 'Trigger Matching Cut', 100, -5, 5)
        self.pt_trig_cut = ROOT.TH1F('pt_trig_cut', 'Trigger Matching Cut', 200, 0, 200)
        self.dimu_trig_cut = ROOT.TH1F('dimu_trig_cut', 'Trigger Matching Cut', 200, 0, 200)

        self.eta_gen_cut = ROOT.TH1F('eta_gen_cut', 'GenPart Matching Cut', 100, -5, 5)
        self.pt_gen_cut = ROOT.TH1F('pt_gen_cut', 'GenPart Matching Cut', 200, 0, 200)
        self.dimu_gen_cut = ROOT.TH1F('dimu_gen_cut', 'GenPart Matching Cut', 200, 0, 200)

        self.eta_final = ROOT.TH1F('eta_final', 'Accepted', 100, -5, 5)
        self.pt_final = ROOT.TH1F('pt_final', 'Accepted', 200, 0, 200)
        self.dimu_final = ROOT.TH1F('dimu_final', 'Accepted', 200, 0, 200)

        self.dimu_beforeFSR = ROOT.TH1F('fsr_before', 'Before FSR Correction', 200, 0, 200)
        self.dimu_afterFSR = ROOT.TH1F('fsr_after', 'After FSR Correction', 200, 0, 200)

        self.addObject(self.nMuon_raw)
        self.addObject(self.eta_raw)
        self.addObject(self.pt_raw)

        self.addObject(self.eta_kin_cut)
        self.addObject(self.pt_kin_cut)
        self.addObject(self.dimu_kin_cut)

        self.addObject(self.eta_trig_cut)
        self.addObject(self.pt_trig_cut)
        self.addObject(self.dimu_trig_cut)

        self.addObject(self.eta_gen_cut)
        self.addObject(self.pt_gen_cut)
        self.addObject(self.dimu_gen_cut)

        self.addObject(self.eta_final)
        self.addObject(self.pt_final)
        self.addObject(self.dimu_final)

        self.addObject(self.dimu_beforeFSR)
        self.addObject(self.dimu_afterFSR)
        print("finished making hists")
        pass

#- Event triggered a single muon trigger (line 35)
#- There are at least 2 oppositely charged muons in the event (line 36)
#(we can talk about cases where there are more than 2 muons. for now you can veto them)
#- At least one of these muons match the muon that triggered the event (this can be optional to begin with) (line 40)
#- pT of these muons are > 20 GeV (we can fine tune this later) (line 48)
#- eta of these muons are < 2.4 (line 48)
#- for MC only: check if the muons originate from a Higgs or a Z (this is also optional as well) 

    def dRSelection(self, eta1, phi1, eta2, phi2):
        return ((eta1-eta2)**2 + (phi1-phi2)**2) < (.1*.1)

    def checkGenDaughters(self, genPart, motherPartIdx):
        for g in genPart:
            #print(g.genPartIdxMother, g.pdgId)
            if(g.genPartIdxMother == motherPartIdx and g.pdgId == 22):
                return g
        return False

    def checkGenParents(self, muons, genPart):
        doesPass_gen_parent_cut = True
        p4_FSR = None
        if(not genPart):
            return True
        for mu in muons:
            if(mu.genPartIdx < 0):
                continue
            parent_pdgId = abs(genPart[genPart[mu.genPartIdx].genPartIdxMother].pdgId)
            #23 -> Z boson, 25 -> Higgs
            if(abs(parent_pdgId) == 13 and genPart[genPart[genPart[mu.genPartIdx].genPartIdxMother].genPartIdxMother].pdgId == 25):
                g = self.checkGenDaughters(genPart, genPart[mu.genPartIdx].genPartIdxMother)
                if(g):
                    p4_FSR = g.p4()
            if(parent_pdgId != 23 and parent_pdgId != 25):
                doesPass_gen_parent_cut = False
        return doesPass_gen_parent_cut, p4_FSR

    def trigObjSelector(self, trigObj):
        doesPass = False
        trigObjIndex = -1
        for i in range(0, len(trigObj)):
            if(abs(trigObj[i].id) == 13 and len(str(bin(trigObj[i].filterBits))) > 4 and str(bin(trigObj[i].filterBits))[len(str(bin(trigObj[i].filterBits)))-4] is "1"):
                doesPass = True
                trigObjIndex = i
        return doesPass, trigObjIndex

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        muons = Collection(event, "Muon")
        trigObj = Collection(event, "TrigObj")
        genPart = Collection(event, "GenPart")

        #Fill Histograms Before Selection
        self.nMuon_raw.Fill(len(muons))
        for mu in muons:
            self.eta_raw.Fill(mu.eta)
            self.pt_raw.Fill(mu.pt)

        #Selecting Events with exactly 2 Muons
        if(not len(muons)==2):
            for mu in muons:
                self.eta_kin_cut.Fill(mu.eta)
                self.pt_kin_cut.Fill(mu.pt)
            return True
        dimu = muons[0].p4() + muons[1].p4()

        #Applying PT cuts
        if(not muons[0].pt > 26 or not muons[1].pt > 26):
            self.eta_kin_cut.Fill(muons[0].eta)
            self.eta_kin_cut.Fill(muons[1].eta)
            self.pt_kin_cut.Fill(muons[0].pt)
            self.pt_kin_cut.Fill(muons[1].pt)
            self.dimu_kin_cut.Fill(dimu.M())
            return True
        dimu = muons[0].p4() + muons[1].p4()

        #Applying ETA cuts
        if(not abs(muons[0].eta) < 2.4 or not abs(muons[1].eta) < 2.4):
            self.eta_kin_cut.Fill(muons[0].eta)
            self.eta_kin_cut.Fill(muons[1].eta)
            self.pt_kin_cut.Fill(muons[0].pt)
            self.pt_kin_cut.Fill(muons[1].pt)
            self.dimu_kin_cut.Fill(dimu.M())
            return True
        dimu = muons[0].p4() + muons[1].p4()

        #Applying Trigger Selection cuts
        doesPassTrigSelection, trigObjIndex = self.trigObjSelector(trigObj)
        if(not doesPassTrigSelection):
            self.eta_trig_cut.Fill(muons[0].eta)
            self.eta_trig_cut.Fill(muons[1].eta)
            self.pt_trig_cut.Fill(muons[0].pt)
            self.pt_trig_cut.Fill(muons[1].pt)
            self.dimu_trig_cut.Fill(dimu.M())
            return True
        #Applying dR Selection to match Trigger Object to the muons tested.
        if(not self.dRSelection(trigObj[trigObjIndex].eta, trigObj[trigObjIndex].phi, muons[0].eta, muons[0].phi) and not self.dRSelection(trigObj[trigObjIndex].eta, trigObj[trigObjIndex].phi, muons[1].eta, muons[1].phi)):
            self.eta_trig_cut.Fill(muons[0].eta)
            self.eta_trig_cut.Fill(muons[1].eta)
            self.pt_trig_cut.Fill(muons[0].pt)
            self.pt_trig_cut.Fill(muons[1].pt)
            self.dimu_trig_cut.Fill(dimu.M())
            return True
        #Applying GenPart cut for MC
        checkGenParents, p4_FSR = self.checkGenParents(muons, genPart)
        print p4_FSR, checkGenParents
        if(not checkGenParents and not p4_FSR):
            self.eta_gen_cut.Fill(muons[0].eta)
            self.eta_gen_cut.Fill(muons[1].eta)
            self.pt_gen_cut.Fill(muons[0].pt)
            self.pt_gen_cut.Fill(muons[1].pt)
            self.dimu_gen_cut.Fill(dimu.M())
            return True
        #Correcting for FSR
        if(p4_FSR):
            self.dimu_beforeFSR.Fill(dimu.M())
            dimu = dimu + p4_FSR
            self.dimu_afterFSR.Fill(dimu.M())
        #Adding to final histogram
        self.eta_final.Fill(muons[0].eta)
        self.eta_final.Fill(muons[1].eta)
        self.pt_final.Fill(muons[0].pt)
        self.pt_final.Fill(muons[1].pt)
        self.dimu_final.Fill(dimu.M())
        return True


# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed
#hmmAnalyzer = lambda: hmmAnalyzer()

