"""
# Author: Grant Morfitt
# Description: Main file for data analysis
# Output : N/A

"""

from module_SimDataAnalysis import ImportSimData,EnergyMetric,IsStable,TrimA330Data
import numpy as np
import pandas as pd
#from sklearn.ensemble import IsolationForest
#import antigravity #haha

Var = {"G97S_DSP_YTSIMTM_F4_1_","G04_EOM_ALT_AGL_F8_1_", "G04_EOM_CAS_F8_1_", "G34_NAV_GS_DEVDDM_F4_1_","L34_NAV_LOC_DEVDDM_F4_1_","G04_EOM_VZ_F8_1_","O34A_RALT_ALT_F4_1_"}


data = ImportSimData("SimFiles/A330/",Var)
anData = {}

for currentFile in data:

    for currentScen in data[currentFile]:
        print(currentScen)
       
        time = data[currentFile][currentScen]['G97S_DSP_YTSIMTM_F4_1_']
        radioAltitude = data[currentFile][currentScen]['O34A_RALT_ALT_F4_1_']
        velocity = data[currentFile][currentScen]['G04_EOM_CAS_F8_1_']
        gsDev = data[currentFile][currentScen]['G34_NAV_GS_DEVDDM_F4_1_']
        locDev = data[currentFile][currentScen]['L34_NAV_LOC_DEVDDM_F4_1_']
        descentFPM = data[currentFile][currentScen]['G04_EOM_VZ_F8_1_']
        altitudeAGL = data[currentFile][currentScen]['G04_EOM_ALT_AGL_F8_1_']
        energy = {}
        stability = {}
        TAWS_actAlt= {}
        TAWS_act = {}
        TAWS_measured = {}
        
        
        #vref, radioAltitude, heightAGL, airspeed,descentFPM,gsDeviation,locDeviation
        
        for currentSample in range(len(time)): 
            energy[currentSample] = EnergyMetric(altitudeAGL[currentSample],velocity[currentSample]) #Calculate energy metric
            stability[currentSample],TAWS_calc,TAWS_measured = IsStable(141,radioAltitude[currentSample],altitudeAGL[currentSample],velocity[currentSample],descentFPM[currentSample],gsDev[currentSample],locDev[currentSample])
            
            TAWS_actAlt[currentSample] = TAWS_calc
            TAWS_act[currentSample] = TAWS_measured
            altitudeAGL[currentSample] = altitudeAGL[currentSample].round() #round the altitude numbers
            
            
        
        energy = pd.Series(energy)
        slope = pd.Series(np.gradient(energy.values), energy.index, name='energy gradient')#calulate slope
        energy = pd.concat([energy.rename("energy"), slope], axis = 1) #Adds both to dataframe
     
        #Formatting the datatables for input into larger dataframe    
        stability = pd.Series(stability)
        stability = stability.to_frame()
        stability = stability.rename(columns = {0 : "stability"})
        TAWS_actAlt = pd.Series(TAWS_actAlt)
        TAWS_actAlt = TAWS_actAlt.to_frame()
        TAWS_actAlt = TAWS_actAlt.rename(columns = {0 : "TAWS Activiation Altitude"})
        TAWS_act = pd.Series(TAWS_act)
        TAWS_act = TAWS_act.to_frame()
        TAWS_act = TAWS_act.rename(columns = {0 : "TAWS Activated"})
        descentFPM = descentFPM.to_frame()
        descentFPM = descentFPM.rename(columns = {0 : "Actual FPM"})
        altitudeAGL = altitudeAGL.to_frame()
        altitudeAGL = altitudeAGL.rename(columns = {0 : "Altitude AGL"})
        velocity = velocity.to_frame()
        gsDev = gsDev.to_frame()
        locDev = locDev.to_frame()
        descentFPM = descentFPM.rename(columns = {0 : "Descent FPM"})
        
        
        #Dump data into a dict
        anData["run: " + str(currentScen)] = pd.concat([time,descentFPM,TAWS_actAlt,TAWS_act,altitudeAGL,velocity,gsDev,locDev,stability,energy],axis = 1)
        
        #These have to be cleared for each run to rewrite them
        del stability
        del energy
        del time
        del radioAltitude
        del velocity
        del gsDev
        del locDev
        del descentFPM
        del altitudeAGL
        del TAWS_act
        

 #Now we have to trim the data based on altitude AGL as suggested by eugene
data = TrimA330Data(anData)


#Data is trimmed, we must calculate correlation between the two values 
temp= {}
corrMatrix = {}
totalValue = {"Run" : []} 
for currentSam in data:
    #print(dic[currentSam])
    currentRun = data[currentSam]
    stab = currentRun["stability"]
    ener = currentRun["energy gradient"]
    temp = pd.concat([stab,ener], axis = 1)
    temp = pd.DataFrame(temp,columns = ['stability', 'energy gradient'])
    
    corrMatrix[currentSam] = temp.corr()
    #corrMatrix.style.background_gradient(cmap='coolwarm')
    totalValue[currentSam] = corrMatrix[currentSam]['energy gradient']
    totalValue[currentSam] = totalValue[currentSam][0]
    

#now we need to average the dataset, first format out the values
data_items = totalValue.items()
totalValue = pd.DataFrame(data_items)
totalValue = totalValue[1]

result = []

#Sort out non integer values
for itemz in totalValue:
    if isinstance(itemz,float) == True or isinstance(itemz,int) == True:
       # if str(itemz) == "nan":
        #    itemz = 0.0
        if str(itemz) != "nan":
            result.append(itemz)
        
result = pd.DataFrame(result)

        

print("CODE DONE")












