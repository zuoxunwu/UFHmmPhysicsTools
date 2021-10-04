from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.modules.common.muonScaleResProducer import muonScaleResProducer, mk_safe
import ROOT
import os
import random

ROOT.PyConfig.IgnoreCommandLineOptions = True

class roccorProducer(muonScaleResProducer):
    def __init__(self, rc_dir, rc_corrections, dataYear):
        p_postproc = '%s/src/PhysicsTools/UFHmmPhysicsTools' % os.environ[
            'CMSSW_BASE']
        p_roccor = p_postproc + '/data/' + rc_dir
        if "/RoccoR_cc.so" not in ROOT.gSystem.GetLibraries():
            p_helper = '%s/RoccoR.cc' % p_roccor
            print('Loading C++ helper from ' + p_helper)
            ROOT.gROOT.ProcessLine('.L ' + p_helper)
        self._roccor = ROOT.RoccoR(p_roccor + '/' + rc_corrections)


roccor2016aV5 = lambda: roccorProducer('roccor', 'RoccoR2016aUL.txt', 2016)
roccor2016bV5 = lambda: roccorProducer('roccor', 'RoccoR2016bUL.txt', 2016)
roccor2017V5  = lambda: roccorProducer('roccor', 'RoccoR2017UL.txt',  2017)
roccor2018V5  = lambda: roccorProducer('roccor', 'RoccoR2018UL.txt',  2018)



