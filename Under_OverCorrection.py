"""
# Author: Grant Morfitt
# Description: Analysis of research question #2, under/overcorrection on glidepath
# Output : N/A

"""


# Author: Grant Morfitt
# Description: EnergyMetric vs Stability analysis
# Output : N/A

from module_SimDataAnalysis import *
import numpy as np
import pandas as pd
import re


Var ={"G04_GRND_WOW_L1_1_", "G97S_DSP_YTSIMTM_F4_1_","G04_EOM_ALT_AGL_F8_1_", "G04_EOM_CAS_F8_1_", "G34_NAV_GS_DEVDDM_F4_1_","L34_NAV_LOC_DEVDDM_F4_1_","G04_EOM_VZ_F8_1_","O34A_RALT_ALT_F4_1_"}


data = ImportSimData("SimFiles/A330/",Var)

trimmedData = {}
numberOnOffApproach = {}
anData = None

for currentFile in data:
  
    del anData
    anData = {}
    for currentScen in data[currentFile]:
        
        
        print(currentScen)
        #collect the varaibles
        onGround = data[currentFile][currentScen]['G04_GRND_WOW_L1_1_']
        time = data[currentFile][currentScen]['G97S_DSP_YTSIMTM_F4_1_']
        radioAltitude = data[currentFile][currentScen]['O34A_RALT_ALT_F4_1_']
        velocity = data[currentFile][currentScen]['G04_EOM_CAS_F8_1_']
        gsDev = data[currentFile][currentScen]['G34_NAV_GS_DEVDDM_F4_1_']
        locDev = data[currentFile][currentScen]['L34_NAV_LOC_DEVDDM_F4_1_']
        altitudeAGL = data[currentFile][currentScen]['G04_EOM_ALT_AGL_F8_1_']
        onGround = data[currentFile][currentScen]['G04_GRND_WOW_L1_1_']
        #Formatting the datatables for input into larger dataframe    
        
        time = time.rename("Time")
        altitudeAGL = altitudeAGL.rename("Altitude AGL")
        onGround = onGround.rename("On Ground")
        velocity = velocity.rename("Velocity KCAS")
        gsDev = gsDev.rename("Glideslope Deviation")
        locDev = locDev.rename("Localizer Deviation")
        
        # gsDeviation, locDeviation, airspeed, vref
        #Calculate if on approach path or not
        appPath = []
        for currentSample in range(len(time)): #Check if on approach path
               appPath.append(OnApproachPath(gsDev[currentSample], locDev[currentSample], velocity[currentSample], 141))
             
        #Blah blah formatting
        altitudeAGL = altitudeAGL.to_frame()
        velocity = velocity.to_frame()
        gsDev = gsDev.to_frame()
        locDev = locDev.to_frame()
        onGround = onGround.to_frame()
        appPath = pd.Series(appPath,name = "On Approach Path")
        
        change = 0
        #Add to data for current scenario
        anData[currentScen] = pd.concat([time,altitudeAGL,velocity,gsDev,locDev,appPath, onGround],axis = 1) 
        
        for currentSample in range(len(time)):#Filter out onground data
            if onGround.iloc[currentSample][0] == -1: #This will be used to filter out onground data
                anData[currentScen].drop(currentSample,inplace = True)
                
                if currentSample !=0: #Make sure we aren't indexing zero..causes exception 
                    tempA = appPath.iloc[currentSample] #This code is going to calculate the change from 0-1 for on the approach path
                    tempB = appPath.iloc[currentSample-1]
                    diff =  tempA - tempB 
                    if diff != 0: #If there is a difference
                      change += 1 #Add 1 to the change count
                      del diff
                      del tempA
                      del tempB
        tempFile = re.findall(r'\d+',str(currentFile))[0] #We have to extract the current number
        tempScen = re.findall(r'\d+',str(currentScen))[0]
        tempRep =  re.findall(r'\d+',str(currentScen))[1]
        
        numberOnOffApproach[tempFile + "." + tempScen + "." + tempRep] = change #Add the change to the number of changes in the appraoch
        
        #These have to be cleared for each run to rewrite them
        del currentSample    
        del time
        del velocity
        del gsDev
        del locDev
        del altitudeAGL
        trimmedData[currentFile] = anData


tabletData = pd.read_csv("Experiment 1 Data/experiment1_tablet_data.csv") #import the tablet data

for i in range(len(tabletData)): #filter out monitoring pilot
    
        if tabletData["role"][i] == "Pilot Monitoring": 
            tabletData.drop(i,inplace = True)
       
        try:   #this allows us to skip this block in case the previous filter already dropped it
            if tabletData["sim_flown"][i] != "A330":
                tabletData.drop(i,inplace = True)
        except: 
            print("Error: Value just dropped")
            
    
            
#This is going to contain our tablet data + numberonOffApproach data
combinedTable = pd.DataFrame(columns = ['Pilot', 'Scenario','Repetition', 'Workload', 'Fatigue', 'Risk'])

for i,v in enumerate(numberOnOffApproach):
    currentPilot = int(v[0])
    currentScenario = int(str(v[1])[:2])
    currentRep = int(str(v[1])[3:])
  
    # key = "('" + str(currentPilot)"
    
    temp = tabletData.loc[tabletData['pilot_id'] == currentPilot] #Now we have to filter tablet data based on the current approach
    temp = temp.loc[temp['scenario'] == currentScenario]
    temp = temp.loc[temp['repetition'] == currentRep]
    
    workload = temp["workload"]
    fatigue = temp["fatigue"]
    risk = temp["risk"]
    
    # = (currentPilot,currentScenario,currentRep,workload,fatigue,risk,columns = ['Pilot', 'Scenario','Repetition', 'Workload', 'Fatigue', 'Risk'])
    tempData = ({"Pilot": currentPilot, "Scenario": currentScenario, "Repetition": currentRep, "Workload": workload,"Fatigue": fatigue, "Risk": risk})
    tempData = pd.DataFrame(tempData)

    combinedTable = combinedTable.append(tempData)
    


