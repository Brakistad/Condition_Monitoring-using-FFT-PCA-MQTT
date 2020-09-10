# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 14:33:54 2020

@author: oyvin
"""
import PCA_Module
import mqttInterface
import time as t
import pandas as pd
import threading
import numpy as np
import matplotlib.pyplot as plt
import scipy.fftpack
from kb_utils import SaveLoad as SL

listening = True# TODO Need to add function
q_data = []
threads = []
sensorListener = mqttInterface.mqtt_User()
lastMsg = ""
timesRetry = 0
maxTimesRetry = 3
fftReady = False
maxHistory = 50
datacount = len(SL('load','pcain'))

def init_data(data):
    SL('save', 'Data', variables = data)

def prep_data(Data):
    data_dir = Data[2].split('"')
    columns = []
    value = []
    key=False
    for piece in data_dir:
        next_ = True
        if not (len(piece)<2):
            piece = piece.lower()
            if (piece.isupper() or piece.islower()):
                columns.append(piece)
                key = True
                next_ = False
            if (key and next_):
                value.append(piece)
                key = False
                next_ = False
    for val in value:
        temp = val
        val = value[value.index(temp)].replace(':','')
        value[value.index(temp)] = val
        temp = val
        val = value[value.index(temp)].replace('[','')
        value[value.index(temp)] = val
        temp = val
        if(value[value.index(temp)][-1:] == ','):
            val = value[value.index(temp)][:-1]
        value[value.index(temp)] = val
        temp = val
        val = value[value.index(temp)].replace(']','')
        value[value.index(temp)] = val
        temp = val
        val = value[value.index(temp)].replace('{','')
        value[value.index(temp)] = val
        temp = val
        val = value[value.index(temp)].replace('}','')
        value[value.index(temp)] = val
        temp = val
        if (val.count(',')>1):    
            val = value[value.index(temp)].split(',')
        value[value.index(temp)] = val
        if (isinstance(val, list)):
            for v in val:
                value[value.index(val)][val.index(v)] = float(v)
    i=0
    finnished_data = {}
    for key in columns:
        finnished_data.update({columns[i] : value[i]})
        i+=1
    finnished_data.update({"timerecieved": Data[1]})
    store_history(finnished_data)
    init_data(finnished_data)
    #print(finnished_data)

def store_history(Data, _raw = True):
    global maxHistory
    completeDataset = SL('load','Data_history')
    
    if (completeDataset == None):
            completeDataset = {'raw':{},'pca':{}}
            if(_raw):
                completeDataset['raw'].update({str(t.asctime(t.localtime())):Data})
            else:
                completeDataset['pca'].update({str(t.asctime(t.localtime())):Data})
    else:
        if(_raw):
            n_raw = len(completeDataset['raw'])
            if (n_raw>maxHistory):
                        completeDataset['raw'].pop(list(completeDataset['raw'].keys())[0])
            completeDataset['raw'].update({str(t.asctime(t.localtime())):Data})
        else:
            n_pca = len(completeDataset['pca'])
            if (n_pca>maxHistory):
                        completeDataset['pca'].pop(list(completeDataset['pca'].keys())[0])
            completeDataset['pca'].update({str(t.asctime(t.localtime())):Data})
    SL('save', 'Data_history', variables = completeDataset)


def analyse_FFT():
    global fftReady
    global q_data
    while(any(q_data)):
        fftReady = False
        prep_data(q_data[0])
        q_data = q_data[1:]
        Data = SL('load','Data')
        delta_avg_time = float(Data['avgdeltatime[us]'])
        #delta_avg_time = float(Data['avgdeltatime[us]'])
        x = Data['x[g]']
        y = Data['y[g]']
        z = Data['z[g]']
        v = []
        for xyz in zip(x,y,z):
            v.append(np.sqrt(xyz[0]*xyz[0]+xyz[1]*xyz[1]+xyz[2]*xyz[2]))
        T = (delta_avg_time * (10**(-6)))
        Nx = int(len(x))
        Ny = int(len(y))
        Nz = int(len(z))
        Nv = int(len(v))
        tx = np.linspace(0.0, Nx*T, Nx)
        ty = np.linspace(0.0, Ny*T, Ny)
        tz = np.linspace(0.0, Nz*T, Nz)
        tv = np.linspace(0.0, Nv*T, Nv)
        xf = scipy.fftpack.rfft(x)
        yf = scipy.fftpack.rfft(y)
        zf = scipy.fftpack.rfft(z)
        vf = scipy.fftpack.rfft(v)
        tfx = np.linspace(0.0, 1.0/(2.0*T), Nx//2)
        tfy = np.linspace(0.0, 1.0/(2.0*T), Ny//2)
        tfz = np.linspace(0.0, 1.0/(2.0*T), Nz//2)
        tfv = np.linspace(0.0, 1.0/(2.0*T), Nv//2)
        fig, ax = plt.subplots()
        ax.set_title("plotting time series of X axis on engine: " + Data['tag'] + " recieved " + Data['timerecieved'])
        ax.plot(tx,x)
        plt.show()
        fig, ax = plt.subplots()
        ax.set_title("plotting time series of Y axis on engine: " + Data['tag'] + " recieved " + Data['timerecieved'])
        ax.plot(ty,y)
        plt.show()
        fig, ax = plt.subplots()
        ax.set_title("plotting time series of Z axis on engine: " + Data['tag'] + " recieved " + Data['timerecieved'])
        ax.plot(tz,z)
        plt.show()
        fig, ax = plt.subplots()
        ax.set_title("plotting time series of abs vector on engine: " + Data['tag'] + " recieved " + Data['timerecieved'])
        ax.plot(tv,v)
        plt.show()
        fig, ax = plt.subplots()
        ax.set_title("plotting freq_spectrum of X axis on engine: " + Data['tag'] + " recieved " + Data['timerecieved'])
        ax.plot(tfx[1:], 2.0/Nx * np.abs(xf[1:Nx//2]))
        #x_lim = ax.get_ylim()
        plt.show()
        fig, ax = plt.subplots()
        ax.set_title("plotting freq_spectrum of Y axis on engine: " + Data['tag'] + " recieved " + Data['timerecieved'])
        ax.plot(tfy[1:], 2.0/Ny * np.abs(yf[1:Ny//2]))
        #y_lim = ax.get_ylim()
        plt.show()
        fig, ax = plt.subplots()
        ax.set_title("plotting freq_spectrum of Z axis on engine: " + Data['tag'] + " recieved " + Data['timerecieved'])
        ax.plot(tfz[1:], 2.0/Nz * np.abs(zf[1:Nz//2]))
        #z_lim = ax.get_ylim()
        plt.show()
        fig, ax = plt.subplots()
        ax.set_title("plotting freq_spectrum of abs vector on engine: " + Data['tag'] + " recieved " + Data['timerecieved'])
        ax.plot(tfv[1:], 2.0/Nv * np.abs(vf[1:Nv//2]))
        #v_lim = ax.get_ylim()
        plt.show()
#        xf_avg = avrg_list(xf[1:])
#        yf_avg = avrg_list(yf[1:])
#        zf_avg = avrg_list(zf[1:])
#        vf_avg = avrg_list(vf[1:])
        #fig, ax = plt.subplots()
#        ax.set_title("plotting averaged freq_spectrum of X axis on engine: " + Data['tag'] + " recieved " + Data['timerecieved'])
#        ax.plot(tfx[1:], 2.0/Nx * np.abs(xf_avg[0][1:Nx//2]))
#        ax.set_ylim(x_lim)
#        plt.show()
#        fig, ax = plt.subplots()
#        ax.set_title("plotting averaged freq_spectrum of Y axis on engine: " + Data['tag'] + " recieved " + Data['timerecieved'])
#        ax.plot(tfy[1:], 2.0/Ny * np.abs(yf_avg[0][1:Ny//2]))
#        ax.set_ylim(y_lim)
#        plt.show()
#        fig, ax = plt.subplots()
#        ax.set_title("plotting averaged freq_spectrum of Z axis on engine: " + Data['tag'] + " recieved " + Data['timerecieved'])
#        ax.plot(tfz[1:], 2.0/Nz * np.abs(zf_avg[0][1:Nz//2]))
#        ax.set_ylim(z_lim)
#        plt.show()
#        fig, ax = plt.subplots()
#        ax.set_title("plotting averaged freq_spectrum of abs vector on engine: " + Data['tag'] + " recieved " + Data['timerecieved'])
#        ax.plot(tfv[1:], 2.0/Nv * np.abs(vf_avg[0][1:Nv//2]))
#        ax.set_ylim(v_lim)
#        plt.show()
        
        time_recieved = Data['timerecieved']
        tag = Data['tag']
        temperaturedifference = float(Data['temperaturedifference'])
        rpm = float(Data['rpm'])
        _objectRow = [tag, time_recieved, temperaturedifference, rpm, *yf[:len(yf)//2]]
        store_in_pca_inputs(_objectRow)


def store_in_pca_inputs(objectRow):
    global datacount
    try:
        objectList = SL('load', 'pcain')
    except:
        SL('save', 'pcain', variables = [])
    objectList.append(objectRow)
    SL('save','pcain',variables = objectList)
    datacount += 1
    print("DATACOUNT IS " + str(datacount))
    

def analyse_pca():
    global datacount
    print("started analysing the pca")
    PCA_Module.fetchData()
    PCA_Module.fit_PCA()
    PCA_Module.display_PCA()
    store_history(PCA_Module.get_complete_Data(),False)
    SL('save','pcain', variables = [])
    datacount = 0

def avrg_list(oldList):
    rangesize = 5
    i=0
    g=0
    partsum = []
    avrgs = []
    avg_list = list(oldList)
    for pt in oldList:
        partsum.append(pt)
        if((i>=rangesize)or(pt == oldList[(len(oldList)-1)])):
            avrg = np.average(partsum)
            avrgs.append(avrg)
            partsum = []
            for j in np.arange(i+1):
                avg_list[g-j] = avrg
            i=0
        i+=1
        g+=1
    return [avg_list,avrgs]

        


def fit_dataQueue(datedData):
    global lastMsg
    global listening
    global q_data
    Message = [datedData[1],datedData[2],datedData[0]]
    if not (lastMsg == Message):
        q_data.append(Message)
    lastMsg = Message
    queue_size = len(q_data)
    print("queue size is now " + str(queue_size))
    listening = False
    

def listen_sensors():
    # main listener task which will be running continiously. listening to sensor publishers.
    global timesRetry
    global listening
    import threading
    import time
    import socket
    try:
        addr1 = socket.gethostbyname('ip.applause.no')
    except:
        return False
    print("started testing")
    sensorListener.change_serverIp(addr1)
    sensorListener.change_userInfo('engineer', 'vykgVjYTPDcK')
    while(listening):
        t = threading.Thread(target = sensorListener.listen_until)
        print("is_alive = " + str(t.is_alive()))
        print("_initialized = " + str(t._initialized))
        t.start()
        print("is_alive = " + str(t.is_alive()))
        print("_initialized = " + str(t._initialized))
        i=0
        messageData = ""
        while t.is_alive():
            if(sensorListener.check_recievedMsg()):
                messageData = sensorListener.get_recentMsg()
                fit_dataQueue(messageData)
                i = 0
                sensorListener.stop_listening()
            else:
                print("listening ... " + str(i))
                i += 1
                time.sleep(2)
                if(i > 40):
                    sensorListener.stop_listening()
                    time.sleep(2)
                    return False
    return True

i=0
pca_object_amount = 20
fft_worker = threading.Thread(target = analyse_FFT)
pca_worker = threading.Thread(target = analyse_pca)
while(i<1000):
    works = listen_sensors()
    listening = True
    if(works):
        print("job has completed successfully")
        if (not (fft_worker.is_alive()) and not (pca_worker.isAlive()) and (datacount<pca_object_amount)):
            fft_worker = threading.Thread(target = analyse_FFT)
            fft_worker.start()
        if (not (pca_worker.is_alive()) and not (fft_worker.isAlive()) and (datacount>=pca_object_amount)):
            pca_worker = threading.Thread(target = analyse_pca)
            pca_worker.start()
    else:
        print("was not able to establish connection")
        t.sleep(20)
    i+=1

if __name__ == "__main__":
    Vault = 90