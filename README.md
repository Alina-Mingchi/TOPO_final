# TOPO_final
Semester Project final documentation Fall 2021

Here we just present the hierarchy of this repository. In each folder representing the 3 models, there are respective Readme files illustrating the usage of the model.

For this project, I have used mainly notebooks to perform the training, testing, and analysis. Since data have been separated in different folders, in order to run tasks for specific folder, typically uncommenting the respective lines are needed.

## Hierarchy of folders
- Data_preprocessing: This folder includes the raw data separated into EPFL_nadir, EPFL_oblique, comballaz_nadir, comballaz_oblique. Further there is the folder for simple geometry data that is used for futher analysis and has been reported in the Appendix of the report. There is also a data pre-processing notebook to calculate the euclidean distance.
- GSRPT_TOPO: This folder includes all the files related to the Guided Super-Resolution as Pixel-to-Pixel Transformation model. 
- MSG_TOPO: This folder includes all the files related to the Multi-Scale Guided convolutional network.
- PMBANet_TOPO: This folder includes all the files related to the Progressive Multi-Branch Aggregation Network.


## Dependences
The code supports Python 3.8
Pytorch is needed for the architecture of the neural networks.
Numpy, Scipy, Matplotlib, Imageio are also necessary.
For the GSRPT, there is an extra tricky (at least for me) library to install. For me, I have downloaded this prox_tv library and manually included in the file directory. According to system difference, there could be no issues for Linux system and/ or Windows system.


