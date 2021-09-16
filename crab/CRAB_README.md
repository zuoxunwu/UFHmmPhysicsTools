## General explanation

A few essential components are needs for running crab jobs: 
- A crab configuration file (`crab_cfg.py`) to give specs of this job.
- A CMSSW parameter set (`PSet.py`) to call CMSSW modules.
- A `FrameworkJobReport.xml` at the remote machine that runs the job.

The NanoAOD-tools is separate from the CMSSW. In principle there is no need to call CMSSW functionalities when running jobs on NanoAOD. So the NanoAOD-tools provides a dummy PSet and makes a basic [jobReport](https://github.com/cms-nanoAOD/nanoAOD-tools/blob/555b3075892c38b63a98f84527685fa042ffcf59/python/postprocessing/framework/postprocessor.py#L36) to make sure the job runs through. The actual job tasks are performed by the user defined scripts `crab/crab_script.sh` and `crab/crab_script.py`.

In PhysicsTools/UFHmmPhysicsTools this workflow is wrapped by `crab/make_batch_crab_jobs.py`
It is enough to only interact with this script.

## Steps for job submission

You may want to make a git tag before submitting crab jobs
```
git tag -a v1.0 -m "version 1.0"
```
The tag is used in your crab request name and output file destination.
You can run
```
python crab/make_batch_crab_jobs.py
```
which generates a crab working area `<CRAB_timestamp_tag>`, containing a collection of crab config files, one for each sample to process.
You can submit and check crab jobs with
```
./<CRAB_timestamp_tag>/submit_all.sh
./<CRAB_timestamp_tag>/check_all.sh
```

###### Remarks

For the git tag to work, this script should be run within the PhysicsTools/UFHmmPhysicsTools environment.
The `make_batch_crab_jobs.py` script also takes options like
```
python crab/make_batch_crab_jobs.py -s ggH DY -m analyzers.hmmAnalyzer.hmmAnalyzer -o hists.root 
```
See more details in the args options in the script.

## Crab config remarks

To test "Automatic" splitting more. See [explanation](https://twiki.cern.ch/twiki/bin/view/CMSPublic/CRAB3FAQ#What_is_the_Automatic_splitting)
Maybe "FileBased" is good enough for all NanoAOD usages.

## To do

Simplify sample list. 
Some features not necessary: nEvt and files.
Some features can be implemented differently: GT and JEC.
Sample definition may just be reduced to name and DAS.

Make a common tree slim module.
In CRAB jobs, trees are always saved. If not slim it is a copy of the original NanoAOD file.
Should not run massive analysis without tree slimming.
