"""
# Author: Grant Morfitt
# Description: Sorts parsed data into dictionary of dataframes for ease of manipulation
# Output : fixedParsedData is dict that contains each file, and then a dictionary of each run which contains dataframes of selected variables

"""
import scipy.io
import numpy as np
import pandas as pd
import os

def ImportSimData(dataDir, arrayOfVariables):
    
    """
    dataDir must refer to folder for ONE(1) aircraft data
    arrayOfVariables contains an array of disired variables.
    output: fixedParsedData
    EX:
        A747Var = {"VVT_1_", "HGSPD_1_"}
        data = ImportSimData("SimFiles/737/",A747Var)
    """
    #----------Import Matlab Files-------------
    matlabFiles = []
    fixedParsedData = {"File": []}
    for file in os.listdir( dataDir ) : #Loop through files in directory
        matlabFiles.append( scipy.io.loadmat( dataDir+file ) )  #Import matlab file
        
        simplifiedSingleData = {"Scenario" : []} #Container to hold scenarios from each file
        
        for currentFile in matlabFiles: #Loop through files
            print("Loading file: " + str(len(matlabFiles)))
            data = currentFile
            for item in currentFile: #item refers to single scenario in the file
                    runData = {}    #temporary storage for current variable value
                                        
                    for currentVar in arrayOfVariables: #Sort through array of variables
                         if (item.startswith('__') != True) and (item.startswith('__version__') != True) and (item.startswith('__globals__') != True): #No headers
                            currentVal = data[item][currentVar] 
                            currentVal = np.concatenate(np.concatenate(np.concatenate(currentVal, axis=0)))
                            runData[currentVar] = currentVal #Save to dictionary the current variable and it's value
                            simplifiedSingleData[item] = pd.DataFrame(runData) #Adds scenario data into dataframe
            
        fixedParsedData[file] = simplifiedSingleData #Adds single file data to larger dictionary 
            
    
    return fixedParsedData;


A747Var = {"pilot_flying", "pilot_monitoring",}

data = ImportSimData("SimFiles/737/", A747Var)
