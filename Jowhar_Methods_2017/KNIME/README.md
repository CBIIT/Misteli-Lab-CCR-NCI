A) The attached production workflow is run on Linux (64-bit) with 56-Cores/Threads (28-CPUs), 190GB RAM, 400GB SSD for KNIME-TEMP.
   1) KNIME Preferences is also in this folder: knime321_preferences.epf
   2) KNIME Configuration captured from the KNIME -> Help--> Installation Details is also in this folder: knime321_configuration.txt

B) The workflow(s) are TESTED exclusively on KNIME 3.2.1. The workflow will MOST likely fail with KNIME 3.3.X release because of changes to the "Feature Calculator (Beta)" node in the KNIME-KNIP 3.3.x release. 

C) Before you execute this workflow please set the path to python executable with appropriate packages:

Python Setup for KNIME-KNIP (Version 3.2.1):

The python/conda environment detailes we are using is provided in the following YML file:
knime321_condapython_environment.yml

Do the following to setup a python (virtual) environment called `knime321` using `conda`:
conda env create -f knime321_condapython_environment.yml

To activate the `knime321` virtual environment do the following (Note: python/conda/virtualenv should be in your PATH):
source activate knime321

Now set the KNIME Pereferences for `Path to Python Executable` to the `python` executable in the virtual environment knime321:
e.g.: /home/<username>/.conda/envs/knime321/bin/python

D) It also expected to point ImageJ1 preferences in KNIME to a local installation of Fiji (stock plugins should be fine):

KNIME--> Image Processing Plugin --> ImageJ1 Preferences --> ImageJ1 Plugin Directory


How to run the workflow:

1) You need 4 files to run this workflow:

	(a) segmentedfilteredImages_stripped.table --> A KNIME Table containing appropriate data for analysis. PLEASE DON'T REDISTRIBUTE THIS DATA. 
	(b) AllAntnotatedWells_RFLearner_GreenCTs.zip --> A RandomForest Learner Model
	(c) AllAnnotatedWells_RFLearner_RedCTs.zip --> A RandomForest Learner Model
	(d) AllAnnotatedWells_RFLearner_RedCTs.zip --> A RandomForest Learner Model

2) Once you have the above files, Open the workflow and right click on the "Configure Workflow" MetaNode to set the values for the above mentioned four inputs.

3) Change the location of the "Output Directory" to a local location on your workstation.

4) After making changes to the "Configure Workflow" MetaNode, Click the "OK" button.

5) Now, hit the "Double Arrow" on the KNIME GUI to execute the workflow.

6) The Workflow should save results (3 .csv files; 3 KNIME Tables .table; and 3 .svg files) in the following location based on the values you entered in the "Configure Workflow" Metanode.

e.g.; <OUTPUT Directory>/<Experiment Name>/<Username>/<YYYYMMMDD_HHMMSS>/


What is the issue:

This workflow has two Metanodes with "python scripting" that are executed per fluorescent channel (total of 6): "ShellAnalysisPython" and "CentriodGravityDistAreaShellNumOfCTs". These metanodes fail at random without much informatio
n about the failure. Re-executing the failed metanodes usually resolves the problem.

You can access these nodes by opening the following Metanodes 
SegmentCTsPerChannel (Green Probe) --> 2DFeaturesandDTValues 
SegmentCTsPerChannel (Red Probe) --> 2DFeaturesandDTValues 
SegmentCTsPerChannel (FarRed Probe) --> 2DFeaturesandDTValues 

Note: The python script in these nodes is doing fairly trivial task. It might be possible to convert the script to pure KNIME-KNIP nodes but having the ability to use Python packages with KNIME-KNIP opens up lot of possibilities.

How to crash the Python Scripting node(s) in the above listed Metanodes:

In the "Configure Workflow" Metanode: Set the following:
"Number of Nuclei Per Chunk" to 3000
"Number of Python Forks" to 8 (or whatever is the CPU count on your machine)


How to run this workflow in BATCH_MODE (ON LINUX):

/home/yyyy/Downloads/knime_3.2.1/knime -reset -nosave  -nosplash -application org.knime.product.KNIME_BATCH_APPLICATION -workflowFile="/home/gudlap/knip_python/HiTIF_CTs_2D_Analysis_CV7000_CT_Segmentation_Analysis_ForKNIPDebug.knwf"  -workflow.variable=outDirectoryvar,"/data/gudlap/ziad/161207-EXP14-15-05-66-04_20161207_123043/knime_ouput",String -workflow.variable=segmentedfilterednucleiktFname,"/data/gudlap/ziad/161207-EXP14-15-05-66-04_20161207_123043/req_files/exp14_segmentedfilteredImages_stripped.table",String -workflow.variable=usernameVar,"gudlap",String -workflow.variable=typeofCellsVar,"Exp14_40X",String -workflow.variable=numberOfNodesvar,42,int, -workflow.variable=numberOfFilesPerChunkvar,1000,int -workflow.variable=equidistantshellsNumber,5,int -workflow.variable=numberOfNodes4ImageJ,1,int -workflow.variable=csvoutputprefix,"AllWells",String -workflow.variable=equiAreashellsNumber,5,int -workflow.variable=NumberOfPythonForks,4,int -workflow.variable=greenCTRFLearnerZip,"/data/gudlap/ziad/161207-EXP14-15-05-66-04_20161207_123043/req_files/02152017/Exp14_AllAnnotatedWells_RFLearner_GreenCTs.zip",String -workflow.variable=farredCTRFLearnerZip,"/data/gudlap/ziad/161207-EXP14-15-05-66-04_20161207_123043/req_files/02152017/Exp14_AllAnnotatedWells_RFLearner_FarRedCTs.zip",String -workflow.variable=redCTRFLearnerZip,"/data/gudlap/ziad/161207-EXP14-15-05-66-04_20161207_123043/req_files/02152017/Exp14_AllAnnotatedWells_RFLearner_RedCTs.zip",String -preferences="/home/gudlap/knip_python/knime321_preferences.epf"
