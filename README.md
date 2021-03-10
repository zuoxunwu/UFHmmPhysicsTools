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

Finally, we can run scram to compile all moduels.
```
scram b -j8
```
## Analyzers

## Selectors

## Scripts

