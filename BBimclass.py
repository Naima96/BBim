# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 19:02:05 2021

@author: al-abiad
"""

import matplotlib
import pdb
matplotlib.use("Qt5Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import interpolate
from datetime import datetime, date, time, timedelta

from data_loading import load

from scipy import signal,fft

from Python_G_to_sec import main 

class BBim(object):
    
    def __init__(self,pathDroite,pathGauche,start_time="",end_time=""):
        """
        1 is right and 2 is left

        Returns
        -------
        None.

        """
        
        #---Read and interpolate periodic time---
        
        if start_time!="":
            time1,x_ind1,x1,y1,z1 = load(pathDroite,startreading=start_time,stopreading=end_time)
            time2,x_ind2,x2,y2,z2 = load(pathGauche,startreading=start_time,stopreading=end_time)
        
            # self.ts2=ts2
            # ts1, header1 = data_loading.load(pathDroite)
            # ts2, header2 = data_loading.load(pathGauche)
            
            # x1, y1, z1 = ts1.get_channels(["X", "Y", "Z"])
            # x2, y2, z2 = ts2.get_channels(["X", "Y", "Z"])
            
            # time1=x1.timestamps
            # time2=x2.timestamps
    
            
            timestamp1= np.array([i.timestamp()for i in time1]).astype('float64')
            start1=timestamp1[0]
    
            timestamp1=(timestamp1-timestamp1[0]).astype('float64')
    
    
            timestamp2= np.array([i.timestamp()for i in time2]).astype('float64')
            start2=timestamp2[0]
    
            timestamp2=(timestamp2-timestamp2[0]).astype('float64')
            
            # x_ind1=x1.indices
            x_time1=timestamp1
    
            # x_ind2=x2.indices
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
            
    
            
            #---interpolate to constant frequency---
            
            matrix1=signal1
            fs=50
            t_t=np.linspace(0, matrix1.index[len(matrix1)-1], num=np.int((matrix1.index[len(matrix1)-1])*fs), endpoint=True,dtype=np.float32)
            
            dd=matrix1.index.union(t_t).drop_duplicates(keep='first')
            matrix1=matrix1.reindex(dd)
            matrix1=matrix1.interpolate(method='linear', limit_direction='both', axis=0)
            matrix1=matrix1[matrix1.index.isin(pd.Index(t_t))]
            matrix1.index=np.around(matrix1.index.values.astype('float64'),decimals=4)
            signal1_interp=matrix1
            
            matrix1=signal2
            fs=50
            t_t=np.linspace(0, matrix1.index[len(matrix1)-1], num=np.int((matrix1.index[len(matrix1)-1])*fs), endpoint=True,dtype=np.float32)
            dd=matrix1.index.union(t_t).drop_duplicates(keep='first')
            matrix1=matrix1.reindex(dd)
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
    
            
            #---truncate/cut for the signals to start and stop at the same time---
            start1=signal1_interp.index[0]
            start2=signal2_interp.index[0]
            
    
            
            end1=signal1_interp.index[-1]
            end2=signal2_interp.index[-1]
    
            
            if start1>start2:
                if end1>end2:
                    print("cond1")
                    signal2_interp_trun=signal2_interp.truncate(before=start1)
                    signal1_interp_trun=signal1_interp.truncate(after=end2)
                else:
                    print("con2")
                    signal2_interp_trun=signal2_interp.truncate(before=start1,after=end1)
                    signal1_interp_trun=signal1_interp.iloc[:len(signal2_interp_trun),:]
            else:
                if end1>end2:
                    print("cond3")
                    signal1_interp_trun=signal1_interp.truncate(before=start2,after=end2)
                    signal2_interp_trun=signal2_interp
                else:
                    print("cond4")
                    signal2_interp_trun=signal2_interp.truncate(after=end1)
                    signal1_interp_trun=signal1_interp.truncate(before=start2)
            
            
            
            self.Gauche_signal=signal2_interp_trun
            self.Droite_signal=signal1_interp_trun
            
            # print(len(self.Gauche_signal))
            
            # print(len(self.Droite_signal))
            
        else:
            header1 = load(pathDroite,startreading="",stopreading="")
            header2 = load(pathGauche,startreading="",stopreading="")
            
            self.sdate="droite: "+ header1['logging_start_time'].strftime("%d/%m/%Y, %H:%M:%S")+ "----gauche: "+header2['logging_start_time'].strftime("%d/%m/%Y, %H:%M:%S")
            self.edate="droite: "+header1['logging_end_time'].strftime("%d/%m/%Y, %H:%M:%S")+ "----gauche: "+header2['logging_end_time'].strftime("%d/%m/%Y, %H:%M:%S")
            
        #---align both signals---
        
        # text='Accz'
        # lag=np.argmax(signal.correlate(signal1_interp_trun[text],signal2_interp_trun[text]))
        # lagInd=np.arange(-np.max([len(signal2_interp_trun[text]),len(signal1_interp_trun[text])]),np.max([len(signal2_interp_trun[text]),len(signal1_interp_trun[text])]))
        # lag=lagInd[lag]
        
        # lag=0 
        # if(lag<=0):
        #     signal2_interp_trun_align=signal2_interp_trun.iloc[-lag:len(signal2_interp_trun)]
        # else:
        #     print("error: I need to fix")
            
            
        
        



    
    def detect_date(self,pathDroite,pathGauche,start_time="",end_time=""):
        
        header1 = load(pathDroite,startreading=start_time,stopreading=end_time)
        header2 = load(pathGauche,startreading=start_time,stopreading=end_time)
        sdate=header1['logging_start_time'].strftime("%d/%m/%Y, %H:%M:%S")+header2['logging_start_time'].strftime("%d/%m/%Y, %H:%M:%S")
        edate=header1['logging_end_time'].strftime("%d/%m/%Y, %H:%M:%S")+header2['logging_end_time'].strftime("%d/%m/%Y, %H:%M:%S")
        # start_date=self.signal2_interp_trun.index[0]
        # syear=start_date.year
        # smonth=start_date.month
        # sday=start_date.day
        # sdate=[str(syear)+'-'+str(smonth)+'-'+str(sday)]
        
        # start_date=self.signal1_interp_trun.index[0]
        # syear=start_date.year
        # smonth=start_date.month
        # sday=start_date.day
        # sdate=sdate+str(syear)+'-'+str(smonth)+'-'+str(sday)
        
        # end_date=self.signal2_interp_trun.index[-1]
        
        # eyear=end_date.year
        # emonth=end_date.month
        # eday=end_date.day
        # edate=str(eyear)+'-'+str(emonth)+'-'+str(eday)
        
        # end_date=self.signal2_interp_trun.index[-1]
        
        # eyear=end_date.year
        # emonth=end_date.month
        # eday=end_date.day
        # edate=[edate+str(eyear)+'-'+str(emonth)+'-'+str(eday)]
        
        return sdate,edate
        
    def crop_signal(self,start_time="",end_time=""):
        #---crop HAI---
        if start_time != "":
            start_time=datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
            end_time=datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
        
            self.Gauche_signal=self.signal2_interp_trun.truncate(before=start_time,after=end_time)
            
            
            self.Droite_signal=self.signal1_interp_trun.truncate(before=start_time,after=end_time)
            

        
        
    def plot_signal(self):
        fig, ax = plt.subplots(2)
        color = 'tab:blue'
        ax[0].title.set_text("Gauche")
        ax[0].set_ylabel('Acc m/s\u00b2', color=color)
        ax[0].plot(self.Gauche_signal)
        
        color = 'tab:blue'
        ax[1].title.set_text("Droite")
        ax[1].set_ylabel('Acc m/s\u00b2', color=color)
        ax[1].set_xlabel('Time', color=color)
        ax[1].plot(self.Droite_signal)

        
    def Calculate_activity_count(self):
        # no danger of inf values
        
        self.Act_count_gauche=main(self.Gauche_signal)
        
        self.Act_count_droite=main(self.Droite_signal)
        
    def Calculate_vector_Magnitude(self):
        # calculation norm 
        # no danger of inf values
        
        #--Gauche---
        x=self.Act_count_gauche['axis1'].values**2
        y=self.Act_count_gauche['axis2'].values**2
        z=self.Act_count_gauche['axis3'].values**2
        m=x+y+z
        mm=np.array([np.sqrt(i) for i in m])
        self.Vect_mag_gauche = mm 
        #---Droite---
        x=self.Act_count_droite['axis1'].values**2
        y=self.Act_count_droite['axis2'].values**2
        z=self.Act_count_droite['axis3'].values**2
        m=x+y+z
        mm=np.array([np.sqrt(i) for i in m])
        
        self.Vect_mag_droite = mm 
        
        difference=len(self.Vect_mag_droite)-len(self.Vect_mag_gauche)
         
        if difference>0:
             self.Vect_mag_droite=self.Vect_mag_droite[:len(self.Vect_mag_droite)-difference]
             
        if difference<0:
             self.Vect_mag_gauche=self.Vect_mag_gauche[:len(self.Vect_mag_gauche)+difference]
        
            
        
        
    def Calculate_mean_median_VectorMagnitude(self,dominant_limb='gauche'):
        # no danger of inf values
        if dominant_limb=='gauche':
            self.Med_VM_dominant=np.median(self.Vect_mag_gauche)
            self.Med_VM_nondominant=np.median(self.Vect_mag_droite)
            self.Mean_VM_dominant=np.mean(self.Vect_mag_gauche)
            self.Mean_VM_nondominant=np.mean(self.Vect_mag_droite)
        else:
            self.Med_VM_nondominant=np.median(self.Vect_mag_gauche)
            self.Med_VM_dominant=np.median(self.Vect_mag_droite)
            
            self.Mean_VM_nondominant=np.mean(self.Vect_mag_gauche)
            self.Mean_VM_dominant=np.mean(self.Vect_mag_droite)
        
        
                
    def plt_vectmag(self):
        
        plt.figure()
        plt.title("Vector magnitude")
        plt.plot(self.Vect_mag_gauche,label="Gauche")
        plt.plot(self.Vect_mag_droite,label="Droite")
        plt.legend()
        
    def calculate_magnitude_ratio(self,dominant_limb='gauche',apply_filter=True):
        """
        if I am not using the dominant then mag ratio is infinity and this value is omitted 
        If I am not using both the dominant and non-dominant this value is omitted
        
        I dont know if I am using the non dominant while not using the dominant becaus
        it is zero anyway

        Parameters
        ----------
        dominant_limb : TYPE, optional
            DESCRIPTION. The default is 'Gauche'.

        Returns
        -------
        None.

        """
        N=5
        
        self.Vect_mag_droite_filtered=np.convolve(self.Vect_mag_droite, np.ones(N)/N, mode='valid')
        self.Vect_mag_gauche_filtered=np.convolve(self.Vect_mag_gauche, np.ones(N)/N, mode='valid')

        
        if dominant_limb=='gauche':
            # simply remove values which give infinity. this value is only calculated when dominant is moving.
            self.mag_ratio=np.divide(self.Vect_mag_droite+1, self.Vect_mag_gauche+1, out=np.zeros_like(self.Vect_mag_droite)+10000, where=self.Vect_mag_gauche!=0)
            self.mag_ratio=self.mag_ratio[np.where(self.mag_ratio!=10000)[0]]
            # self.mag_ratio=(self.Vect_mag_droite_filtered+1)/(self.Vect_mag_gauche_filtered+1)
            # self.use_ratio=np.divide(self.Vect_mag_droite+1, self.Vect_mag_gauche+1, out=np.zeros_like(self.Vect_mag_droite), where=self.Vect_mag_gauche!=0)
            self.mag_ratio=np.log(self.mag_ratio)
        else:
            self.mag_ratio=np.divide(self.Vect_mag_gauche+1, self.Vect_mag_droite+1, out=np.zeros_like(self.Vect_mag_gauche)+10000, where=self.Vect_mag_droite!=0)
            self.mag_ratio=self.mag_ratio[np.where(self.mag_ratio!=10000)[0]]
            self.mag_ratio=np.log(self.mag_ratio)
            
            
    def Calculate_mean_median_Mag_ratio(self):
        
        # there is a risk of been inf but now that we remove inf values it must be better
        self.Med_mag_ratio=np.median(self.mag_ratio)
        self.Mean_mag_ratio=np.mean(self.mag_ratio)
        
    def plot_magnitude_ratio(self):
        
        plt.figure()
        plt.title("Magnitude ratio")
        plt.plot(self.mag_ratio)
        
    def calculate_total_activity(self,vm_thresh=10,dominant_limb='gauche'):
        """
        calculate sum of seconds where activity counts is greater than 10 

        Returns
        -------
        None.

        """
        # no risk of been inf
        
        if dominant_limb=="gauche":
            self.dominant_total_activity= np.sum(self.Vect_mag_gauche>vm_thresh)
            self.nondominant_total_activity= np.sum(self.Vect_mag_droite>vm_thresh)
        else:
            self.nondominant_total_activity= np.sum(self.Vect_mag_gauche>vm_thresh)
            self.dominant_total_activity= np.sum(self.Vect_mag_droite>vm_thresh)
            
        
        print("The total activity or sum of seconds where activity count>10 of dominant hand is %d and of nondominant hand is %d"%(self.dominant_total_activity,self.nondominant_total_activity))
        
        
    def Calculate_percent_activity(self,vm_thresh=10,dominant_limb='gauche'):
        # no risk of inf
        self.percent_act_dominant=self.dominant_total_activity*100/len(self.Vect_mag_gauche)
        self.percent_act_nondominant=self.nondominant_total_activity*100/len(self.Vect_mag_gauche)


        
    def calculate_use_ratio(self,dominant="gauche"):
        # no risk of inf

        self.use_ratio=self.nondominant_total_activity/self.dominant_total_activity
        
        
        if dominant=="gauche":
            self.mag_use_ratio=np.sum(self.Vect_mag_droite)/np.sum(self.Vect_mag_gauche)
        else:
            self.mag_use_ratio=np.sum(self.Vect_mag_gauche)/np.sum(self.Vect_mag_droite)
            
        
        
        print("The use ratio is %f "%(self.use_ratio))

            
    def calculate_bilateral_magnitude(self):
        """
        The Bilateral Magnitude reflects the intensity of activity 
        across both UEs,and was calculated by summing the smoothed vector 
        magnitude of the nondominant and dominant UEs for each second of 
        activity. Bilateral Magnitude values of 0 indicate that no 
        activity occurred, and increasing Bilateral Magnitude values 
        indicate increasing intensity of bilateral UE activity

        Returns
        -------
        None.

        """
        #no risk of inf
        
        N=5
        
        self.Vect_mag_droite_filtered=np.convolve(self.Vect_mag_droite, np.ones(N)/N, mode='valid')
        self.Vect_mag_gauche_filtered=np.convolve(self.Vect_mag_gauche, np.ones(N)/N, mode='valid')

        self.bilateral_magnitude=self.Vect_mag_droite_filtered+self.Vect_mag_gauche_filtered
        
        
    def Calculate_mean_median_bilateral(self):
        #no risk of inf
        self.Med_bilateral=np.median(self.bilateral_magnitude)
        self.Mean_bilateral=np.mean(self.bilateral_magnitude)
        
    def plot_bilateral_magnitude(self):
        
        plt.figure()
        plt.title("bilateral magnitude")
        plt.plot(self.bilateral_magnitude)
        
        
    def perform_statistics(self):
        """
        Seconds when no activity in either
        extremity occurred (i.e. the Bilateral Magnitude was equal to zero)
        were removed for statistical analysis.
        
        When is bilateral magnitude counted as movement when it is zero?
        

        Returns
        -------
        None.

        """
        thresh=2
        self.bilateral_magnitude_remove_zero=self.bilateral_magnitude[(self.bilateral_magnitude >= thresh) | (self.bilateral_magnitude <= -thresh)]
        
        self.magnitude_ratio_remove_zero=self.use_ratio[(self.bilateral_magnitude >= thresh) | (self.bilateral_magnitude <= -thresh)]
        
        # bin_range = int((max(self.bilateral_magnitude_remove_zero)) - min(self.bilateral_magnitude_remove_zero))+1
        # plt.figure()
        # freq,bins=np.histogram(self.bilateral_magnitude_remove_zero, bins=bin_range)
        n_bm, bins_bm, patches= plt.hist(self.bilateral_magnitude_remove_zero, bins='auto')
        plt.grid(axis='y', alpha=0.75)
        plt.xlabel('Value')
        plt.ylabel('Frequency')
        med=np.median(self.bilateral_magnitude_remove_zero)
        plt.title('Bilateral magnitude med=%.2f'%(med))
        maxfreq = n_bm.max()
        # Set a clean upper y-axis limit.
        plt.ylim(ymax=np.ceil(maxfreq / 10) * 10 if maxfreq % 10 else maxfreq + 10)
                
        # bin_range = int((max(self.magnitude_ratio_remove_zero)) - min(self.magnitude_ratio_remove_zero))+1
        # plt.figure()
        # freq,bins=np.histogram(self.magnitude_ratio_remove_zero, bins=bin_range)
        n_mr, bins_mr, patches = plt.hist(self.magnitude_ratio_remove_zero, bins='auto')
        plt.grid(axis='y', alpha=0.75)
        plt.xlabel('Value')
        plt.ylabel('Frequency')
        
        med=np.median(self.magnitude_ratio_remove_zero)
        plt.title('Magnitude ratio med=%.2f'%(med))
        maxfreq = n_mr.max()
        # Set a clean upper y-axis limit.
        plt.ylim(ymax=np.ceil(maxfreq / 10) * 10 if maxfreq % 10 else maxfreq + 10)
           
        
        
    def Calculate_MAUI(self, dominant="gauche",vm_thresh=10):
        
        if dominant== "gauche":
            print("prefered hand is gauche?")
            Activity_count_dom=np.sum(self.Vect_mag_gauche[self.Vect_mag_droite<vm_thresh])
            Activity_count_nondom=np.sum(self.Vect_mag_droite[self.Vect_mag_gauche<vm_thresh])
            
            self.nonpref_moving_n_pref_notmoving=np.sum((self.Vect_mag_droite>=vm_thresh) & (self.Vect_mag_gauche<vm_thresh))
            self.pref_moving_n_nonpref_notmoving=np.sum((self.Vect_mag_gauche>=vm_thresh) & (self.Vect_mag_droite<vm_thresh))
            
            self.nonprefnotmoving=np.sum(self.Vect_mag_droite<vm_thresh)
            self.prefnotmoving=np.sum(self.Vect_mag_gauche<vm_thresh)
            
            self.pref_moving=self.dominant_total_activity
            self.nonpref_moving=self.nondominant_total_activity
            
            self.MAUI=Activity_count_nondom/Activity_count_dom

            
            print("gauche is dominant")
        else:
            Activity_count_dom=np.sum(self.Vect_mag_droite[self.Vect_mag_gauche<vm_thresh])
            Activity_count_nondom=np.sum(self.Vect_mag_gauche[self.Vect_mag_droite<vm_thresh])
            
            self.nonpref_moving_n_pref_notmoving=np.sum((self.Vect_mag_gauche>=vm_thresh) & (self.Vect_mag_droite<vm_thresh))
            self.pref_moving_n_nonpref_notmoving=np.sum((self.Vect_mag_droite>=vm_thresh) & (self.Vect_mag_gauche<vm_thresh))
            
            self.nonprefnotmoving=np.sum(self.Vect_mag_gauche<vm_thresh)
            self.prefnotmoving=np.sum(self.Vect_mag_droite<vm_thresh)
            
            self.pref_moving=self.dominant_total_activity
            self.nonpref_moving=self.nondominant_total_activity
            
            self.MAUI=Activity_count_nondom/Activity_count_dom

            print("droite is dominant")
            
            
            
            
        self.actprefhandzero=Activity_count_nondom/self.prefnotmoving
        self.actnonprefhandzero=Activity_count_dom/self.nonprefnotmoving

        self.nonpref_moving_n_pref_notmoving=self.nonpref_moving_n_pref_notmoving*100/len(self.Vect_mag_gauche)
        self.pref_moving_n_nonpref_notmoving=self.pref_moving_n_nonpref_notmoving*100/len(self.Vect_mag_gauche)
        
        self.prefnotmoving=self.prefnotmoving*100/len(self.Vect_mag_gauche)
        self.nonprefnotmoving=self.nonprefnotmoving*100/len(self.Vect_mag_gauche)
        
        print("The MAUI is %f "%(self.MAUI))
            
    def Calculate_BAUI(self, dominant="gauche",vm_thresh=10):
        
        if dominant=="gauche":
            print("prefered hand is gauche?")
            
            Activity_count_dom=np.sum(self.Vect_mag_gauche[self.Vect_mag_droite>vm_thresh])
            
            Activity_count_nondom=np.sum(self.Vect_mag_droite[self.Vect_mag_gauche>vm_thresh])
            
            self.bothmoving=np.sum((self.Vect_mag_gauche>vm_thresh) & (self.Vect_mag_droite>vm_thresh))
            
            self.BAUI=Activity_count_nondom/Activity_count_dom
            
        else:
            Activity_count_dom=np.sum(self.Vect_mag_droite[self.Vect_mag_gauche>vm_thresh])
            Activity_count_nondom=np.sum(self.Vect_mag_gauche[self.Vect_mag_droite>vm_thresh])
            
            self.bothmoving=np.sum((self.Vect_mag_gauche>=vm_thresh) & (self.Vect_mag_droite>=vm_thresh))
            # self.lenactnonprefhandnotzero=len(self.Vect_mag_droite[self.Vect_mag_gauche>10])
            
            self.BAUI=Activity_count_nondom/Activity_count_dom
        
        
        self.bothnotmoving=np.sum((self.Vect_mag_gauche<vm_thresh) & (self.Vect_mag_droite<vm_thresh))
        
        self.pref_moving=self.dominant_total_activity*100/len(self.Vect_mag_gauche)
        self.nonpref_moving=self.nondominant_total_activity*100/len(self.Vect_mag_gauche)
        
        self.actprefhandnotzero=Activity_count_nondom/self.pref_moving
        self.actnonprefhandnotzero=Activity_count_dom/self.nonpref_moving
        
        self.bothmoving=self.bothmoving*100/len(self.Vect_mag_gauche)
        
        self.bothnotmoving=self.bothnotmoving*100/len(self.Vect_mag_gauche)
        
        print("The BAUI is %f "%(self.BAUI))
        
        
    def Plot_Histo(self):
        f, ax = plt.subplots(1, 1)
        Vect_mag_droite_removezero=self.Vect_mag_droite[self.Vect_mag_droite!=0]
        Vect_mag_gauche_removezero=self.Vect_mag_gauche[self.Vect_mag_gauche!=0]
        
        histgauche,binns=np.histogram(Vect_mag_gauche_removezero,bins='auto')
        histdroite,_=np.histogram(Vect_mag_droite_removezero,bins=binns)

        step=8
        plt.bar(binns[:-1], histgauche, width=step, align="center", ec="k",label='Gauche')
        plt.bar(-binns[:-1][::-1], histdroite[::-1], width=step, align="center", ec="k",label='Droite')
        locs, labels = plt.xticks() 

        labelx = [int(i) for i in np.abs(locs)]
        plt.xticks(locs, labelx) 
        
        plt.text(0.1, 0.9,'UR= %.2f'%(self.use_ratio),
        horizontalalignment='center',
        verticalalignment='center',
        transform = ax.transAxes)
        
        plt.legend(loc='upper right')
        plt.show()
        
        
        
        
        
        
        
                
 
    
 
    
 
    
if __name__=="__main__":
    
    plt.close('all')
    pathDroite="d:\\Users\\al-abiad\\Desktop\\BB-Bim\\test 2\\D_CA_Test1.CWA"
    pathGauche="d:\\Users\\al-abiad\\Desktop\\BB-Bim\\test 2\\G_CA_Test1.CWA"
    
    
    # start_timee="11/02/2021 13:30:00"
    # end_timee="11/02/2021 13:42:00"
    start_timee="26/01/2021 13:38:00"
    end_timee="26/01/2021 13:52:00"
    # start_timee=""
    # end_timee=""
    #Gauche is the dominant limb
    
    bb=BBim(pathDroite,pathGauche,start_time=start_timee,end_time=end_timee)
    bb.plot_signal()
    
    # pdb.set_trace()
    bb.Calculate_activity_count()
    bb.Calculate_vector_Magnitude()
    bb.plt_vectmag()

    bb.calculate_total_activity()
    bb.calculate_magnitude_ratio()
    bb.plot_magnitude_ratio()
    # # bb.calculate_bilateral_magnitude()
    # # bb.plot_bilateral_magnitude()
    
    bb.calculate_use_ratio()
    bb.Calculate_BAUI()
    bb.Calculate_MAUI()
    # # bb.perform_statistics()
    bb.Plot_Histo()
    
    