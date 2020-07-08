"""
# Author: Grant Morfitt
# Description: Main file for data analysis
# Output : N/A

"""

from module_SimDataAnalysis import ImportSimData,EnergyMetric,IsStable
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest

Var = {"G97S_DSP_YTSIMTM_F4_1_","G04_EOM_ALT_AGL_F8_1_", "G04_EOM_CAS_F8_1_", "G34_NAV_GS_DEVDDM_F4_1_","L34_NAV_LOC_DEVDDM_F4_1_","G04_EOM_VZ_F8_1_"}
#time, altitude, CAS

# GS DEV: G34_NAV_GS_DEVDDM_F4_1_ 
# LOC DEV: L34_NAV_LOC_DEVDDM_F4_1_ 
# "G04_EOM_VZ_F8_1_"
data = ImportSimData("SimFiles/A330/",Var)
energy = {}
stability = {}
actualFPM = {}
TAWSFpm = {}
time = data['sim_data_pilot111.mat']['data_scen01_rep1']['G97S_DSP_YTSIMTM_F4_1_']
height = data['sim_data_pilot111.mat']['data_scen01_rep1']['G04_EOM_ALT_AGL_F8_1_']
velocity = data['sim_data_pilot111.mat']['data_scen01_rep1']['G04_EOM_CAS_F8_1_']
gsDev = data['sim_data_pilot111.mat']['data_scen01_rep1']['G34_NAV_GS_DEVDDM_F4_1_']
locDev = data['sim_data_pilot111.mat']['data_scen01_rep1']['L34_NAV_LOC_DEVDDM_F4_1_']
descentFPM = data['sim_data_pilot111.mat']['data_scen01_rep1']['G04_EOM_VZ_F8_1_']

for currentSample in range(len(time)): 
    energy[currentSample] = EnergyMetric(height[currentSample],velocity[currentSample]) #Calculate energy metric
    
energy = pd.Series(energy)
slope = pd.Series(np.gradient(energy.values), energy.index, name='energy gradient')#calulate slope
df = pd.concat([energy.rename("energy"), slope], axis = 1) #Adds both to dataframe




#vref, altitude, airspeed, pitchAngle, gsDeviation, locDeviation
for currentSample in range(len(time)): #This calculates stability using IsStable function
    stability[currentSample],fpm= IsStable(75,height[currentSample],velocity[currentSample],descentFPM[currentSample],gsDev[currentSample],locDev[currentSample])
    actualFPM[currentSample] = fpm
    
stability = pd.Series(stability) #formats everything into dataframe
stability = stability.to_frame()
actualFPM = pd.Series(actualFPM)
actualFPM = actualFPM.to_frame()
height = height.to_frame()
velocity = velocity.to_frame()
gsDev = gsDev.to_frame()
locDev = locDev.to_frame()

df = pd.concat([stability.rename(columns = {0 : "stability"}),df],axis = 1) #Put values into dataframe
df = pd.concat([actualFPM.rename(columns = {0 : "FPM"}),df],axis = 1)
df = pd.concat([height,velocity,gsDev,locDev,df],axis = 1)






# #This is stuff for outlier detection for use later down the line
# model = IsolationForest(n_estimators=50, max_samples='auto', contamination='auto',max_features=1.0)
# model.fit(df[["energy gradient"]])
# df['scores']=model.decision_function(df[['energy gradient']])
# df['anomaly']=model.predict(df[['energy gradient']])


# # for currentSample in range(len(df)):
# #     if df['anomaly'][currentSample] == -1:
# #         print("ANOMALY. REMOVING")
# #         df = df.drop(currentSample, axis = 0)
        
        



















print("CODE DONE")
