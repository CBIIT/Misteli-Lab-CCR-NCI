A) The attached production workflow(s) were mostly run on Linux (64-bit) compute node (Biowulf, HPC @ NIH).
   Compute node specs: 56-Cores/Threads (28-CPUs), 190GB RAM, 500GB SSD for KNIME-TEMP, and 4 Nvidia Kepler 80 GPUs (12 GB Graphics RAM each).

B) The workflow(s) are TESTED exclusively on KNIME 3.2.1. The workflow will MOST likely fail with KNIME 3.3.X release because of changes to the "Feature Calculator (Beta)" node in the KNIME-KNIP 3.3.x release. 

C) Before you execute this workflow please set the path to python executable with appropriate packages:

Python2.7.12 Setup for KNIME-KNIP (Version 3.2.1):

The python environment detailes we are using is provided in the following txt file (pip freeze):
[p27_packages_in_singularity.txt](https://github.com/CBIIT/Misteli-Lab-CCR-NCI/blob/master/Jowhar_SCA_2018/KNIME/KNIME_Config_Files/p27_packages_in_singularity.txt)

You can install the requirements using pip:
pip install --no-cache-dir -r p27_packages_in_singularity.txt


Set the KNIME Pereferences for `Path to Python Executable` to the `python` executable:
e.g.: /usr/bin/python

D) It also expected to point ImageJ1 preferences in KNIME to a local installation of Fiji (stock plugins should be fine):

KNIME--> Image Processing Plugin --> ImageJ1 Preferences --> ImageJ1 Plugin Directory


Notes: 
1) To run the workflows you might need to adapt the path to the deep learning model weights (.h5) and architecture files (.json). These are in [DeeplearningModels](https://github.com/CBIIT/Misteli-Lab-CCR-NCI/blob/master/Jowhar_SCA_2018/KNIME/DeeplearningModels) sub-folder.

2) The Random Forests Model (.zip) for filtering out mis-segmented nuclei is [here](https://github.com/CBIIT/Misteli-Lab-CCR-NCI/blob/master/Jowhar_SCA_2018/KNIME/RandomForestModels/NucleiRFLearner/DAPI_2DNuclei_RFLearner.zip).

3) KNIME Preferences we used for our set is here [knime321_preferences.epf](https://github.com/CBIIT/Misteli-Lab-CCR-NCI/blob/master/Jowhar_SCA_2018/KNIME/KNIME_Config_Files/knime321_preferences.epf)

4) KNIME Configuration captured from the KNIME -> Help--> Installation Details is also in this folder. See [knime321_configuration.txt](https://github.com/CBIIT/Misteli-Lab-CCR-NCI/blob/master/Jowhar_SCA_2018/KNIME/KNIME_Config_Files/knime321_configuration.txt)

