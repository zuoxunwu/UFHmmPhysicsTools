# UFHmmPhysicsTools
UF Physics Tools for Hmm Analysis.

These tools are organized into directories of `selectors`, `analyzers`, and `scripts`.


## Set Up
These tools are made to be used in a CMSSW Environment. On LXPLUS the CMSSW Environment can be retrieved using `cmsrel`.
```
cmsrel CMSSW_10_6_19_patch2
cd CMSSW_10_6_19_patch2/src

cmsenv
```

Additionally, these tools depend on the NanoAOD tools. We can get these analysis tools and the NanoAOD tools and put them into the `src` directories of the CMSSW Environment.
```
git clone https://github.com/cms-nanoAOD/nanoAOD-tools.git PhysicsTools/NanoAODTools
git clone git@github.com:jrotter2/UFHmmPhysicsTools.git PhysicsTools/UFHmmPhysicsTools
```

Finally, we can run scram to compile all modules.
```
scram b -j8
```
## Analyzers
Analyzers are stored in `python/analyzers` directory and are used as imported modules by `hmm_postproc.py` to analyze events and build histograms. 

The structure of an analyzer module comes in two main parts:

* `beginJob()`
    * Initialize histograms and add them to `self`

* `analyze()`
    * Initialize collections, perform selections, fill histograms


Once an analyzer has been created it can be executed in the `src` directory using `hmm_postproc.py`.
```
python PhysicsTools/UFHmmPhysicsTools/scripts/hmm_postproc.py \
        -c "0==0" \
        -N 1000 \
        --bi PhysicsTools/UFHmmPhysicsTools/scripts/keep_and_drop_input.txt \
        --noout True \
        --hdir <output-hist-directory> \
        --hfile <output-hist-file> \
        -I PhysicsTools.UFHmmPhysicsTools.analyzers.<your-analyzer> <your-analyzer> \
        <input-root-file>
```
This will run the module found at `PhysicsTools/UFHmmPhysicsTools/python/analyzers/<your-analyzer>` and create a ROOT file at `<output-hist-file>` relative to the `src` directory with the histogram in the ROOT directory `<output-hist-directory>`.

## Plotting
After running the analyzer and retrieving the output histograms, `plotter.py` can be used to stack, stylize, and export the plots from multiple root files to PDF format.

To run `plotter.py` from the `src` directory:
```
./PhysicsTools/UFHmmPhysicsTools/plotting/plotter.py --m <matching-method> --pfs <plot-title-prefixes> <output-pdf-dir> <root-plot-dir>  <root-files>
``` 

`--m ` The matching method is used to determine how the plots will be paired both between and within files. Matching plots will be overlaid in the same canvas with a legend.
* "none"
    * No plots will be matched and will each be plotted on a different canvas
* "name-bet-files"
    * Plots will be matched with plots of the exact same name between each of the files
* "name-in-files"  
    * Plots will be matched with plots of the same prefix in the same file
* "name-bet-in-files"  or " name-in-bet-files"
    * Plots will be matched with plots of the same prefix between each of the files

`--pfs` The Plot Title Prefixes are used to match plots between the same file that have the same type of data in them. This is entered as a comma seperated strng. For Example, `"nMuon, dimu_mass, mu_eta"`

All together an example command would be: 
```
./PhysicsTools/UFHmmPhysicsTools/plotting/plotter.py --m "name-bet-in-files" --pfs "nMuon, dimu_mass, mu_eta" /pdfs /plots hist_out_DYJets.root hist_out_ZH_HToMuMu.root
```
## Scripts

