# This is a (perhaps stupid) way to load the cpp Rochester Correction library into python scripts
# The command below generates a shared library object RoccoR_cc.so, which can be loaded with ROOT.gSystem.Load()
# There should be better ways to do this. -- XWZ 2021.07.31

root -l .L RoccoR.cc++
