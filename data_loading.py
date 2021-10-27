# -*- coding: utf-8 -*-
"""
Created on Tue Mar  9 14:03:14 2021

@author: al-abiad
"""
import numpy as np

from datetime import datetime, time, timedelta

from struct import *
from math import *
import io

from collections import OrderedDict



def twos_comp(val, bits):

    if( (val&(1<<(bits-1))) != 0 ):
        val = val - (1<<bits)
    return val

def byte(value):
    return (value + 2 ** 7) % 2 ** 8 - 2 ** 7

def ushort(value):
    return value % 2 ** 16

def short(value):
    return (value + 2 ** 15) % 2 ** 16 - 2 ** 15

def axivity_read_timestamp(stamp):
    stamp = unpack('I', stamp)[0]
    year = ((stamp >> 26) & 0x3f) + 2000
    month = (stamp >> 22) & 0x0f
    day   = (stamp >> 17) & 0x1f
    hours = (stamp >> 12) & 0x1f
    mins  = (stamp >>  6) & 0x3f
    secs  = (stamp >>  0) & 0x3f
    try:
        t = datetime(year, month, day, hours, mins, secs)
    except ValueError:
        t = None
    return t

def axivity_read_timestamp_raw(stamp):
    year = ((stamp >> 26) & 0x3f) + 2000
    month = (stamp >> 22) & 0x0f
    day   = (stamp >> 17) & 0x1f
    hours = (stamp >> 12) & 0x1f
    mins  = (stamp >>  6) & 0x3f
    secs  = (stamp >>  0) & 0x3f
    try:
        t = datetime(year, month, day, hours, mins, secs)
    except ValueError:
        t = None
    return t

def axivity_read(fh, bytes):
    data = fh.read(bytes)
    if len(data) == bytes:
        return data
    else:
        raise IOError
        
        # raise IOError

def axivity_parse_header(fh):

    ax_header = OrderedDict()

    blockSize = unpack('H', axivity_read(fh,2))[0] #H== unsigned short
    performClear = unpack('B', axivity_read(fh,1))[0] #B== unsigned char
    deviceId = unpack('H', axivity_read(fh,2))[0]
    sessionId = unpack('I', axivity_read(fh,4))[0] #I==unsigned int
    shippingMinLightLevel = unpack('H', axivity_read(fh,2))[0]
    loggingStartTime = axivity_read(fh,4)
    loggingEndTime = axivity_read(fh,4)
    # print(loggingEndTime)
    loggingCapacity = unpack('I', axivity_read(fh,4))[0]
    # print("loggingCapacity")
    # print(loggingCapacity)
    allowStandby = unpack('B', axivity_read(fh,1))[0]
    debuggingInfo = unpack('B', axivity_read(fh,1))[0]
    # print("debuggingInfo")
    # print(debuggingInfo)
    batteryMinimumToLog = unpack('H', axivity_read(fh,2))[0]
    # print("batteryMinimumToLog")
    # print(batteryMinimumToLog)
    batteryWarning = unpack('H', axivity_read(fh,2))[0]
    # print("batteryWarning")
    # print(batteryWarning)
    enableSerial = unpack('B', axivity_read(fh,1))[0]
    lastClearTime = axivity_read(fh,4)
    samplingRate = unpack('B', axivity_read(fh,1))[0]
    lastChangeTime = axivity_read(fh,4)
    firmwareVersion = unpack('B', axivity_read(fh,1))[0]

    reserved = axivity_read(fh,22)

    annotationBlock = axivity_read(fh, 448 + 512)

    if len(annotationBlock) < 448 + 512:
        annotationBlock = ""

    annotation = ""
    for x in annotationBlock:
        if x != 255 and x != ' ':
            if x == '?':
                x = '&'
            annotation += str(x)
    annotation = annotation.strip()

    annotationElements = annotation.split('&')
    annotationNames = {
        '_c': 'studyCentre',
        '_s': 'studyCode',
        '_i': 'investigator',
        '_x': 'exerciseCode',
        '_v': 'volunteerNum', '_p':
        'bodyLocation', '_so':
        'setupOperator', '_n': 'notes',
        '_b': 'startTime', '_e': 'endTime',
        '_ro': 'recoveryOperator',
        '_r': 'retrievalTime',
        '_co': 'comments'
    }

    for element in annotationElements:
        kv = element.split('=', 2)
        
        if kv[0] in annotationNames:
            
            ax_header[annotationNames[kv[0]]] = kv[1]
    
    
    for x in ('startTime', 'endTime', 'retrievalTime'):
        if x in ax_header:
            # print("ax_header['startTime']")
            if '/' in ax_header[x]:
                ax_header[x] = time.strptime(ax_header[x], '%d/%m/%Y')
            else:
                ax_header[x] = time.strptime(ax_header[x], '%Y-%m-%d %H:%M:%S')


    lastClearTime = axivity_read_timestamp(lastClearTime)
    # print(lastClearTime)
    lastChangeTime = axivity_read_timestamp(lastChangeTime)
    # print(lastChangeTime)
    firmwareVersion = firmwareVersion if firmwareVersion != 255 else 0


    #ax_header["sample_rate"] = samplingRate
    ax_header["device"] = deviceId
    ax_header["session"] = sessionId
    ax_header["firmware"] = firmwareVersion
    # print(loggingStartTime)
    # print(axivity_read_timestamp(loggingStartTime))
    ax_header["logging_start_time"] = axivity_read_timestamp(loggingStartTime)
    ax_header["logging_end_time"] = axivity_read_timestamp(loggingEndTime)


    ax_header["frequency"] = 3200/(1<<(15-(int(samplingRate) & 0x0f)))


    return ax_header

