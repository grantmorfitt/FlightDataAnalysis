"""
# Author: Grant Morfitt
# Description: File containing various functions for Simulator Data analysis
# Output : N/A

"""
import scipy.io
import numpy as np
import pandas as pd
import os
import math

def ImportSimData(dataDir, arrayOfVariables):
    """
     DESCRIPTION: Sorts parsed data into dictionary of dataframes for ease of manipulation
     INPUT: Datadir of folder, array containing disered variables
     OUTPUT: fixedParsedData is dict that contains each file, and then a dictionary of each run which contains dataframes of selected variables
     INFO:
            dataDir must refer to folder for ONE(1) aircraft data
            arrayOfVariables contains an array of disired variables.
            output: fixedParsedData
            EX:
                A747Var = {"VVT_1_", "HGSPD_1_"}
                data = ImportSimData("SimFiles/737/",A747Var)
    """
    #----------Import Matlab Files-------------
    matlabFiles = []
    fixedParsedData = {}
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
            
    print(str(len(matlabFiles)) + " FILES LOADED SUCESSFULLY")
    return fixedParsedData



def EnergyMetric(height, velocity):
    """
     DESCRIPTION: Calculates proposed energy metric for single time sample
     INPUT: Current height of aircraft, current velocity of aircraft
     OUTPUT: Float energy
         
    """
    energy = 0
    CONST_GRAVITY = 32.17405
    
    velocitySquared = pow(velocity,2)
    energy = height + velocitySquared/(2*CONST_GRAVITY)
    
    return energy

# def CalculateDescentFPM(airspeed,pitchAngle):
#     """
#     DESCRIPTION: Calculates aircraft FPM based on airspeed and pitchangle
#     INPUT: Airspeed, pitch angle in degrees
#     OUTPUT: Feet per minute of aircraft descent
    
#     """
#     FPM = 0
#     FPM = airspeed *(1/60) * 6080 * math.tan(pitchAngle)
#     return FPM

def IsStable(vref, radioAltitude, heightAGL, airspeed,descentFPM,gsDeviation,locDeviation):
    """
    DESCRIPTION: Calculates stability at time sample given input parameters
    INPUT: Vref for aircraft, radio altitude, height above ground, current airspeed(CAS), descent feet per minute, glideslope deviaiotn and localizer deviation
    OUTPUT: T/F of aircraft stability based on the metrics in the info section
    INFO: 
              #Airspeed: +0-10 vref
              #Glideslope: 1 dot
              #Localizer : 1 dot
              #ROD       : TAWS not activated
        ****WHEN ADDING NEW AIRCRAFT GS MUST BE TAKEN INTO CONSIDERATION****
    """
              
    TAWS = None
    isStable = None  #initialize variable
    clearance = None
    #FPM must be negative
    #radioAtltude > 284 <2450 = upper Clearance
    #radioAltitude < 284 > 10 lower Clearance ASSUMING FPM >1482
    
    TAWS = 0 #our default will be zero, the if statement will indicate a 1 if activated
    isStable = None  #initialize variable
    
    upperClearance = (-0.575*descentFPM) - 1645.235
    lowerClearance = (-1.202*descentFPM) - 1771
    
    if (radioAltitude < 2450.0) and (descentFPM > -7125): #TAWS Won't activate if radioAlt>2450ft
        if(radioAltitude > 284.0) and (descentFPM < -1710.0): #if the upper line
            if(radioAltitude < upperClearance): #if upperclearance line is greater, aka height AGL is less
                TAWS = 1
                clearance = upperClearance
        elif(radioAltitude < 284.0) and (descentFPM < -1482.0): #if lower boundary
            if (radioAltitude < lowerClearance):
                TAWS = 1
                clearance = lowerClearance
    
    if abs(airspeed-vref) <= 10 and abs(gsDeviation) <= 1 and abs(locDeviation) <= 1 and TAWS != 1:
        isStable = True    
    
    else:
        isStable = False
    

    return isStable, clearance ,TAWS

     

def TestStable(radioAltitude,descentFPM):
    #FPM must be negative
    #radioAtltude > 284 <2450 = upper Clearance
    #radioAltitude < 284 > 10 lower Clearance ASSUMING FPM >1482
    
    TAWS = 0 #our default will be zero, the if statement will indicate a 1 if activated
   # isStable = None  #initialize variable
    upperClearance = (-0.575*descentFPM) - 1645.235
    lowerClearance = (-1.202*descentFPM) - 1771
    
    if (radioAltitude < 2450.0) and (descentFPM > -7125): #TAWS Won't activate if radioAlt>2450ft
        if(radioAltitude > 284.0) and (descentFPM < -1710.0): #if the upper line
            if(radioAltitude < upperClearance): #if upperclearance line is greater, aka height AGL is less
                TAWS = 1

        elif(radioAltitude < 284.0) and (descentFPM < -1482.0): #if lower boundary
            if (radioAltitude < lowerClearance):
                TAWS = 1
                
            
        
    return radioAltitude,upperClearance,lowerClearance,TAWS
    #return isStable, yy_dtc,TAWS,zdev_calc,bias
 