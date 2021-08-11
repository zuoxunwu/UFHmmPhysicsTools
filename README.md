# UFHmmPhysicsTools
UF Physics Tools for Hmm Analysis.

These tools are organized into directories of `analyzers`, `scripts`, and `plotters`.


## Set Up
These tools are made to be used in a CMSSW Environment. On LXPLUS the CMSSW Environment can be retrieved using `cmsrel`.
```
cmsrel CMSSW_10_6_19_patch2
cd CMSSW_10_6_19_patch2/src

cmsenv
voms-proxy-init --voms cms
```

Each time you would login on LXPLUS you will need to change to the `CMSSW_10_6_19_patch2/src` directory and run,
```
cmsenv
voms-proxy-init --voms cms
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

#### Set up Rochester Correction
Go to directory `PhysicsTools/UFHmmPhysicsTools/src` and run script `makeSharedObject.sh`
```
. ./makeSharedObject.sh
```
A shared object `RoccoR_cc.so` will be made in this directory, which is loaded in `PhysicsTools/UFHmmPhysicsTools/python/helpers/roccorHelper.py` for Rochester Correction.  


## Scripts
The only script in the framework is `hmm_postproc.py` which intializes the relavent branches, creates the ROOT output files, and runs the event loop. Accompanying the `hmm_postproc.py` is the `keep_and_drop_input.txt` file which controls which branches are kept or dropped. If your analyzer uses any specific branches such as `Electron`, `Muon`, `GenPart`, then it needs to be added to `keep_and_drop_input.txt`. 

Additionally, in the `scripts` directory there is a text file that has dataset information written in JSON format in `dataset_config.txt` this is where you can add dataset parameters such as files, MC flags, or other options. 

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

Alternatively, you can add your datasets to the `dataset_config.txt` file in the `scripts` directory to easily call your analyzer on a specific set of input root files. Then you can run the analyzer using,
```
python PhysicsTools/UFHmmPhysicsTools/scripts/hmm_postproc.py \
        -N 1000 \
        --ds "<dataset-name>" \
        --hdir <output-hist-directory> \
        --hfile <output-hist-file> \
        -I PhysicsTools.UFHmmPhysicsTools.analyzers.<your-analyzer> <your-analyzer>
```

## Plotting
After running the analyzer and retrieving the output histograms, `plotter.py` can be used to stack, stylize, and export the plots from multiple root files to PDF format.

To run `plotter.py` from the `src` directory:
```
./PhysicsTools/UFHmmPhysicsTools/plotting/plotter.py --m <matching-method> --pfs <plot-title-prefixes> --lbs <dict-of-prefixes-to-labels> <output-pdf-dir> <root-plot-dir>  <root-files>
``` 

`--m ` The matching method is used to determine how the plots will be paired both between and within files. Matching plots will be overlaid in the same canvas with a legend.
* `"none"`
    * No plots will be matched and will each be plotted on a different canvas
* `"name-bet-files"`
    * Plots will be matched with plots of the exact same name between each of the files
* `"name-in-files"`
    * Plots will be matched with plots of the same prefix in the same file
* `"name-bet-in-files"` or `" name-in-bet-files"`
    * Plots will be matched with plots of the same prefix between each of the files

`--pfs` The Plot Title Prefixes are used to match plots between the same file that have the same type of data in them. This is entered as a comma seperated strng. For Example, `"nMuon, dimu_mass, mu_eta"`

`--lbs` Adding Labels to Plots can be done through a dictionary, passed in as a string, that has the form `"{'prefix':'Main Title', 'X-Axis Title', 'Y-Axis Title'}"`. The prefix keys must match the prefixes passed in the `--pfs` option in the command.

All together an example command would be: 
```
./PhysicsTools/UFHmmPhysicsTools/plotting/plotter.py \
        --m "name-bet-in-files" \
        --pfs "nMuon, dimu_mass, mu_eta" \
        --lbs "{'nMuon':['nMuon','Number of Muons', 'Counts'], 'dimu_mass':['diMuon Invariant Mass', 'm_{#mu^{+} #mu^{-}} (GeV/c^{2})', 'Counts'], 'mu_eta':['Muon #eta','#eta', 'Counts']}" \
        /pdfs /plots hist_out_DYJets.root hist_out_ZH_HToMuMu.root
```

