# -*- coding: utf-8 -*-
"""
Created on Tue Mar  2 11:44:09 2021

@author: al-abiad
"""
import matplotlib.pyplot as plt
import os
from os import walk

import tkinter as tk
import pygubu
from tkinter import messagebox

from tkinter import *

from BBimclass import BBim

import numpy as np

from matplotlib.backends.backend_tkagg import ( FigureCanvasTkAgg, NavigationToolbar2Tk)# Implement the default Matplotlib key bindings.
from matplotlib.figure import Figure

import pandas as pd

CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
pickable_artists = []

class MyApplication:
    
    def __init__(self):
        #1: Create a builder
        self.builder = builder = pygubu.Builder()

        #2: Load an ui file
        builder.add_from_file(os.path.join(CURRENT_DIR, 'bbim_window.ui'))
        
        #3: Create the toplevel widget.
        self.mainwindow = builder.get_object('mainwindow')
        
        # Container for the matplotlib canvas and toolbar classes
        self.fcontainer1 = builder.get_object('fcontainer1')
        self.fcontainer2 = builder.get_object('fcontainer2')
        self.fcontainer3 = builder.get_object('fcontainer3')
        self.fcontainer4 = builder.get_object('fcontainer4')
        
        self.fcontainer11 = builder.get_object('fcontainer11')
        self.fcontainer21 = builder.get_object('fcontainer21')
        self.fcontainer31 = builder.get_object('fcontainer31')
        self.fcontainer41 = builder.get_object('fcontainer41')
        self.fcontainer51 = builder.get_object('fcontainer51')
        
        self.fcontainer12 = builder.get_object('fcontainer12')
        self.fcontainer22 = builder.get_object('fcontainer22')
        self.fcontainer32 = builder.get_object('fcontainer32')
        self.fcontainer42 = builder.get_object('fcontainer42')
        self.fcontainer52 = builder.get_object('fcontainer52')
        
        self.fcontainer13 = builder.get_object('fcontainer13')
        self.fcontainer23 = builder.get_object('fcontainer23')
        self.fcontainer33 = builder.get_object('fcontainer33')
        self.fcontainer43 = builder.get_object('fcontainer43')
        self.fcontainer53 = builder.get_object('fcontainer53')
        
        self.fcontainer14 = builder.get_object('fcontainer14')
        self.fcontainer24 = builder.get_object('fcontainer24')
        self.fcontainer34 = builder.get_object('fcontainer34')
        self.fcontainer44 = builder.get_object('fcontainer44')
        self.fcontainer54 = builder.get_object('fcontainer54')

        #histogram containers
        self.fcontainer5 = builder.get_object('fcontainer5')
        self.fcontainer6 = builder.get_object('fcontainer6')
        self.fcontainer7 = builder.get_object('fcontainer7')
        self.fcontainer8 = builder.get_object('fcontainer8')
        self.fcontainer9 = builder.get_object('fcontainer9')
        self.fcontainer10 = builder.get_object('fcontainer10')
        
        
        
        #treeview
        self.treeview=self.builder.get_object('myetv')
        
        #set filepathchooser
        self.filepath = builder.get_object('filepath')
        
        #%% get labels
        self.lbl_files=builder.get_object('lbl_files')
        self.lbl_useratio=builder.get_object('lbl_useratio')
        self.lbl_baui=builder.get_object('lbl_baui')
        self.lbl_maui=builder.get_object('lbl_maui')
        self.lbl_Dact_count=builder.get_object('lbl_Dact_count')
        self.lbl_Gact_count=builder.get_object('lbl_Gact_count')
        
        self.lbl_date_start=builder.get_object('lbl_date_start')
        self.lbl_date_end=builder.get_object('lbl_date_end')
        
        self.lbl_actprefhandzero=builder.get_object('lbl_actprefhandzero')
        self.lbl_actnonprefhandzero=builder.get_object('lbl_actnonprefhandzero')
        self.lbl_actprefhandnotzero=builder.get_object('lbl_actprefhandnotzero')
        self.lbl_actnonprefhandnotzero=builder.get_object('lbl_actnonprefhandnotzero')
        
        self.lbl_nonprefmoving=builder.get_object('lbl_nonprefmoving')
        self.lbl_prefmoving=builder.get_object('lbl_prefmoving')
        self.lbl_bothmoving=builder.get_object('lbl_bothmoving')
        
        self.lbl_useratio1=builder.get_object('lbl_useratio1')
        self.lbl_baui1=builder.get_object('lbl_baui1')
        self.lbl_maui1=builder.get_object('lbl_maui1')
        self.lbl_Dact_count1=builder.get_object('lbl_dact_count1')
        self.lbl_Gact_count1=builder.get_object('lbl_gact_count1')
        
        

        
        self.lbl_actprefhandzero1=builder.get_object('lbl_actprefhandzero1')
        self.lbl_actnonprefhandzero1=builder.get_object('lbl_actnonprefhandzero1')
        self.lbl_actprefhandnotzero1=builder.get_object('lbl_actprefhandnotzero1')
        self.lbl_actnonprefhandnotzero1=builder.get_object('lbl_actnonprefhandnotzero1')
        
        self.lbl_nonprefmoving1=builder.get_object('lbl_nonprefmoving1')
        self.lbl_prefmoving1=builder.get_object('lbl_prefmoving1')
        self.lbl_bothmoving1=builder.get_object('lbl_bothmoving1')
        
        self.lbl_useratio2=builder.get_object('lbl_useratio2')
        self.lbl_baui2=builder.get_object('lbl_baui2')
        self.lbl_maui2=builder.get_object('lbl_maui2')
        self.lbl_Dact_count2=builder.get_object('lbl_dact_count2')
        self.lbl_Gact_count2=builder.get_object('lbl_gact_count2')

        
        self.lbl_actprefhandzero2=builder.get_object('lbl_actprefhandzero2')
        self.lbl_actnonprefhandzero2=builder.get_object('lbl_actnonprefhandzero2')
        self.lbl_actprefhandnotzero2=builder.get_object('lbl_actprefhandnotzero2')
        self.lbl_actnonprefhandnotzero2=builder.get_object('lbl_actnonprefhandnotzero2')
        
        self.lbl_nonprefmoving2=builder.get_object('lbl_nonprefmoving2')
        self.lbl_prefmoving2=builder.get_object('lbl_prefmoving2')
        self.lbl_bothmoving2=builder.get_object('lbl_bothmoving2')
        
        self.lbl_useratio3=builder.get_object('lbl_useratio3')
        self.lbl_baui3=builder.get_object('lbl_baui3')
        self.lbl_maui3=builder.get_object('lbl_maui3')
        self.lbl_Dact_count3=builder.get_object('lbl_dact_count3')
        self.lbl_Gact_count3=builder.get_object('lbl_gact_count3')

        
        self.lbl_actprefhandzero3=builder.get_object('lbl_actprefhandzero3')
        self.lbl_actnonprefhandzero3=builder.get_object('lbl_actnonprefhandzero3')
        self.lbl_actprefhandnotzero3=builder.get_object('lbl_actprefhandnotzero3')
        self.lbl_actnonprefhandnotzero3=builder.get_object('lbl_actnonprefhandnotzero3')
        
        self.lbl_nonprefmoving3=builder.get_object('lbl_nonprefmoving3')
        self.lbl_prefmoving3=builder.get_object('lbl_prefmoving3')
        self.lbl_bothmoving3=builder.get_object('lbl_bothmoving3')
        
        self.lbl_useratio4=builder.get_object('lbl_useratio4')
        self.lbl_baui4=builder.get_object('lbl_baui4')
        self.lbl_maui4=builder.get_object('lbl_maui4')
        self.lbl_Dact_count4=builder.get_object('lbl_dact_count4')
        self.lbl_Gact_count4=builder.get_object('lbl_gact_count4')

        
        self.lbl_actprefhandzero4=builder.get_object('lbl_actprefhandzero4')
        self.lbl_actnonprefhandzero4=builder.get_object('lbl_actnonprefhandzero4')
        self.lbl_actprefhandnotzero4=builder.get_object('lbl_actprefhandnotzero4')
        self.lbl_actnonprefhandnotzero4=builder.get_object('lbl_actnonprefhandnotzero4')
        
        self.lbl_nonprefmoving4=builder.get_object('lbl_nonprefmoving4')
        self.lbl_prefmoving4=builder.get_object('lbl_prefmoving4')
        self.lbl_bothmoving4=builder.get_object('lbl_bothmoving4')
        
        self.lbl_useratio5=builder.get_object('lbl_useratio5')
        self.lbl_baui5=builder.get_object('lbl_baui5')
        self.lbl_maui5=builder.get_object('lbl_maui5')
        self.lbl_Dact_count5=builder.get_object('lbl_dact_count5')
        self.lbl_Gact_count5=builder.get_object('lbl_gact_count5')

        
        self.lbl_actprefhandzero5=builder.get_object('lbl_actprefhandzero5')
        self.lbl_actnonprefhandzero5=builder.get_object('lbl_actnonprefhandzero5')
        self.lbl_actprefhandnotzero5=builder.get_object('lbl_actprefhandnotzero5')
        self.lbl_actnonprefhandnotzero5=builder.get_object('lbl_actnonprefhandnotzero5')
        
        self.lbl_nonprefmoving5=builder.get_object('lbl_nonprefmoving5')
        self.lbl_prefmoving5=builder.get_object('lbl_prefmoving5')
        self.lbl_bothmoving5=builder.get_object('lbl_bothmoving5')
        

        #%% rest of the code
        #get entries
        self.ent_start= self.builder.get_object('ent_start')
        self.ent_stop = self.builder.get_object('ent_stop')
        self.pref_limb = self.builder.get_object('pref_limb')
        
        #buttons
        self.calculate=self.builder.get_object('btn_calculate')
        
        #calendar
        
        self.calendar=self.builder.get_object('calendarframe')
        
        #combobox
        self.file_combo = builder.get_object('combo_files')
        
        
        #scrollbar and canvas

        
        
        # Connect button callback
        builder.connect_callbacks(self)
        
        
    def on_path_changed(self, event=None):
        self.process_bbim=False
        print("you are in on path changed")
        self.path = self.filepath.cget('path')
        _, _, self.files = next(walk(self.path))
        cwa_files=[]
        
        for f in self.files:
            if f.endswith(".CWA"):
                cwa_files.append(f)
                
                
        files=[f for f in cwa_files if f.find("D_")!=-1]

        self.file_combo.config(values=files)


    
    def on_file_selected(self,event=None):
        testdroite=self.file_combo.get()
        
        testgauche="G_"+testdroite[2:]
        
        self.files=[testdroite,testgauche]
        
        self.lbl_files.configure(text = 'The files are %s and %s'%(self.files[0],self.files[1]))

        
    def select_date(self,event=None):
        print("in select date")
        dt=self.calendar.selection
        
        date=dt.strftime('%d/%m/%Y %H:%M:%S')
        
        print(date)
        
        self.ent_start.get()

        self.ent_stop.get()
        
        self.ent_start.delete(0,"end")
        self.ent_start.insert(0,date)
        self.ent_stop.delete(0,"end")
        self.ent_stop.insert(0,date)
        

        

        
        
    def Calculate_everything(self, event=None):
        print("Calculatingg....")
        
        
        if self.files[0].find("D_") != -1:
            print("make sure that the file %s is Droite" %(self.files[0]))
            pathDroite=os.path.join(self.path, self.files[0])
            pathGauche=os.path.join(self.path, self.files[1])
        else:
            print("make sure that the file %s is Gauche"%(self.files[0]))
            pathDroite=os.path.join(self.path, self.files[1])
            pathGauche=os.path.join(self.path, self.files[0])
            
        start_timees=self.ent_start.get()
        end_timees=self.ent_stop.get()
        
        start_timee=start_timees.split(',')
        
        end_timee=end_timees.split(',')
        
        if len(start_timee)!=len(end_timee):
            print("errorr in length")
        
        
        pref_hand=self.pref_limb.get()
        print(pref_hand)
        
        list_results=[]
        
        for i in range(0,len(start_timee)):
            print("interpolating-->cutting")
            self.bb=BBim(pathDroite,pathGauche,start_time=start_timee[i],end_time=end_timee[i])
            print("Done interpolating-->cutting")
    
            print("ploting signals")
            
            self.plot_signal(i)
            
            print("done ploting signals")
            
            print("calculating activity counts")
            
            self.bb.Calculate_activity_count()
            
            print("calculating Vector magnitude")
            
            self.bb.Calculate_vector_Magnitude()
            
            print("plotting vector magnitude")
            
            self.plot_vectormagnitude(i)
            
            print("calculating total activity")
            self.bb.calculate_total_activity()
            
            print("Calculating magnitude ratio")
            
            self.bb.calculate_magnitude_ratio(dominant_limb=pref_hand)
            
            print("ploting magnitude ratio")
            
            self.plot_magnituderatio(i)
            
            print("calculate Bilateral magnitude")
            
            self.bb.calculate_bilateral_magnitude()
            
            print("plot Bilateral magnitude")
            
            self.plot_bilateralmagnitude(i)
            
            print("calculating use ratio, Baui, Maui")
            
            self.bb.calculate_use_ratio(dominant=pref_hand)
            self.bb.Calculate_BAUI(dominant=pref_hand)
            self.bb.Calculate_MAUI(dominant=pref_hand)
            
            print("ploting histogram")
            
            self.plot_histo(i)
            
            list_results.append([start_timee[i],end_timee[i],'%.2f '%(self.bb.use_ratio),'%.2f'%(self.bb.MAUI),
                                '%.2f'%(self.bb.BAUI),'%d activities'%(self.bb.Droite_total_activity),
                                '%d activities'%(self.bb.Gauche_total_activity),'%.2f '%(self.bb.actprefhandzero),
                                '%.2f '%(self.bb.actnonprefhandzero),'%.2f '%(self.bb.actprefhandnotzero),
                                '%.2f '%(self.bb.actnonprefhandnotzero),'%.2f '%(self.bb.nonprefmoving),
                                '%.2f '%(self.bb.prefmoving),'%.2f '%(self.bb.bothmoving)])
            #%% conditions for labels
            if i==0:
                self.lbl_useratio.configure(text ='%.2f '%(self.bb.use_ratio))
                self.lbl_maui.configure(text ='%.2f'%(self.bb.MAUI))
                self.lbl_baui.configure(text ='%.2f'%(self.bb.BAUI))
                self.lbl_Dact_count.configure(text ='%d activities'%(self.bb.Droite_total_activity))
                self.lbl_Gact_count.configure(text ='%d activities'%(self.bb.Gauche_total_activity))
                
                self.lbl_actprefhandzero.configure(text ='%.2f '%(self.bb.actprefhandzero))
                self.lbl_actnonprefhandzero.configure(text ='%.2f '%(self.bb.actnonprefhandzero))
                self.lbl_actprefhandnotzero.configure(text ='%.2f '%(self.bb.actprefhandnotzero))
                self.lbl_actnonprefhandnotzero.configure(text ='%.2f '%(self.bb.actnonprefhandnotzero))
                
                self.lbl_nonprefmoving.configure(text ='%.2f '%(self.bb.nonprefmoving))
                self.lbl_prefmoving.configure(text ='%.2f '%(self.bb.prefmoving))
                self.lbl_bothmoving.configure(text ='%.2f '%(self.bb.bothmoving))

            if i==1:
                
                self.lbl_useratio1.configure(text ='%.2f '%(self.bb.use_ratio))
                self.lbl_maui1.configure(text ='%.2f'%(self.bb.MAUI))
                self.lbl_baui1.configure(text ='%.2f'%(self.bb.BAUI))
                self.lbl_Dact_count1.configure(text ='%d activities'%(self.bb.Droite_total_activity))
                self.lbl_Gact_count1.configure(text ='%d activities'%(self.bb.Gauche_total_activity))
                
                self.lbl_actprefhandzero1.configure(text ='%.2f '%(self.bb.actprefhandzero))
                self.lbl_actnonprefhandzero1.configure(text ='%.2f '%(self.bb.actnonprefhandzero))
                self.lbl_actprefhandnotzero1.configure(text ='%.2f '%(self.bb.actprefhandnotzero))
                self.lbl_actnonprefhandnotzero1.configure(text ='%.2f '%(self.bb.actnonprefhandnotzero))
                
                self.lbl_nonprefmoving1.configure(text ='%.2f '%(self.bb.nonprefmoving))
                self.lbl_prefmoving1.configure(text ='%.2f '%(self.bb.prefmoving))
                self.lbl_bothmoving1.configure(text ='%.2f '%(self.bb.bothmoving))
                
            if i==2:
                
                self.lbl_useratio2.configure(text ='%.2f '%(self.bb.use_ratio))
                self.lbl_maui2.configure(text ='%.2f'%(self.bb.MAUI))
                self.lbl_baui2.configure(text ='%.2f'%(self.bb.BAUI))
                self.lbl_Dact_count2.configure(text ='%d activities'%(self.bb.Droite_total_activity))
                self.lbl_Gact_count2.configure(text ='%d activities'%(self.bb.Gauche_total_activity))
                
                self.lbl_actprefhandzero2.configure(text ='%.2f '%(self.bb.actprefhandzero))
                self.lbl_actnonprefhandzero2.configure(text ='%.2f '%(self.bb.actnonprefhandzero))
                self.lbl_actprefhandnotzero2.configure(text ='%.2f '%(self.bb.actprefhandnotzero))
                self.lbl_actnonprefhandnotzero2.configure(text ='%.2f '%(self.bb.actnonprefhandnotzero))
                
                self.lbl_nonprefmoving2.configure(text ='%.2f '%(self.bb.nonprefmoving))
                self.lbl_prefmoving2.configure(text ='%.2f '%(self.bb.prefmoving))
                self.lbl_bothmoving2.configure(text ='%.2f '%(self.bb.bothmoving))
                
            if i==3:
                
                self.lbl_useratio3.configure(text ='%.2f '%(self.bb.use_ratio))
                self.lbl_maui3.configure(text ='%.2f'%(self.bb.MAUI))
                self.lbl_baui3.configure(text ='%.2f'%(self.bb.BAUI))
                self.lbl_Dact_count3.configure(text ='%d activities'%(self.bb.Droite_total_activity))
                self.lbl_Gact_count3.configure(text ='%d activities'%(self.bb.Gauche_total_activity))
                
                self.lbl_actprefhandzero3.configure(text ='%.2f '%(self.bb.actprefhandzero))
                self.lbl_actnonprefhandzero3.configure(text ='%.2f '%(self.bb.actnonprefhandzero))
                self.lbl_actprefhandnotzero3.configure(text ='%.2f '%(self.bb.actprefhandnotzero))
                self.lbl_actnonprefhandnotzero3.configure(text ='%.2f '%(self.bb.actnonprefhandnotzero))
                
                self.lbl_nonprefmoving3.configure(text ='%.2f '%(self.bb.nonprefmoving))
                self.lbl_prefmoving3.configure(text ='%.2f '%(self.bb.prefmoving))
                self.lbl_bothmoving3.configure(text ='%.2f '%(self.bb.bothmoving))

            if i==4:
                
                self.lbl_useratio4.configure(text ='%.2f '%(self.bb.use_ratio))
                self.lbl_maui4.configure(text ='%.2f'%(self.bb.MAUI))
                self.lbl_baui4.configure(text ='%.2f'%(self.bb.BAUI))
                self.lbl_Dact_count4.configure(text ='%d activities'%(self.bb.Droite_total_activity))
                self.lbl_Gact_count4.configure(text ='%d activities'%(self.bb.Gauche_total_activity))
                
                self.lbl_actprefhandzero4.configure(text ='%.2f '%(self.bb.actprefhandzero))
                self.lbl_actnonprefhandzero4.configure(text ='%.2f '%(self.bb.actnonprefhandzero))
                self.lbl_actprefhandnotzero4.configure(text ='%.2f '%(self.bb.actprefhandnotzero))
                self.lbl_actnonprefhandnotzero4.configure(text ='%.2f '%(self.bb.actnonprefhandnotzero))
                
                self.lbl_nonprefmoving4.configure(text ='%.2f '%(self.bb.nonprefmoving))
                self.lbl_prefmoving4.configure(text ='%.2f '%(self.bb.prefmoving))
                self.lbl_bothmoving4.configure(text ='%.2f '%(self.bb.bothmoving))
                
            if i==5:
                
                self.lbl_useratio5.configure(text ='%.2f '%(self.bb.use_ratio))
                self.lbl_maui5.configure(text ='%.2f'%(self.bb.MAUI))
                self.lbl_baui5.configure(text ='%.2f'%(self.bb.BAUI))
                self.lbl_Dact_count5.configure(text ='%d activities'%(self.bb.Droite_total_activity))
                self.lbl_Gact_count5.configure(text ='%d activities'%(self.bb.Gauche_total_activity))
                
                self.lbl_actprefhandzero5.configure(text ='%.2f '%(self.bb.actprefhandzero))
                self.lbl_actnonprefhandzero5.configure(text ='%.2f '%(self.bb.actnonprefhandzero))
                self.lbl_actprefhandnotzero5.configure(text ='%.2f '%(self.bb.actprefhandnotzero))
                self.lbl_actnonprefhandnotzero5.configure(text ='%.2f '%(self.bb.actnonprefhandnotzero))
                
                self.lbl_nonprefmoving5.configure(text ='%.2f '%(self.bb.nonprefmoving))
                self.lbl_prefmoving5.configure(text ='%.2f '%(self.bb.prefmoving))
                self.lbl_bothmoving5.configure(text ='%.2f '%(self.bb.bothmoving))
        
        for d in list_results:
            self.treeview.insert('', tk.END, values=d)
                
             #%% rest of the code  
        
        
    def Detect_dates(self, event=None):
        print("detecting dates...")
        if self.files[0].find("D_") != -1:
            print("make sure that the file %s is Droite" %(self.files[0]))
            pathDroite=os.path.join(self.path, self.files[0])
            pathGauche=os.path.join(self.path, self.files[1])
        else:
            print("make sure that the file %s is Gauche"%(self.files[0]))
            pathDroite=os.path.join(self.path, self.files[1])
            pathGauche=os.path.join(self.path, self.files[0])

        self.bb=BBim(pathDroite,pathGauche,start_time="",end_time="")
        
        
        
        self.lbl_date_start.configure(text =self.bb.sdate)
        self.lbl_date_end.configure(text =self.bb.edate)
        print("Done")
        
    def plot_signal(self,i):
        
        if i==0:
            self.figure1 = Figure(figsize=(5, 4), dpi=100)
            self.canvas1 = FigureCanvasTkAgg(self.figure1, master=self.fcontainer1)
            self.canvas1.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
            self.toolbar = NavigationToolbar2Tk(self.canvas1, self.fcontainer1)
            self.toolbar.update()
            self.canvas1._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
            
    
            color = 'tab:blue'
           
            b = self.figure1.add_subplot(211)
                
            b.plot(self.bb.Gauche_signal,zorder=1)
            b.set_ylabel('Acc m/s\u00b2', color=color)
            b.title.set_text("Gauche")
            b.set_xticks([])
            self.canvas1.draw()
            
            a = self.figure1.add_subplot(212)
                
            a.plot(self.bb.Droite_signal,zorder=1)
            a.set_ylabel('Acc m/s\u00b2', color=color)
            a.set_xlabel('Time', color=color)
            a.title.set_text("Droite")
            self.canvas1.draw()
            
        if i==1:
            self.figure11 = Figure(figsize=(5, 4), dpi=100)
            self.canvas11 = FigureCanvasTkAgg(self.figure11, master=self.fcontainer11)
            self.canvas11.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
            self.toolbar11 = NavigationToolbar2Tk(self.canvas11, self.fcontainer11)
            self.toolbar11.update()
            self.canvas11._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
            
    
            color = 'tab:blue'
           
            b = self.figure11.add_subplot(211)
                
            b.plot(self.bb.Gauche_signal,zorder=1)
            b.set_ylabel('Acc m/s\u00b2', color=color)
            b.title.set_text("Gauche")
            b.set_xticks([])
            self.canvas11.draw()
            
            a = self.figure11.add_subplot(212)
                
            a.plot(self.bb.Droite_signal,zorder=1)
            a.set_ylabel('Acc m/s\u00b2', color=color)
            a.set_xlabel('Time', color=color)
            a.title.set_text("Droite")
            self.canvas11.draw()
            
        if i==2:
            self.figure21 = Figure(figsize=(5, 4), dpi=100)
            self.canvas21 = FigureCanvasTkAgg(self.figure21, master=self.fcontainer21)
            self.canvas21.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
            self.toolbar21 = NavigationToolbar2Tk(self.canvas21, self.fcontainer21)
            self.toolbar21.update()
            self.canvas21._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
            
    
            color = 'tab:blue'
           
            b = self.figure21.add_subplot(211)
                
            b.plot(self.bb.Gauche_signal,zorder=1)
            b.set_ylabel('Acc m/s\u00b2', color=color)
            b.title.set_text("Gauche")
            b.set_xticks([])
            self.canvas21.draw()
            
            a = self.figure21.add_subplot(212)
                
            a.plot(self.bb.Droite_signal,zorder=1)
            a.set_ylabel('Acc m/s\u00b2', color=color)
            a.set_xlabel('Time', color=color)
            a.title.set_text("Droite")
            self.canvas21.draw()
            
        if i==3:
            self.figure31 = Figure(figsize=(5, 4), dpi=100)
            self.canvas31 = FigureCanvasTkAgg(self.figure31, master=self.fcontainer31)
            self.canvas31.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
            self.toolbar31 = NavigationToolbar2Tk(self.canvas31, self.fcontainer31)
            self.toolbar31.update()
            self.canvas31._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
            
    
            color = 'tab:blue'
           
            b = self.figure31.add_subplot(211)
                
            b.plot(self.bb.Gauche_signal,zorder=1)
            b.set_ylabel('Acc m/s\u00b2', color=color)
            b.title.set_text("Gauche")
            b.set_xticks([])
            self.canvas31.draw()
            
            a = self.figure31.add_subplot(212)
                
            a.plot(self.bb.Droite_signal,zorder=1)
            a.set_ylabel('Acc m/s\u00b2', color=color)
            a.set_xlabel('Time', color=color)
            a.title.set_text("Droite")
            self.canvas31.draw()
            
        if i==4:
            self.figure41 = Figure(figsize=(5, 4), dpi=100)
            self.canvas41 = FigureCanvasTkAgg(self.figure41, master=self.fcontainer41)
            self.canvas41.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
            self.toolbar41 = NavigationToolbar2Tk(self.canvas41, self.fcontainer41)
            self.toolbar41.update()
            self.canvas41._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
            
    
            color = 'tab:blue'
           
            b = self.figure41.add_subplot(211)
                
            b.plot(self.bb.Gauche_signal,zorder=1)
            b.set_ylabel('Acc m/s\u00b2', color=color)
            b.title.set_text("Gauche")
            b.set_xticks([])
            self.canvas41.draw()
            
            a = self.figure41.add_subplot(212)
                
            a.plot(self.bb.Droite_signal,zorder=1)
            a.set_ylabel('Acc m/s\u00b2', color=color)
            a.set_xlabel('Time', color=color)
            a.title.set_text("Droite")
            self.canvas41.draw()
            
            
        if i==5:
            self.figure51 = Figure(figsize=(5, 4), dpi=100)
            self.canvas51 = FigureCanvasTkAgg(self.figure51, master=self.fcontainer51)
            self.canvas51.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
            self.toolbar51 = NavigationToolbar2Tk(self.canvas51, self.fcontainer51)
            self.toolbar51.update()
            self.canvas51._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
            
    
            color = 'tab:blue'
           
            b = self.figure51.add_subplot(211)
                
            b.plot(self.bb.Gauche_signal,zorder=1)
            b.set_ylabel('Acc m/s\u00b2', color=color)
            b.title.set_text("Gauche")
            b.set_xticks([])
            self.canvas51.draw()
            
            a = self.figure51.add_subplot(212)
                
            a.plot(self.bb.Droite_signal,zorder=1)
            a.set_ylabel('Acc m/s\u00b2', color=color)
            a.set_xlabel('Time', color=color)
            a.title.set_text("Droite")
            self.canvas51.draw()
        
        
    def plot_vectormagnitude(self,i):

         if i==0:
            self.figure2 = Figure(figsize=(5, 4), dpi=100)
            self.canvas2 = FigureCanvasTkAgg(self.figure2, master=self.fcontainer2)
            self.canvas2.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
            self.toolbar = NavigationToolbar2Tk(self.canvas2, self.fcontainer2)
            self.toolbar.update()
            self.canvas2._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
            color = 'tab:blue'
            b = self.figure2.add_subplot(111)
            b.title.set_text("Vector magnitude")
            b.set_ylabel('Activity counts', color=color)
            b.plot(self.bb.Vect_mag_gauche,label="Gauche")
            b.plot(self.bb.Vect_mag_droite,label="Droite")
            plt.legend()
            self.canvas2.draw()
            
         if i==1:
            self.figure12 = Figure(figsize=(5, 4), dpi=100)
            self.canvas12 = FigureCanvasTkAgg(self.figure12, master=self.fcontainer12)
            self.canvas12.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
            self.toolbar12 = NavigationToolbar2Tk(self.canvas12, self.fcontainer12)
            self.toolbar12.update()
            self.canvas12._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
  
            color = 'tab:blue'
            b = self.figure12.add_subplot(111)
            b.title.set_text("Vector magnitude")
            b.set_ylabel('Activity counts', color=color)
            b.plot(self.bb.Vect_mag_gauche,label="Gauche")
            b.plot(self.bb.Vect_mag_droite,label="Droite")
            plt.legend()
            self.canvas12.draw()
            
         if i==2:
            self.figure22 = Figure(figsize=(5, 4), dpi=100)
            self.canvas22 = FigureCanvasTkAgg(self.figure22, master=self.fcontainer22)
            self.canvas22.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
            self.toolbar22 = NavigationToolbar2Tk(self.canvas22, self.fcontainer22)
            self.toolbar22.update()
            self.canvas22._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
  
            color = 'tab:blue'
            b = self.figure22.add_subplot(111)
            b.title.set_text("Vector magnitude")
            b.set_ylabel('Activity counts', color=color)
            b.plot(self.bb.Vect_mag_gauche,label="Gauche")
            b.plot(self.bb.Vect_mag_droite,label="Droite")
            plt.legend()
            self.canvas22.draw()
            
         if i==3:
            self.figure32 = Figure(figsize=(5, 4), dpi=100)
            self.canvas32 = FigureCanvasTkAgg(self.figure32, master=self.fcontainer32)
            self.canvas32.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
            self.toolbar32 = NavigationToolbar2Tk(self.canvas32, self.fcontainer32)
            self.toolbar32.update()
            self.canvas32._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
  
            color = 'tab:blue'
            b = self.figure32.add_subplot(111)
            b.title.set_text("Vector magnitude")
            b.set_ylabel('Activity counts', color=color)
            b.plot(self.bb.Vect_mag_gauche,label="Gauche")
            b.plot(self.bb.Vect_mag_droite,label="Droite")
            plt.legend()
            self.canvas32.draw()
            
         if i==4:
            self.figure42 = Figure(figsize=(5, 4), dpi=100)
            self.canvas42 = FigureCanvasTkAgg(self.figure42, master=self.fcontainer42)
            self.canvas42.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
            self.toolbar42 = NavigationToolbar2Tk(self.canvas42, self.fcontainer42)
            self.toolbar42.update()
            self.canvas42._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
  
            color = 'tab:blue'
            b = self.figure42.add_subplot(111)
            b.title.set_text("Vector magnitude")
            b.set_ylabel('Activity counts', color=color)
            b.plot(self.bb.Vect_mag_gauche,label="Gauche")
            b.plot(self.bb.Vect_mag_droite,label="Droite")
            plt.legend()
            self.canvas42.draw()
            
            
         if i==5:
            self.figure52 = Figure(figsize=(5, 4), dpi=100)
            self.canvas52 = FigureCanvasTkAgg(self.figure52, master=self.fcontainer52)
            self.canvas52.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
            self.toolbar52 = NavigationToolbar2Tk(self.canvas52, self.fcontainer52)
            self.toolbar52.update()
            self.canvas52._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
  
            color = 'tab:blue'
            b = self.figure52.add_subplot(111)
            b.title.set_text("Vector magnitude")
            b.set_ylabel('Activity counts', color=color)
            b.plot(self.bb.Vect_mag_gauche,label="Gauche")
            b.plot(self.bb.Vect_mag_droite,label="Droite")
            plt.legend()
            self.canvas52.draw()
        

        
    def plot_magnituderatio(self,i):

        
        if i==0:
            self.figure3 = Figure(figsize=(5, 4), dpi=100)
            self.canvas3 = FigureCanvasTkAgg(self.figure3, master=self.fcontainer3)
            self.canvas3.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
            self.toolbar = NavigationToolbar2Tk(self.canvas3, self.fcontainer3)
            self.toolbar.update()
            self.canvas3._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
            
            color = 'tab:blue'
            b = self.figure3.add_subplot(111)
            b.title.set_text("Magnitude ratio")
            b.set_ylabel('Ratio of activity counts', color=color)
            b.plot(self.bb.mag_ratio,label="Gauche")
            self.canvas3.draw()
        if i==1:
            self.figure13 = Figure(figsize=(5, 4), dpi=100)
            self.canvas13 = FigureCanvasTkAgg(self.figure13, master=self.fcontainer13)
            self.canvas13.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
            self.toolbar13 = NavigationToolbar2Tk(self.canvas13, self.fcontainer13)
            self.toolbar13.update()
            self.canvas13._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
            
            color = 'tab:blue'
            b = self.figure13.add_subplot(111)
            b.title.set_text("Magnitude ratio")
            b.set_ylabel('Ratio of activity counts', color=color)
            b.plot(self.bb.mag_ratio,label="Gauche")
            self.canvas13.draw()
            
        if i==2:
            self.figure23 = Figure(figsize=(5, 4), dpi=100)
            self.canvas23 = FigureCanvasTkAgg(self.figure23, master=self.fcontainer23)
            self.canvas23.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
            self.toolbar23 = NavigationToolbar2Tk(self.canvas23, self.fcontainer23)
            self.toolbar23.update()
            self.canvas23._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
            
            color = 'tab:blue'
            b = self.figure23.add_subplot(111)
            b.title.set_text("Magnitude ratio")
            b.set_ylabel('Ratio of activity counts', color=color)
            b.plot(self.bb.mag_ratio,label="Gauche")
            self.canvas23.draw()
            
        if i==3:
            self.figure33 = Figure(figsize=(5, 4), dpi=100)
            self.canvas33 = FigureCanvasTkAgg(self.figure33, master=self.fcontainer33)
            self.canvas33.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
            self.toolbar33 = NavigationToolbar2Tk(self.canvas33, self.fcontainer33)
            self.toolbar33.update()
            self.canvas33._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
  
            color = 'tab:blue'
            b = self.figure33.add_subplot(111)
            b.title.set_text("Magnitude ratio")
            b.set_ylabel('Ratio of activity counts', color=color)
            b.plot(self.bb.mag_ratio,label="Gauche")
            self.canvas33.draw()
            
        if i==4:
            self.figure43 = Figure(figsize=(5, 4), dpi=100)
            self.canvas43 = FigureCanvasTkAgg(self.figure43, master=self.fcontainer43)
            self.canvas43.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
            self.toolbar43 = NavigationToolbar2Tk(self.canvas43, self.fcontainer43)
            self.toolbar43.update()
            self.canvas43._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
  
            color = 'tab:blue'
            b = self.figure43.add_subplot(111)
            b.title.set_text("Magnitude ratio")
            b.set_ylabel('Ratio of activity counts', color=color)
            b.plot(self.bb.mag_ratio,label="Gauche")
            self.canvas43.draw()
            
            
        if i==5:
            self.figure53 = Figure(figsize=(5, 4), dpi=100)
            self.canvas53 = FigureCanvasTkAgg(self.figure53, master=self.fcontainer53)
            self.canvas52.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
            self.toolbar53 = NavigationToolbar2Tk(self.canvas53, self.fcontainer53)
            self.toolbar53.update()
            self.canvas53._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
  
            color = 'tab:blue'
            b = self.figure53.add_subplot(111)
            b.title.set_text("Magnitude ratio")
            b.set_ylabel('Ratio of activity counts', color=color)
            b.plot(self.bb.mag_ratio,label="Gauche")
            self.canvas53.draw()
        
        
    def plot_bilateralmagnitude(self,i):

        
        if i==0:
            self.figure4 = Figure(figsize=(5, 4), dpi=100)
            self.canvas4 = FigureCanvasTkAgg(self.figure4, master=self.fcontainer4)
            self.canvas4.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
            self.toolbar = NavigationToolbar2Tk(self.canvas4, self.fcontainer4)
            self.toolbar.update()
            self.canvas4._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
            
            color = 'tab:blue'
            b = self.figure4.add_subplot(111)
            b.title.set_text("Bilateral magnitude")
            b.set_ylabel('Sum of activity counts', color=color)
            b.plot(self.bb.bilateral_magnitude)
            self.canvas4.draw()
        if i==1:
            self.figure14 = Figure(figsize=(5, 4), dpi=100)
            self.canvas14 = FigureCanvasTkAgg(self.figure14, master=self.fcontainer14)
            self.canvas14.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
            self.toolbar14 = NavigationToolbar2Tk(self.canvas14, self.fcontainer14)
            self.toolbar14.update()
            self.canvas14._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
            
            color = 'tab:blue'
            b = self.figure14.add_subplot(111)
            b.title.set_text("Bilateral magnitude")
            b.set_ylabel('Sum of activity counts', color=color)
            b.plot(self.bb.bilateral_magnitude)
            self.canvas14.draw()
            
        if i==2:
            self.figure24 = Figure(figsize=(5, 4), dpi=100)
            self.canvas24 = FigureCanvasTkAgg(self.figure24, master=self.fcontainer24)
            self.canvas24.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
            self.toolbar24 = NavigationToolbar2Tk(self.canvas24, self.fcontainer24)
            self.toolbar24.update()
            self.canvas24._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
            
            color = 'tab:blue'
            b = self.figure24.add_subplot(111)
            b.title.set_text("Bilateral magnitude")
            b.set_ylabel('Sum of activity counts', color=color)
            b.plot(self.bb.bilateral_magnitude)
            self.canvas24.draw()
            
        if i==3:
            self.figure34 = Figure(figsize=(5, 4), dpi=100)
            self.canvas34 = FigureCanvasTkAgg(self.figure34, master=self.fcontainer34)
            self.canvas34.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
            self.toolbar34 = NavigationToolbar2Tk(self.canvas34, self.fcontainer34)
            self.toolbar34.update()
            self.canvas34._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
  
            color = 'tab:blue'
            b = self.figure34.add_subplot(111)
            b.title.set_text("Bilateral magnitude")
            b.set_ylabel('Sum of activity counts', color=color)
            b.plot(self.bb.bilateral_magnitude)
            self.canvas34.draw()
            
        if i==4:
            self.figure44 = Figure(figsize=(5, 4), dpi=100)
            self.canvas44 = FigureCanvasTkAgg(self.figure44, master=self.fcontainer44)
            self.canvas44.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
            self.toolbar44 = NavigationToolbar2Tk(self.canvas44, self.fcontainer44)
            self.toolbar44.update()
            self.canvas44._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
  
            color = 'tab:blue'
            b = self.figure44.add_subplot(111)
            b.title.set_text("Bilateral magnitude")
            b.set_ylabel('Sum of activity counts', color=color)
            b.plot(self.bb.bilateral_magnitude)
            self.canvas44.draw()
            
            
        if i==5:
            self.figure54 = Figure(figsize=(5, 4), dpi=100)
            self.canvas54 = FigureCanvasTkAgg(self.figure54, master=self.fcontainer54)
            self.canvas54.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
            self.toolbar54 = NavigationToolbar2Tk(self.canvas54, self.fcontainer54)
            self.toolbar54.update()
            self.canvas54._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
  
            color = 'tab:blue'
            b = self.figure54.add_subplot(111)
            b.title.set_text("Bilateral magnitude")
            b.set_ylabel('Sum of activity counts', color=color)
            b.plot(self.bb.bilateral_magnitude)
            self.canvas54.draw()
        
        
        
        
    def plot_histo(self,i):
        
        #technical
        
        if i==0:
            self.figure5 = Figure(figsize=(5, 4), dpi=100)
            self.canvas5 = FigureCanvasTkAgg(self.figure5, master=self.fcontainer5)
            self.canvas5.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
            self.toolbar = NavigationToolbar2Tk(self.canvas5, self.fcontainer5)
            self.toolbar.update()
            self.canvas5._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
            
            #calculation of histogram
            Vect_mag_droite_removezero=self.bb.Vect_mag_droite[self.bb.Vect_mag_droite>10]
            Vect_mag_gauche_removezero=self.bb.Vect_mag_gauche[self.bb.Vect_mag_gauche>10]
            histgauche,binns=np.histogram(Vect_mag_gauche_removezero,bins='auto')
            histdroite,_=np.histogram(Vect_mag_droite_removezero,bins=binns)
            
            #plot of histograme
            color = 'tab:blue'
            b = self.figure5.add_subplot(111)
            step=8
            b.bar(binns[:-1], histgauche, width=step, align="center", ec="k",label='Gauche')
            b.bar(-binns[:-1][::-1], histdroite[::-1], width=step, align="center", ec="k",label='Droite')
            locs= b.get_xticks() 
            labelx = [int(i) for i in np.abs(locs)]
            b.set_xticks(locs)
            b.set_xticklabels(labelx)
            b.legend(loc='upper right')
            b.title.set_text("Histogram of activity counts")
            b.set_ylabel('Frequency of activity counts', color=color)
            
            self.canvas5.draw() 
            
        if i==1:
            self.figure6 = Figure(figsize=(5, 4), dpi=100)
            self.canvas6 = FigureCanvasTkAgg(self.figure6, master=self.fcontainer6)
            self.canvas6.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
            self.toolbar6 = NavigationToolbar2Tk(self.canvas6, self.fcontainer6)
            self.toolbar6.update()
            self.canvas6._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
            
            #calculation of histogram
            Vect_mag_droite_removezero=self.bb.Vect_mag_droite[self.bb.Vect_mag_droite>10]
            Vect_mag_gauche_removezero=self.bb.Vect_mag_gauche[self.bb.Vect_mag_gauche>10]
            histgauche,binns=np.histogram(Vect_mag_gauche_removezero,bins='auto')
            histdroite,_=np.histogram(Vect_mag_droite_removezero,bins=binns)
            
            #plot of histograme
            color = 'tab:blue'
            b = self.figure6.add_subplot(111)
            step=8
            b.bar(binns[:-1], histgauche, width=step, align="center", ec="k",label='Gauche')
            b.bar(-binns[:-1][::-1], histdroite[::-1], width=step, align="center", ec="k",label='Droite')
            locs= b.get_xticks() 
            labelx = [int(i) for i in np.abs(locs)]
            b.set_xticks(locs)
            b.set_xticklabels(labelx)
            b.legend(loc='upper right')
            b.title.set_text("Histogram of activity counts")
            b.set_ylabel('Frequency of activity counts', color=color)
            
            self.canvas6.draw() 
            
        if i==2:
            self.figure7 = Figure(figsize=(5, 4), dpi=100)
            self.canvas7 = FigureCanvasTkAgg(self.figure7, master=self.fcontainer7)
            self.canvas7.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
            self.toolbar7 = NavigationToolbar2Tk(self.canvas7, self.fcontainer7)
            self.toolbar7.update()
            self.canvas7._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
            
            #calculation of histogram
            Vect_mag_droite_removezero=self.bb.Vect_mag_droite[self.bb.Vect_mag_droite>10]
            Vect_mag_gauche_removezero=self.bb.Vect_mag_gauche[self.bb.Vect_mag_gauche>10]
            histgauche,binns=np.histogram(Vect_mag_gauche_removezero,bins='auto')
            histdroite,_=np.histogram(Vect_mag_droite_removezero,bins=binns)
            
            #plot of histograme
            color = 'tab:blue'
            b = self.figure7.add_subplot(111)
            step=8
            b.bar(binns[:-1], histgauche, width=step, align="center", ec="k",label='Gauche')
            b.bar(-binns[:-1][::-1], histdroite[::-1], width=step, align="center", ec="k",label='Droite')
            locs= b.get_xticks() 
            labelx = [int(i) for i in np.abs(locs)]
            b.set_xticks(locs)
            b.set_xticklabels(labelx)
            b.legend(loc='upper right')
            b.title.set_text("Histogram of activity counts")
            b.set_ylabel('Frequency of activity counts', color=color)
            
            self.canvas7.draw() 
            
        if i==3:
            self.figure8 = Figure(figsize=(5, 4), dpi=100)
            self.canvas8 = FigureCanvasTkAgg(self.figure8, master=self.fcontainer8)
            self.canvas8.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
            self.toolbar8 = NavigationToolbar2Tk(self.canvas8, self.fcontainer8)
            self.toolbar8.update()
            self.canvas8._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
            
            #calculation of histogram
            Vect_mag_droite_removezero=self.bb.Vect_mag_droite[self.bb.Vect_mag_droite>10]
            Vect_mag_gauche_removezero=self.bb.Vect_mag_gauche[self.bb.Vect_mag_gauche>10]
            histgauche,binns=np.histogram(Vect_mag_gauche_removezero,bins='auto')
            histdroite,_=np.histogram(Vect_mag_droite_removezero,bins=binns)
            
            #plot of histograme
            color = 'tab:blue'
            b = self.figure8.add_subplot(111)
            step=8
            b.bar(binns[:-1], histgauche, width=step, align="center", ec="k",label='Gauche')
            b.bar(-binns[:-1][::-1], histdroite[::-1], width=step, align="center", ec="k",label='Droite')
            locs= b.get_xticks() 
            labelx = [int(i) for i in np.abs(locs)]
            b.set_xticks(locs)
            b.set_xticklabels(labelx)
            b.legend(loc='upper right')
            b.title.set_text("Histogram of activity counts")
            b.set_ylabel('Frequency of activity counts', color=color)
            
            self.canvas8.draw() 
            
        if i==4:
            self.figure9 = Figure(figsize=(5, 4), dpi=100)
            self.canvas9 = FigureCanvasTkAgg(self.figure9, master=self.fcontainer9)
            self.canvas9.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
            self.toolbar9 = NavigationToolbar2Tk(self.canvas9, self.fcontainer9)
            self.toolbar9.update()
            self.canvas9._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
            
            #calculation of histogram
            Vect_mag_droite_removezero=self.bb.Vect_mag_droite[self.bb.Vect_mag_droite>10]
            Vect_mag_gauche_removezero=self.bb.Vect_mag_gauche[self.bb.Vect_mag_gauche>10]
            histgauche,binns=np.histogram(Vect_mag_gauche_removezero,bins='auto')
            histdroite,_=np.histogram(Vect_mag_droite_removezero,bins=binns)
            
            #plot of histograme
            color = 'tab:blue'
            b = self.figure9.add_subplot(111)
            step=8
            b.bar(binns[:-1], histgauche, width=step, align="center", ec="k",label='Gauche')
            b.bar(-binns[:-1][::-1], histdroite[::-1], width=step, align="center", ec="k",label='Droite')
            locs= b.get_xticks() 
            labelx = [int(i) for i in np.abs(locs)]
            b.set_xticks(locs)
            b.set_xticklabels(labelx)
            b.legend(loc='upper right')
            b.title.set_text("Histogram of activity counts")
            b.set_ylabel('Frequency of activity counts', color=color)
            
            self.canvas9.draw() 
            
        if i==5:
            self.figure10 = Figure(figsize=(5, 4), dpi=100)
            self.canvas10 = FigureCanvasTkAgg(self.figure10, master=self.fcontainer10)
            self.canvas10.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
            self.toolbar10 = NavigationToolbar2Tk(self.canvas10, self.fcontainer10)
            self.toolbar10.update()
            self.canvas10._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
            
            #calculation of histogram
            Vect_mag_droite_removezero=self.bb.Vect_mag_droite[self.bb.Vect_mag_droite>10]
            Vect_mag_gauche_removezero=self.bb.Vect_mag_gauche[self.bb.Vect_mag_gauche>10]
            histgauche,binns=np.histogram(Vect_mag_gauche_removezero,bins='auto')
            histdroite,_=np.histogram(Vect_mag_droite_removezero,bins=binns)
            
            #plot of histograme
            color = 'tab:blue'
            b = self.figure10.add_subplot(111)
            step=8
            b.bar(binns[:-1], histgauche, width=step, align="center", ec="k",label='Gauche')
            b.bar(-binns[:-1][::-1], histdroite[::-1], width=step, align="center", ec="k",label='Droite')
            locs= b.get_xticks() 
            labelx = [int(i) for i in np.abs(locs)]
            b.set_xticks(locs)
            b.set_xticklabels(labelx)
            b.legend(loc='upper right')
            b.title.set_text("Histogram of activity counts")
            b.set_ylabel('Frequency of activity counts', color=color)
            
            self.canvas10.draw() 
        
        

        


        

        
    
        
        
    
        

        
    def run(self):
        self.mainwindow.mainloop()
        
        
        
if __name__ == '__main__':
    plt.close('all')
    app = MyApplication()
    app.run()