def convert_actigraph_timestamp(t):
    return datetime(*map(int, [t[6:10],t[3:5],t[0:2],t[11:13],t[14:16],t[17:19],int(t[20:])*1000]))

def load(source, datetime_format="%d/%m/%Y %H:%M:%S:%f", datetime_column=0, ignore_columns=False, unique_names=False, hdf5_mode="r", hdf5_group="Raw",startreading="",stopreading=""):
    
    if startreading!="":
        startreading=datetime.strptime(startreading, '%d/%m/%Y %H:%M:%S')
        stopreading=datetime.strptime(stopreading, '%d/%m/%Y %H:%M:%S')
    
    load_start = datetime.now()

    header = OrderedDict()


    
    handle = open(source, "rb")
    raw_bytes = handle.read()
    #print("Number of bytes:", len(raw_bytes))
    #print("/512 = ", len(raw_bytes)/512)
    
    fh = io.BytesIO(raw_bytes)
    
    n = 0
    num_samples = 0
    num_pages = 0
    
    start = datetime(2014, 1, 1)
    
    # Rough number of pages expected = length of file / size of block (512 bytes)
    # Rough number of samples expected = pages * 120
    # Add 1% buffer just to be cautious - it's trimmed later
    estimated_num_pages = int(len(raw_bytes)/512 * 1.01)
    estimated_num_samples = int(estimated_num_pages*120)
    #print("Estimated number of samples:", estimated_num_samples)
    
    axivity_x = np.empty(estimated_num_samples)
    axivity_y = np.empty(estimated_num_samples)
    axivity_z = np.empty(estimated_num_samples)
    axivity_light = np.empty(estimated_num_pages)
    axivity_temperature = np.empty(estimated_num_pages)
    axivity_timestamps = np.empty(estimated_num_pages, dtype=type(start))
    axivity_indices = np.empty(estimated_num_pages)
    
    file_header = OrderedDict()
    
    lastSequenceId = None
    lastTimestampOffset = None
    lastTimestamp = None
    
    try:
        header = axivity_read(fh,2)
    
        while len(header) == 2:
    
            if header == b'MD':
                #print('MD')
                file_header = axivity_parse_header(fh)
                
                if startreading=="":
                    return file_header
            elif header == b'UB':
                #print('UB')
                blockSize = unpack('H', axivity_read(fh,2))[0]
            elif header == b'SI':
                #print('SI')
                pass
            elif header == b'AX':
    
                packetLength, deviceId, sessionId, sequenceId, sampleTimeData, light, temperature, events, battery, sampleRate, numAxesBPS, timestampOffset, sampleCount = unpack('HHIIIHHcBBBhH', axivity_read(fh,28))
    
                if packetLength != 508 or sampleRate == 0:
                    continue
    
                if ((numAxesBPS >> 4) & 15) != 3:
                    print('[ERROR: num-axes not expected]')
    
                if (numAxesBPS & 15) == 2:
                    bps = 6
                elif (numAxesBPS & 15) == 0:
                    bps = 4
    
                freq = 3200 / (1 << (15 - sampleRate & 15))
                if freq <= 0:
                    freq = 1
    
                timestamp_original = axivity_read_timestamp_raw(sampleTimeData)
    
                if timestamp_original is None:
                    continue
    
                # if top-bit set, we have a fractional date
                if deviceId & 0x8000:
                    # Need to undo backwards-compatible shim by calculating how many whole samples the fractional part of timestamp accounts for.
                    timeFractional = (deviceId & 0x7fff) * 2     # use original deviceId field bottom 15-bits as 16-bit fractional time
                    timestampOffset += (timeFractional * int(freq)) // 65536 # undo the backwards-compatible shift (as we have a true fractional)
                    timeFractional = float(timeFractional) / 65536
    
                    # Add fractional time to timestamp
                    timestamp = timestamp_original + timedelta(seconds=timeFractional)
    
                else:
    
                    timestamp = timestamp_original
    
                # --- Time interpolation ---
                # Reset interpolator if there's a sequence break or there was no previous timestamp
                if lastSequenceId == None or (lastSequenceId + 1) & 0xffff != sequenceId or lastTimestampOffset == None or lastTimestamp == None:
                    # Bootstrapping condition is a sample one second ago (assuming the ideal frequency)
                    lastTimestampOffset = timestampOffset - freq
                    lastTimestamp = timestamp - timedelta(seconds=1)
                    lastSequenceId = sequenceId - 1
    
                localFreq = timedelta(seconds=(timestampOffset - lastTimestampOffset)) / (timestamp - lastTimestamp)
                final_timestamp = timestamp + -timedelta(seconds=timestampOffset) / localFreq
    
                # Update for next loop
                lastSequenceId = sequenceId
                lastTimestampOffset = timestampOffset - sampleCount
                lastTimestamp = timestamp
                
                # print(final_timestamp)

                if final_timestamp>startreading and final_timestamp<stopreading:
                    # print("we are inside condition")
                    axivity_indices[num_pages] = num_samples
                    axivity_timestamps[num_pages] = final_timestamp
                    axivity_light[num_pages] = light
                    axivity_temperature[num_pages] = temperature
                    num_pages += 1
        
                    for sample in range(sampleCount):
        
                        if bps == 6:
        
                            x, y, z = unpack('hhh', fh.read(6))
                            x, y, z = x/256.0, y/256.0, z/256.0
        
                        elif bps == 4:
        
                            temp = unpack('I', fh.read(4))[0]
                            temp2 = (6 - byte(temp >> 30))
                            x = short(short((ushort(65472) & ushort(temp << 6))) >> temp2) / 256.0
                            y = short(short((ushort(65472) & ushort(temp >> 4))) >> temp2) / 256.0
                            z = short(short((ushort(65472) & ushort(temp >> 14))) >> temp2) / 256.0
        
                            # Optimisation: cache value of ushort(65472) ?
        
                        axivity_x[num_samples] = x
                        axivity_y[num_samples] = y
                        axivity_z[num_samples] = z
        
                        num_samples += 1
                        
                if final_timestamp>stopreading:
                    break
                else:
      
                    fh.seek((sampleCount)*4,1) 
                    
                checksum = unpack('H', axivity_read(fh,2))[0]
    
            else:
                pass
                #print("Unrecognised header", header)
    
            header = axivity_read(fh,2)
    
            n=n+1
            

    except IOError:
        # End of file
        pass

    # We created oversized arrays at the start, to make sure we could fit all the data in
    # Now we know how much data was there, we can shrink the arrays to size
    

    axivity_x.resize(num_samples)
    axivity_y.resize(num_samples)
    axivity_z.resize(num_samples)
    
    axivity_timestamps.resize(num_pages)
    axivity_indices.resize(num_pages)
    axivity_temperature.resize(num_pages)
    axivity_light.resize(num_pages)

    axivity_indices = axivity_indices.astype(int)

    


    header = file_header


    # Calculate how long it took to load this file
    # load_end = datetime.now()
    # load_duration = (load_end - load_start).total_seconds()


    return axivity_timestamps,axivity_indices,axivity_x,axivity_y,axivity_z

if __name__ == "__main__":
    # filename="d:\\Users\\al-abiad\\Desktop\\BB-Bim\\test 1\\G_AV_Test1.CWA"
    filename="d:\\Users\\al-abiad\\Desktop\\BB-Bim\\SELE\\D_SL_Activite_libre&test9.CWA"
    start_time="01/04/2021 15:25:00"
    
    # start_time=""
    
    end_time="01/04/2021 15:42:00"
    
    # start_time="26/01/2021 13:30:00"
    # end_time="26/01/2021 13:40:00"
    t1,i1,x1,y1,z1= load(filename,startreading=start_time,stopreading=end_time)
    
    # header= load(filename,startreading=start_time,stopreading=end_time)
