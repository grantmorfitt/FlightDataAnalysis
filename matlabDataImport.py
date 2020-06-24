#-------------------------------------------
# Author: Grant Morfitt
# Description: Sorts parsed data into dictionary of dataframes for ease of maniupulation
# Output : fixedParsedData is dict that contains each file, and then a dictionary of each run which contains dataframes of selected variables

import scipy.io
import numpy as np
import pandas as pd
import os

#----------Import Matlab Files-------------
dataDir = "SimFiles/" #CHANGE TO FILE DIRECTORY OF SIM FILES
matlabFiles = []
fixedParsedData = {"File": []}

for file in os.listdir( dataDir ) : #Loop through files in directory
    matlabFiles.append( scipy.io.loadmat( dataDir+file ) )  #Import matlab file
    
    simplifiedSingleData = {"Scenario" : []} #Container to hold scenarios from each file
    
    for currentFile in matlabFiles: #Loop through 
        print(file)      
        data = currentFile
        
        for item in currentFile: #For (item) in total data set
        
            if (item != "__header__") and (item != "__version__") and (item != "__globals__"):    #Sort out headers
                
                #-----------Edit this jazz to change what variables get saved------------------------
                
                timeValue = (data[item]['G97S_DSP_YTSIMTM_F4_1_'])    #Structure['parent1']['variable1'] / Pulls value into array
                groundSpeed = (data[item]['G04_EOM_GSPEED_F8_1_'])    #Pulls current groundspeed variable for current scenario
                
                timeValue = np.concatenate(np.concatenate(np.concatenate(timeValue, axis=0))) #Converts to array
                groundSpeed = np.concatenate(np.concatenate(np.concatenate(groundSpeed, axis=0))) #Converts to array
        
                runData = {"Time": timeValue, "Ground Speed": groundSpeed}  #Creates a dictionary for this scenario/run
                
                #----------------------------------------------------------------------------------------
                
                
                simplifiedSingleData[item] = pd.DataFrame(runData) #Adds scenario data into dataframe
        
    fixedParsedData[file] = simplifiedSingleData #Adds single file data to larger dictionary 
    
    