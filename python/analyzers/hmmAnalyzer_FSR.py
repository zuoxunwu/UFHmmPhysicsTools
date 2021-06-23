import math as Math
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True


class hmmAnalyzer_FSR(Module):
    def __init__(self):
        self.writeHistFile = True
        pass

    def beginJob(self, histFile=None, histDirName=None):
        Module.beginJob(self, histFile, histDirName)
        print("starting module")

        self.dimu_no_GP = ROOT.TH1F('allGP_noFSR', 'No FSR', 200, 0, 200)
        self.dimu_with_GP = ROOT.TH1F('allGP_withFSR', 'With FSR', 200, 0, 200)
        self.dimu_no_ND = ROOT.TH1F('allND_noFSR', 'No FSR', 200, 0, 200)
        self.dimu_with_ND = ROOT.TH1F('allND_withFSR', 'With FSR', 200, 0, 200)

        self.dimu_ND_FSR_B = ROOT.TH1F('ND_fsr_before', 'Before FSR Correction', 200, 0, 200)
        self.dimu_ND_FSR_A = ROOT.TH1F('ND_fsr_after', 'After FSR Correction', 200, 0, 200)

        self.dimu_GP_FSR_B = ROOT.TH1F('GP_fsr_before', 'Before FSR Correction', 200, 0, 200)
        self.dimu_GP_FSR_A = ROOT.TH1F('GP_fsr_after', 'After FSR Correction', 200, 0, 200)

        self.addObject(self.dimu_no_GP)
        self.addObject(self.dimu_with_GP)
        self.addObject(self.dimu_no_ND)
        self.addObject(self.dimu_with_ND)

        self.addObject(self.dimu_ND_FSR_B)
        self.addObject(self.dimu_ND_FSR_A)
        self.addObject(self.dimu_GP_FSR_B)
        self.addObject(self.dimu_GP_FSR_A)

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
                    if(g.pt > 2 and (abs(g.eta) < 1.4 or (abs(g.eta) > 1.6 and abs(g.eta) < 2.4))):
                        dR = ((g.eta-mu.eta)**2 + (g.phi-mu.phi)**2)**(.5)
                        if(dR < .5):
                            if(g.pt/mu.pt < 0.4):
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
        fsrPhotons = Collection(event, "FsrPhoton")

        #Selecting Events with exactly 2 Muons
        if(not len(muons)==2):
            return True

        #Applying PT cuts
        if(not muons[0].pt > 26 or not muons[1].pt > 26):
            return True

        #Applying ETA cuts
        if(not abs(muons[0].eta) < 2.4 or not abs(muons[1].eta) < 2.4):
            return True

        #Applying Trigger Selection cuts
        doesPassTrigSelection, trigObjIndex = self.trigObjSelector(trigObj)
        if(not doesPassTrigSelection):
            return True
        #Applying dR Selection to match Trigger Object to the muons tested.
        if(not self.dRSelection(trigObj[trigObjIndex].eta, trigObj[trigObjIndex].phi, muons[0].eta, muons[0].phi) and not self.dRSelection(trigObj[trigObjIndex].eta, trigObj[trigObjIndex].phi, muons[1].eta, muons[1].phi)):
            return True
        #Applying GenPart cut for MC
        checkGenParents, p4_FSR = self.checkGenParents(muons, genPart)
        if(not checkGenParents and not p4_FSR):
            return True
        dimu = muons[0].p4() + muons[1].p4()


        if(p4_FSR):
            self.dimu_GP_FSR_B.Fill(dimu.M())
            dimu = dimu + p4_FSR
            self.dimu_GP_FSR_A.Fill(dimu.M())
            self.dimu_with_GP.Fill(dimu.M())
        else:
            self.dimu_no_GP.Fill(dimu.M())

        #Correcting for FSR using NanoAOD Premade Variables
        p4FSR_ND, dROverEt2_min_candiate = None, 1000
        for photon in fsrPhotons:
            if(photon.pt > 2 and (abs(photon.eta) < 1.4 or (abs(photon.eta) > 1.6 and abs(photon.eta) < 2.4))):
                dR = ((photon.eta-muons[photon.muonIdx].eta)**2 + (photon.phi-muons[photon.muonIdx].phi)**2)**(.5)
                if(dR < .5):
                    if(photon.relIso03 < 1.8):
                        if(photon.dROverEt2 < 0.012):
                            if(photon.pt/muons[photon.muonIdx].pt < 0.4):
                                if(photon.dROverEt2 < dROverEt2_min_candiate or dROverEt2_min_candiate == 1000):
                                    vect = ROOT.TLorentzVector()
                                    vect.SetPtEtaPhiM(photon.pt, photon.eta, photon.phi, 0)
                                    p4FSR_ND = vect
        if(p4FSR_ND):
            dimu = muons[0].p4() + muons[1].p4()
            vect = ROOT.TLorentzVector()
            vect.SetPxPyPzE(p4FSR_ND.Px(), p4FSR_ND.Py(), p4FSR_ND.Pz(), p4FSR_ND.E())
            self.dimu_ND_FSR_B.Fill(dimu.M())
            dimu = dimu + vect
            self.dimu_ND_FSR_A.Fill(dimu.M())
            self.dimu_with_ND.Fill(dimu.M())
        else:
            self.dimu_no_ND.Fill(dimu.M())


        return True


