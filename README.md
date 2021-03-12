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

### Pre-Selection and Triggers
To modify the event loop to only loop over events that pass a given trigger combination, the pre-selection input can be changed from `0==0` to a boolean conbination of the HLT Trigger Paths. For example to apply the trigger selection `HLT_IsoMu20 or HLT_Mu20`,
```
python PhysicsTools/UFHmmPhysicsTools/scripts/hmm_postproc.py \
        -c "HLT_IsoMu20 || HLT_Mu20" \
        -N 1000 \
        --bi PhysicsTools/UFHmmPhysicsTools/scripts/keep_and_drop_input.txt \
        --noout True \
        --hdir <output-hist-directory> \
        --hfile <output-hist-file> \
        -I PhysicsTools.UFHmmPhysicsTools.analyzers.<your-analyzer> <your-analyzer> \
        <input-root-file>
```
Notice the use of `||` instead of `or`, similarly `&&` should be used in place of `and`. 

## Selectors

## Scripts

