# How to download and run the FDTD_3D_BioHeatSolver Converted code in your python ide of choice. 

## Steps: 
    1. If you have conda or python installed, open up your editor of choice and create a new folder/project.
    
    2. Create a virtual environment in your project folder. This is important because some of the pip packages 
    can be irritating and incompatible with other packages for some reason.
    
    3. Activate your virtual environment and install the following packages: 
        - numpy
        - matplotlib
        - scipy
        - tqdm (This is for progress bars to show up.)
    
    4. Either clone the github repository and open up the FDTD_3D_BioheatSolver-selected in the current workspace. 
    
    5. Or, download the experimental_TEMPS_func_run.py file and the Calc_TEMPS_v045_python.py file and place them 
    in your project folder.
    
    6. Run the experimental_TEMPS_func_run.py file.
    
    7. The code should run and produce the desired plot of the heating curve at the focal point of the model.