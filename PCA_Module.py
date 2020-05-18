# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 13:14:44 2020

@author: oyvin
"""
import pandas as pd;
import random as rand;
from kb_utils import SaveLoad as SL;
import matplotlib as matplt;
import matplotlib.pyplot as plt;
from mpl_toolkits.mplot3d import Axes3D;
from sklearn.preprocessing import StandardScaler;
from sklearn.decomposition import PCA;
import time as t;
import numpy as numpi;


columns = ["engineID","vib_amp","vib_freq","rpm", "temp"];
Data = "";
df = "";
pca = "";
principalComponents = "";
principalDf = "";
pca_components = 3;
complete_Data = "";
loggable_Data = "";
column_to_check = "tempdev";
flag_color = True;
loadings = "";
ignore_these_columns = [];

def genRandDataset(nObjects):
    global columns;
    global Data;
    global df;
    columns = ["engineID","vib_amp","vib_freq","rpm","temp"];
    Data = {"engineID":[],"vib_amp":[],"vib_freq":[],"rpm":[],"temp":[]};
    randGen = rand.Random();
    randGen.seed(t.gmtime());
    for column in Data:
        i=0;
        randomNumber = 0;
        if(column == "engineID"):
            low = 0
            high = 10;
        elif(column == "vib_amp"):
            low = 0.0;
            high = 8.0;
        elif(column == "vib_freq"):
            low = 0.0;
            high = 2000.0;
        elif(column == "rpm"):
            low = 1000.0;
            high = 1400.0;
        elif(column == "temp"):
            low = 25.0;
            high = 60.0;
        a = 0;
        while(i < nObjects):
            randomNumber = randGen.uniform(low,high);
            if(column == "engineID"):
                randomNumber = a;
                if (a<10):
                    a +=1;
                else:
                    a = 0;
            Data[column].append(randomNumber);
            i+=1;
def fetchData():
    global Data;
    global columns;
    freshData = SL('load','pcain');
    N = len(freshData[0][4:]);
    columns = ["tag and timestamp","tempdev","rpm"];
    Data = {};
    _N = len(freshData[0]);
    for i in range(N):
        columns.append("f"+str(i));
    for name in columns:
        Data.update({name : []});
    for row in freshData:
        _tag_timestamp = "";
        for j in range(_N):
            if (j == 0):
                _tag_timestamp = row[j] + "-";
            elif(j == 1):
                _tag_timestamp +=  row[j];
                Data[columns[j-1]].append(_tag_timestamp);
            else:
                Data[columns[j-1]].append(row[j]);



def fit_PCA():
    global columns;
    global Data;
    global df;
    global principalComponents;
    global principalDf;
    global pca;
    global pca_components;
    global complete_Data;
    global loggable_data;
    global loadings;
    df = pd.DataFrame(Data);
    myX = df[columns[1:]];
    #print(myX);
    
    #print(myY);
    myX = StandardScaler().fit_transform(myX);
    #print(df);
    
    pca = PCA(n_components=pca_components)
    
    principalComponents = pca.fit_transform(myX);
    pca_columns = [];
    for i in range(pca_components):
        pca_columns.append('principal component ' + str(i+1));
    principalDf = pd.DataFrame(data = principalComponents
                 , columns = pca_columns)
    complete_Data = pd.concat([principalDf, df, pd.DataFrame(pca.components_.T, columns=['PC1', 'PC2', 'PC3'], index=columns[1:]) ], axis = 1);
    loggable_data = Data;
    loadings = pd.DataFrame(pca.components_.T, columns=['PC1', 'PC2', 'PC3'], index=columns[1:]);

def upload_data_history(n=1):
    global completeData;
    global Data;
    global columns;
    global ignore_these_columns;
    dataHis = SL('load','data_History');
    columnList = [];
    newData = {};
    stopat = 'f341';
    continueIt = True;
    for row in dataHis['pca'][list(dataHis['pca'].keys())[(len(list(dataHis['pca'].keys()))-1)]]:
        if(continueIt):
            if(row == stopat):
                continueIt = False;
            if not (ignore_these_columns.__contains__(row)):
                columnList.append(row);
    for col in columnList:
        newData.update({col:[]});
    for i in range(n):
        #print(dataHis['pca'][list(dataHis['pca'].keys())[(len(list(dataHis['pca'].keys()))-1) - i]]);
        for col in columnList:
            newData[col].extend(dataHis['pca'][list(dataHis['pca'].keys())[(len(list(dataHis['pca'].keys()))) - n + i]][col]);
    newData.update({'objectN':list(range(len(newData[columnList[0]])))});
    Data = newData;
    columns = columnList;
    #print(Data);

def export_csv():
    global Data;
    df = pd.DataFrame(Data);
    print(df);
    df.to_csv (r'C:\Users\oyvin\Documents\Python\exportedData\export_dataframe.csv', index = False, header=True);
    
def activate_colors(flag = True):
    global flag_color;
    flag_color = flag;


def create_colors(n):
    global flag_color;
    ret = [];
    ma = max(n);
    mi = min(n);
    gt = 0.0;
    bt = 0.4;
    at = 0.7;
    if(flag_color):
        for i in range(len(n)):
            rt = ((n[i] - mi + .1)/(ma - mi + .1));
            ret.append(numpi.atleast_2d([rt,gt,bt,at]));#'#' + '%02x%02x%02x' % 
    else:
        for i in range(len(n)):
            ret.append(numpi.atleast_2d([0.0,0.0,0.0,at]));#'#' + '%02x%02x%02x' %
    return ret;

def check_column(col):
    global column_to_check;
    column_to_check = col;

def ignore_columns(col=[]):
    global ignore_these_columns;
    ignore_these_columns = col;

def display_PCA():
    global columns;
    global Data;
    global df;
    global principalComponents;
    global principalDf;
    global complete_Data;
    global column_to_check;
    global loadings;
    finalDf = complete_Data;
    fig = plt.figure(figsize = (8,8))
    ax = fig.add_subplot(1,1,1)
    ax.set_xlabel('Principal Component 1', fontsize = 15)
    ax.set_ylabel('Principal Component 2', fontsize = 15)
    ax.set_title('2 component PCA', fontsize = 20)
    targets = df['tag and timestamp'];
    colorcodeArray = list(map(lambda x: float(numpi.sqrt(x[0]**2 + x[1]**2 + x[2]**2 + x[3]**2) >= 2.7), 
                               zip(numpi.abs(finalDf['f53']),
                                numpi.abs(finalDf['f54']),
                                numpi.abs(finalDf['f55']),
                                numpi.abs(finalDf['f56']))));
    colors = create_colors([*colorcodeArray]);
    #colors = create_colors([*finalDf[column_to_check]]);
    for target, _color in zip(targets,colors):
        indicesToKeep = finalDf['tag and timestamp'] == target
        ax.scatter(finalDf.loc[indicesToKeep, 'principal component 1']
                   , finalDf.loc[indicesToKeep, 'principal component 2']
                   , c = _color
                   , s = 50)
#    for i, txt in enumerate(zip(finalDf['tag and timestamp'],finalDf['tempdev'])):
#        if ((i%50 == 0) or (i ==1)):
#            ax.annotate(txt,(finalDf['principal component 1'][i], finalDf['principal component 2'][i]));
    ax.grid();

def get_complete_Data():
    global loggable_data;
    return loggable_data;

def display3D_PCA():
    global columns;
    global Data;
    global df;
    global principalComponents;
    global principalDf;
    global complete_Data;
    global column_to_check;
    finalDf = complete_Data;
    
    fig = plt.figure(figsize = (8,8))
    ax = fig.add_subplot(111, projection = '3d') 
    ax.set_xlabel('Principal Component 1', fontsize = 15)
    ax.set_ylabel('Principal Component 2', fontsize = 15)
    ax.set_zlabel('Principal Component 3', fontsize = 15)
    ax.set_title('3 component PCA', fontsize = 20)
    targets = df['tag and timestamp']
    colors = create_colors([*finalDf[column_to_check]]);
    for target, _color in zip(targets,colors):
        indicesToKeep = finalDf['tag and timestamp'] == target
        ax.scatter(finalDf.loc[indicesToKeep, 'principal component 1']
                   , finalDf.loc[indicesToKeep, 'principal component 2']
                   , finalDf.loc[indicesToKeep, 'principal component 3']
                   , c = _color
                   , s = 50
                   , depthshade = True)
    #ax.legend(Data['tag and timestamp']);
def plot_against():
    global complete_Data;
    global column_to_check;
    finalDf = complete_Data;
    fig, ax = plt.subplots();
    fig.suptitle('Comparing ' + column_to_check + ' to principal component 1');
    ax.scatter(finalDf[column_to_check],finalDf['principal component 1']);
    fig, ax = plt.subplots();
    fig.suptitle('Comparing ' + column_to_check + ' to principal component 2');
    ax.scatter(finalDf[column_to_check],finalDf['principal component 2']);
    fig, ax = plt.subplots();
    fig.suptitle('Comparing ' + column_to_check + ' to principal component 3');
    ax.scatter(finalDf[column_to_check],finalDf['principal component 3']);

def plot_against_freq():
    global complete_Data;
    global columns;
    finalDf = complete_Data;
    fig, ax = plt.subplots();
    fig.suptitle('Comparing scores of frequencies on principal component 1');
    colormatch = create_colors(range(len(columns[3:])));
    for freq,_color in zip(columns[3:],colormatch):
        ax.scatter(finalDf[freq]
                   , finalDf['principal component 1']
                   , c = _color
                   , s = 30);
    fig, ax = plt.subplots();
    fig.suptitle('Comparing scores of frequencies on principal component 2');
    colormatch = create_colors(range(len(columns[3:])));
    for freq,_color in zip(columns[3:],colormatch):
        ax.scatter(finalDf[freq]
                   , finalDf['principal component 2']
                   , c = _color
                   , s = 30);
    fig, ax = plt.subplots();
    fig.suptitle('Comparing scores of frequencies on principal component 3');
    colormatch = create_colors(range(len(columns[3:])));
    for freq,_color in zip(columns[3:],colormatch):
        ax.scatter(finalDf[freq]
                   , finalDf['principal component 3']
                   , c = _color
                   , s = 30);
def plot_loading():
    global columns;
    global Data;
    global df;
    global principalComponents;
    global principalDf;
    global complete_Data;
    global column_to_check;
    global loadings;
    split = 30;
    cut = [1,2];
    pc = 1;
    fig = plt.figure(figsize = (12,4))
    ax1 = fig.add_subplot(1,1,1)
    ax1.set_xlabel('frequency variables ');#+ str(split*cut[0]) + ' - ' + str(split*cut[1]), fontsize = 15)
    ax1.set_ylabel('Principal Component '+str(pc) +' load', fontsize = 15)
    ax1.set_title('load plot', fontsize = 20)
    #ax1.bar(list(loadings['PC1'].keys())[split*cut[0]:split*cut[1]],loadings['PC1'][split*cut[0]:split*cut[1]],0.5);
    ax1.bar(list(loadings['PC1'].keys()),loadings['PC'+str(pc)],0.5);
    #ax1.grid();
#    plt.bar(y_pos, height)
#     
#    # Create names on the x-axis
#    plt.xticks(y_pos, bars)
    
        
#    for ind in loadings.index:
#        ax.annotate(ind,(loadings['PC1'][ind], loadings['PC2'][ind]),size=14);
#    for i, txt in enumerate(zip(finalDf['tag and timestamp'],finalDf['tempdev'])):
#        if ((i%50 == 0) or (i ==1)):
#            ax.annotate(txt,(finalDf['principal component 1'][i], finalDf['principal component 2'][i]));
def plot_these(f1='objectN',f2='tempdev',typ  = 'scatter',limitEn = False, lim = 0):
    global complete_Data;
    global loadings;
    finalDf = complete_Data;
    fig = plt.figure(figsize = (8,8))
    ax = fig.add_subplot(1,1,1)
    ax.set_xlabel(f1, fontsize = 15)
    ax.set_ylabel(f2, fontsize = 15)
    ax.set_title(f1 + ' against ' + f2, fontsize = 20)
    if(typ == 'scatter'):
        ax.scatter(finalDf[f1]
                   , finalDf[f2]
                   , s = 10);
    elif(typ == 'line'):
        ax.plot(finalDf[f1]
                   , finalDf[f2]);
        stateDetect = list(map(lambda x: numpi.sqrt(x[0]**2 + x[1]**2 + x[2]**2 + x[3]**2) >= 2.7, 
                               zip(numpi.abs(finalDf['f53']), 
                                numpi.abs(finalDf['f54']),
                                numpi.abs(finalDf['f55']),
                                numpi.abs(finalDf['f56']))));
        #print(stateDetect);
        ax.plot(finalDf[f1], stateDetect)
    if (limitEn):
        first = True;
        ax.plot(finalDf[f1],[lim for i in range(len(finalDf[f1]))], c = 'r');
        for txt, detect, i in zip(finalDf['tag and timestamp'],stateDetect, list(range(len(finalDf[f1])))):
            if ((detect) and (first)):
                first = False;
                ax.annotate(txt,(finalDf[f1][i], stateDetect[i]),size=16);
ing_freq = [];
#for i in range(342):
#    if ((i < 52) or (i>60)):
#        ing_freq.append('f'+str(i));
ignore_columns(['tempdev','rpm','f0']);# *ing_freq]);
activate_colors(True);
check_column('f54');
upload_data_history(19);
#export_csv();
fit_PCA();
#display_PCA();
##genRandDataset(30000);
##fit_PCA();
display_PCA();
display3D_PCA();
#plot_against_freq();
plot_loading();
plot_these('objectN','principal component 1','line', True);
print(pca.explained_variance_ratio_);
print(pca.components_);
#print(numpi.sum( pca.explained_variance_ratio_));
