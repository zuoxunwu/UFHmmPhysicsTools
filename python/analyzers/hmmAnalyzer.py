
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
        self.h_nMu_no_sel = ROOT.TH1F('nMuons_no_sel', 'nMuons_no_sel', 10, 0, 10)
        self.h_nMu_pt_sel = ROOT.TH1F('nMuons_pt_sel', 'nMuons_pt_sel', 10, 0, 10)
        self.h_nMu_pt_eta = ROOT.TH1F('nMuons_pt_eta', 'nMuons_pt_sel', 10, 0, 10)
        self.h_nMu_pt_eta_trig = ROOT.TH1F('nMuons_pt_eta_trig', 'nMuons_pt_sel_trig', 10, 0, 10)
        self.h_nMu_pt_eta_trig_genPart = ROOT.TH1F('nMuons_pt_eta_trig_genPart', 'nMuons_pt_sel_trig_genPart', 10, 0, 10)

        self.h_dimu_mass_no_sel = ROOT.TH1F('dimu_mass_no_sel', 'dimu_mass_no_sel', 200, 0, 200)
        self.h_dimu_mass_pt_sel = ROOT.TH1F('dimu_mass_pt_sel', 'dimu_mass_pt_sel', 200, 0, 200)
        self.h_dimu_mass_pt_eta = ROOT.TH1F('dimu_mass_pt_eta', 'dimu_mass_pt_eta', 200, 0, 200)
        self.h_dimu_mass_pt_eta_trig = ROOT.TH1F('dimu_mass_pt_eta_trig', 'dimu_mass_pt_eta_trig', 200, 0, 200)
        self.h_dimu_mass_pt_eta_trig_genPart = ROOT.TH1F('dimu_mass_pt_eta_trig_genPart', 'dimu_mass_pt_eta_trig_genPart', 200, 0, 200)

        self.h_mu_eta_no_sel = ROOT.TH1F('mu_eta_no_sel', 'mu_eta_no_sel', 200, -5, 5)
        self.h_mu_eta_pt_sel = ROOT.TH1F('mu_eta_pt_sel', 'mu_eta_pt_sel', 200, -5, 5)
        self.h_mu_eta_pt_eta = ROOT.TH1F('mu_eta_pt_eta', 'mu_eta_pt_eta', 200, -5, 5)
        self.h_mu_eta_pt_eta_trig = ROOT.TH1F('mu_eta_pt_eta_trig', 'mu_eta_pt_eta_trig', 200, -5, 5)
        self.h_mu_eta_pt_eta_trig_genPart = ROOT.TH1F('mu_eta_pt_eta_trig_genPart', 'mu_eta_pt_eta_trig_genPart', 200, -5, 5)
        self.addObject(self.h_nMu_no_sel)
        self.addObject(self.h_nMu_pt_sel)
        self.addObject(self.h_nMu_pt_eta)
        self.addObject(self.h_nMu_pt_eta_trig)
        self.addObject(self.h_nMu_pt_eta_trig_genPart)
        self.addObject(self.h_dimu_mass_no_sel)
        self.addObject(self.h_dimu_mass_pt_sel)
        self.addObject(self.h_dimu_mass_pt_eta)
        self.addObject(self.h_dimu_mass_pt_eta_trig)
        self.addObject(self.h_dimu_mass_pt_eta_trig_genPart)
        self.addObject(self.h_mu_eta_no_sel)
        self.addObject(self.h_mu_eta_pt_sel)
        self.addObject(self.h_mu_eta_pt_eta)
        self.addObject(self.h_mu_eta_pt_eta_trig)
        self.addObject(self.h_mu_eta_pt_eta_trig_genPart)
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
            print(g.genPartIdxMother, g.pdgId)
            if(g.genPartIdxMother == motherPartIdx and g.pdgId == 22):
                return g.p4()
        return False

    def checkGenParents(self, muons, genPart):
        doesPass_gen_parent_cut = True
        p4_FSR = any
        if(not genPart):
            return True
        for mu in muons:
            parent_pdgId = genPart[genPart[mu.genPartIdx].genPartIdxMother].pdgId
            #23 -> Z boson, 25 -> Higgs
            if(abs(parent_pdgId) == 13 and genPart[genPart[genPart[mu.genPartIdx].genPartIdxMother].genPartIdxMother].pdgId == 25):
                p4_FSR = self.checkGenDaughters(genPart, genPart[mu.genPartIdx].genPartIdxMother)
            if(parent_pdgId != 23 and parent_pdgId != 25):
                doesPass_gen_parent_cut = False
        return doesPass_gen_parent_cut, p4_FSR

    def trigObjSelector(self, trigObj):
        doesPass = False
        trigObjIndex = -1
        for i in range(0, len(trigObj)):
            if(abs(trigObj[i].id) == 13 and len(str(bin(trigObj[i].filterBits))) > 4 and str(bin(trigObj[i].filterBits))[4] is "1"):
                doesPass = True
                trigObjIndex = i
        return doesPass, trigObjIndex

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        muons = Collection(event, "Muon")
        trigObj = Collection(event, "TrigObj")
        genPart = Collection(event, "GenPart")

        #Fill Histograms Before Selection
        self.h_nMu_no_sel.Fill(len(muons))

        #Fill Histograms After Selecting Events with exactly 2 Muons
        if(not len(muons)==2):
            return True
        dimu = muons[0].p4() + muons[1].p4()
        self.h_dimu_mass_no_sel.Fill(dimu.M())
        self.h_mu_eta_no_sel.Fill(muons[0].eta)
        self.h_mu_eta_no_sel.Fill(muons[1].eta)

        #Applying PT cuts
        if(not muons[0].pt > 26 or not muons[1].pt > 26):
            return True
        self.h_nMu_pt_sel.Fill(len(muons))
        dimu = muons[0].p4() + muons[1].p4()
        self.h_dimu_mass_pt_sel.Fill(dimu.M())
        self.h_mu_eta_pt_sel.Fill(muons[0].eta)
        self.h_mu_eta_pt_sel.Fill(muons[1].eta)

        #Applying ETA cuts
        if(not abs(muons[0].eta) < 2.4 or not abs(muons[1].eta) < 2.4):
            return True
        self.h_nMu_pt_eta.Fill(len(muons))
        dimu = muons[0].p4() + muons[1].p4()
        self.h_dimu_mass_pt_eta.Fill(dimu.M())
        self.h_mu_eta_pt_eta.Fill(muons[0].eta)
        self.h_mu_eta_pt_eta.Fill(muons[1].eta)

        #Applying Trigger Selection cuts
        doesPassTrigSelection, trigObjIndex = self.trigObjSelector(trigObj)
        if(not doesPassTrigSelection):
            return True
        #Applying dR Selection to match Trigger Object to the muons tested.
        if(not self.dRSelection(trigObj[trigObjIndex].eta, trigObj[trigObjIndex].phi, muons[0].eta, muons[0].phi) and not self.dRSelection(trigObj[trigObjIndex].eta, trigObj[trigObjIndex].phi, muons[1].eta, muons[1].phi)):
            return True

        self.h_nMu_pt_eta_trig.Fill(len(muons))
        self.h_dimu_mass_pt_eta_trig.Fill(dimu.M())
        self.h_mu_eta_pt_eta_trig.Fill(muons[0].eta)
        self.h_mu_eta_pt_eta_trig.Fill(muons[1].eta)
        
        checkGenParents, p4_FSR = self.checkGenParents(muons, genPart)
        if(not checkGenParents):
            return True
        if(p4_FSR):
            dimu = muons[0].p4() + muons[1].p4() + p4_FSR.p4()
        self.h_nMu_pt_eta_trig_genPart.Fill(len(muons))
        self.h_dimu_mass_pt_eta_trig_genPart.Fill(dimu.M())
        self.h_mu_eta_pt_eta_trig_genPart.Fill(muons[0].eta)
        self.h_mu_eta_pt_eta_trig_genPart.Fill(muons[1].eta)


#        if(doesPassTrigSelection):
#            if(len(muons) == 2 and muons[0].charge*muons[1].charge < 0):
#                if(dRSelection(trigObj[trigObjIndex].eta, trigObj[trigObjIndex].phi, muons[0].eta, muons[0].phi) or dRSelection(trigObj[trigObjIndex].eta, trigObj[trigObjIndex].phi, muons[1].eta, muons[1].phi)):
#                    if(pT_etaSelection(muons)):
#                        if(checkGenParents(muons, genPart)):   
        #self.h_nMu.Fill(len(muons))
        #dimu = muons[0].p4() + muons[1].p4()
        #self.h_dimu_mass.Fill(dimu.M())

        return True
