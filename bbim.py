# -*- coding: utf-8 -*-
"""
Created on Wed Jan 27 15:59:12 2021

@author: al-abiad
"""
import matplotlib

matplotlib.use("Qt5Agg")

import matplotlib.pyplot as plt
import pandas as pd

from scipy import interpolate
from datetime import datetime, date, time, timedelta
from pampro import data_loading, Time_Series, Channel, channel_inference, triaxial_calibration
from scipy import signal,fft
from scipy.signal import find_peaks

import numpy as np
# Read the data - yields 1 channel per axis

path1="d:\\Users\\al-abiad\\Desktop\\BB-Bim\\test 2\\D_CA_Test1.CWA"
path2="d:\\Users\\al-abiad\\Desktop\\BB-Bim\\test 2\\G_CA_Test1.CWA"

#ts is the time series that contains channels 
ts1, header1 = data_loading.load(path1, "Axivity")
ts2, header2 = data_loading.load(path2, "Axivity")

x1, y1, z1 = ts1.get_channels(["X", "Y", "Z"])
x2, y2, z2 = ts2.get_channels(["X", "Y", "Z"])

#changing into seconds
time1=x1.timestamps
time2=x2.timestamps

# mattime=[datetime2matlabdn(i) for i in time]
# mattime2=[i.replace(",", ".") for i in mattime2]
# mattime2=[float(i) for i in mattime2 ]

timestamp1= np.array([i.timestamp()for i in time1]).astype('float64')
start1=timestamp1[0]
timestamp1=(timestamp1-timestamp1[0]).astype('float64')


timestamp2= np.array([i.timestamp()for i in time2]).astype('float64')
start2=timestamp2[0]
timestamp2=(timestamp2-timestamp2[0]).astype('float64')

# mattimedate2=[datenum_to_datetime(i) for i in mattime2]



x_ind1=x1.indices
x_time1=timestamp1

x_ind2=x2.indices
x_time2=timestamp2

f1 = interpolate.interp1d(x_ind1, x_time1,kind='linear',fill_value='extrapolate')
f2 = interpolate.interp1d(x_ind2, x_time2,kind='linear',fill_value='extrapolate')

x_newind1=np.arange(0,len(x1.data))
x_newind2=np.arange(0,len(x2.data))

new_time1=f1(x_newind1)#+start1

new_time2=f2(x_newind2)#+start2

new_time11 = [datetime.fromtimestamp(i) for i in new_time1]

new_time22 = [datetime.fromtimestamp(i) for i in new_time2]


data1 = {'Accx': x1.data,'Accy': y1.data,'Accz': z1.data}
signal1= pd.DataFrame(data1)
signal1.index=new_time1

data2 = {'Accx': x2.data,'Accy': y2.data,'Accz': z2.data}
signal2= pd.DataFrame(data2)
signal2.index=new_time2

#interpolate
matrix1=signal1
fs=50
t_t=np.linspace(0, matrix1.index[len(matrix1)-1], num=np.int((matrix1.index[len(matrix1)-1])*fs), endpoint=True,dtype=np.float32)
matrix1=matrix1.reindex(matrix1.index.union(t_t))
matrix1=matrix1.interpolate(method='linear', limit_direction='both', axis=0)
matrix1=matrix1[matrix1.index.isin(pd.Index(t_t))]
matrix1.index=np.around(matrix1.index.values.astype('float64'),decimals=4)
signal1_interp=matrix1

matrix1=signal2
fs=50
t_t=np.linspace(0, matrix1.index[len(matrix1)-1], num=np.int((matrix1.index[len(matrix1)-1])*fs), endpoint=True,dtype=np.float32)
matrix1=matrix1.reindex(matrix1.index.union(t_t))
matrix1=matrix1.interpolate(method='linear', limit_direction='both', axis=0)
matrix1=matrix1[matrix1.index.isin(pd.Index(t_t))]
matrix1.index=np.around(matrix1.index.values.astype('float64'),decimals=4)
signal2_interp=matrix1


signal1_interp.index=signal1_interp.index+start1
signal2_interp.index=signal2_interp.index+start2


new_index1= [datetime.fromtimestamp(i) for i in signal1_interp.index]

new_index2 = [datetime.fromtimestamp(i) for i in signal2_interp.index]

signal1_interp.index=new_index1
signal2_interp.index=new_index2


#truncate to be on same time

start1=signal1_interp.index[0]
start2=signal2_interp.index[0]

end1=signal1_interp.index[-1]
end2=signal2_interp.index[-1]

if start1>start2:
    if end1>end2:
        signal2_interp_trun=signal2_interp.truncate(before=start1)
        signal1_interp_trun=signal1_interp.truncate(after=end2)
    else:
        signal2_interp_trun=signal2_interp.truncate(before=start1,after=end1)
else:
    if end1>end2:
        signal1_interp_trun=signal1_interp.truncate(before=start2,after=end2)
    else:
       signal2_interp_trun=signal2_interp.truncate(after=end1)
       signal1_interp_trun=signal1_interp.truncate(before=start2)
        

signal2_interp_trun_align=signal2_interp_trun.iloc[-lag:len(signal2_interp_trun)]


# calculation norm 

x=signal2_interp_trun_align.iloc[:,0].values**2
y=signal2_interp_trun_align.iloc[:,1].values**2
z=signal2_interp_trun_align.iloc[:,2].values**2
m=x+y+z
#    m=np.sqrt(m)
mm=np.array([np.sqrt(i) for i in m])

