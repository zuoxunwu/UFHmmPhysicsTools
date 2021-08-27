import ROOT


# Find FWHM of a TH1 hist, return bin numbers for low and high ends
def findFWHM(hist, window = 0, VERBOSE = False):
    xmax = 0
    ymax = 0
    # integrate a small window to mitigate fluctuations in fine-binned hists
    if window == 0: 
        window = min(1, hist.GetNbinsX() // 40)

    if hist.GetEntries() < 50:
      print 'Looking for FWHM in %s, too few entries (%d). Return X axis range as FWHM.' %(hist.GetName(), hist.GetEntries())
      return (1, hist.GetNbinsX())

    for i in range(window + 1, hist.GetNbinsX() - window + 1):
      if ymax < hist.Integral(i-window, i+window):
        ymax = hist.Integral(i-window, i+window)
        xmax = i
    if ymax == 0:
      print 'Weird case: no max found in hist. Return X axis range as FWHM'
      return (1, hist.GetNbinsX())

    lo_bin = hist.GetNbinsX()
    hi_bin = 1
    for i in range(window + 1, hist.GetNbinsX() -  window + 1):
      if i < lo_bin and hist.Integral(i-window, i+window) > ymax/2.0: lo_bin = i
      if i > hi_bin and hist.Integral(i-window, i+window) > ymax/2.0: hi_bin = i

    if VERBOSE: print "FWHM is %f to %f" %(hist.GetBinCenter(lo_bin), hist.GetBinCenter(hi_bin))
    return (lo_bin, hi_bin)
