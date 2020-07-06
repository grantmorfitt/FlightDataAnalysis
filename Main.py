"""
# Author: Grant Morfitt
# Description: Main file for data analysis
# Output : N/A

"""

from module_SimDataAnalysis import ImportSimData,EnergyMetric
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest

Var = {"G97S_DSP_YTSIMTM_F4_1_","G04_EOM_ALT_AGL_F8_1_", "L34A_ADC_TAS_F4_1_"}
#time, altitude, gs
 
data = ImportSimData("SimFiles/A330/",Var)

energy = {}

time = data['sim_data_pilot111.mat']['data_scen01_rep1']['G97S_DSP_YTSIMTM_F4_1_']
height = data['sim_data_pilot111.mat']['data_scen01_rep1']['G04_EOM_ALT_AGL_F8_1_']
velocity = data['sim_data_pilot111.mat']['data_scen01_rep1']['L34A_ADC_TAS_F4_1_']


for currentSample in range(len(time)):
    energy[currentSample] = EnergyMetric(height[currentSample],velocity[currentSample])
    print("Currently on: " + str(currentSample))
    
energy = pd.Series(energy)

slope = pd.Series(np.gradient(energy.values), energy.index, name='energy gradient')
df = pd.concat([energy.rename("energy"), slope], axis=1)



model = IsolationForest(n_estimators=50, max_samples='auto', contamination='auto',max_features=1.0)
model.fit(df[["energy gradient"]])
df['scores']=model.decision_function(df[['energy gradient']])
df['anomaly']=model.predict(df[['energy gradient']])


for currentSample in range(len(df)):
    if df['anomaly'][currentSample] == -1:
        print("ANOMALY. REMOVING")
        df = df.drop(currentSample, axis = 0)
        
        



















print("CODE DONE")