signal2_interp_trun_align['Accm'] = mm 

x=signal1_interp_trun.iloc[:,0].values**2
y=signal1_interp_trun.iloc[:,1].values**2
z=signal1_interp_trun.iloc[:,2].values**2
m=x+y+z
#    m=np.sqrt(m)
mm=np.array([np.sqrt(i) for i in m])

signal1_interp_trun['Accm'] = mm 




plt.plot(signal2_interp_trun)

plt.plot(signal1_interp_trun)

plt.figure()
plt.plot(signal2['time'],signal2['Accy'])
plt.title("ACCy")
plt.figure()
plt.plot(signal2['time'],signal2['Accz'])
plt.title("ACCz")
plt.figure()
plt.plot(signal2['time'],signal2['Accx'])
plt.title("ACCx")

plt.plot(signal2['Accz'])
plt.plot(signal1['Accz'])









# finally didnt find the signal in the hand ... but could find align the signal because of the shape of 
# the vertical acceleration signal
text='Accz'
lag=np.argmax(signal.correlate(signal1_interp_trun[text],signal2_interp_trun[text]))
lagInd=np.arange(-np.max([len(signal2_interp_trun[text]),len(signal1_interp_trun[text])]),np.max([len(signal2_interp_trun[text]),len(signal1_interp_trun[text])]))
lag=lagInd[lag]
# lag=36100


sig1=signal1_interp_trun[text].iloc[-lag:len(signal1_interp_trun[text])]

sig2=signal2_interp_trun[text].iloc[-lag:len(signal2_interp_trun[text])]

sig1_index=np.arange(0,len(sig1))

sig2_index=np.arange(0,len(sig2))



plt.plot(sig2_index,sig2.values)

plt.plot(np.arange(0,len(signal2_interp_trun[text])),signal2_interp_trun[text].values)
plt.plot(np.arange(0,len(signal1_interp_trun[text])),signal1_interp_trun[text].values)
plt.title(text)







plt.plot(signal1['time'],signal1['Accy'])

t_t=np.linspace(0, timestamp[-1], num=len(timestamp)*120+120, endpoint=True,dtype=np.float32)


ax=xx.data
ay=yy.data
az=zz.data

data = {'Accx': ax,'Accy': ay,'Accz': az}
signal= pd.DataFrame(data)



timeseries=timeseries.reindex(timeseries.index.union(t_t))
timeseries=pd.Series(timestamp,)
#enlarging the array

def datetime2matlabdn(dt):
   mdn = dt + timedelta(days = 366)
   frac_seconds = (dt-datetime.datetime(dt.year,dt.month,dt.day,0,0,0)).seconds / (24.0 * 60.0 * 60.0)
   frac_microseconds = dt.microsecond / (24.0 * 60.0 * 60.0 * 1000000.0)
   return mdn.toordinal() + frac_seconds + frac_microseconds


def datenum_to_datetime(datenum):
    """
    Convert Matlab datenum into Python datetime.
    :param datenum: Date in datenum format
    :return:        Datetime object corresponding to datenum.
    """
    days = datenum % 1
    return datetime.fromordinal(int(datenum)) \
           + timedelta(days=days) \
           - timedelta(days=366)










for channel in ts:
    print(channel)

# chart = ts.draw(["X"], height=2)

xx, yy, zz = ts.get_channels(["X", "Y", "Z"])
ts.write_channels_to_file("3.csv")
# Autocalibrate the raw acceleration data
x, y, z, calibration_diagnostics = triaxial_calibration.calibrate(xx, yy, zz)

x.name
size=x.size
timeframe=x.timeframe
time_period=xx.time_period 
data=x.data
timestamps=xx.timestamps
xx.indices
x.annotations
x.draw_properties 
x.cached_indices 
x.timestamp_policy 
x.missing_value 

timestamp_seconds=[]
for i in timestamps:
    timestamp_seconds.append(time.mktime(i.timetuple()))

timestamp_seconds=np.array(timestamp_seconds)
timestamp_seconds=timestamp_seconds-timestamp_seconds[0]



# Autocalibrate the raw acceleration data
x, y, z, calibration_diagnostics = triaxial_calibration.calibrate(x, y, z)

# Infer some sample level information - Vector Magnitude (VM), Euclidean Norm Minus One (ENMO)
vm = channel_inference.infer_vector_magnitude(x, y, z)
enmo = channel_inference.infer_enmo(vm)


# Create a time series object and add channels to it
ts.add_channels([vm, enmo])

# Uncomment this line to write the raw data as CSV
#ts.write_channels_to_file("C:/Data/3.csv")

# Request some interesting statistics - mean of ENMO
stats = {"ENMO":[("generic", ["mean"])]}

# Get the above statistics on an hourly level - returned as channels
hourly_results = ts.piecewise_statistics(timedelta(hours=1), statistics=stats)

# Write the hourly analysis to a file
hourly_results.write_channels_to_file("example_output.csv")

# Visualise the hourly ENMO signal
hourly_results.draw([["ENMO_mean"]], file_target="example.png")

fs=50
fc=2
N=4
Wn =fc/(fs/2) # Cutoff frequency normalized 
B, A = signal.butter(N, Wn,'low', output='ba') 


y=signal2.copy()
for col in y:
    if col!='time':
        y[col]=signal.filtfilt(B, A, y[col].values) # fix
signal__filtered=y
