# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 13:49:25 2020

@author: oyvin
"""
import pandas as pd;
import random as rand;
import matplotlib.pyplot as plt;
from sklearn.preprocessing import StandardScaler;
from sklearn.decomposition import PCA;
import time as t;
import numpy as numpi;


url = "https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data"
# load dataset into Pandas DataFrame
df = pd.read_csv(url, names=['sepal length','sepal width','petal length','petal width','target']);

print(df);

features = ['sepal length', 'sepal width', 'petal length', 'petal width'];

# Separating out the features
x = df.loc[:, features].values;

print(x);

#seperating out the target
y = df.loc[:,['target']].values

# Standardizing the features
x = StandardScaler().fit_transform(x)


pca = PCA(n_components=2)

principalComponents = pca.fit_transform(x)

principalDf = pd.DataFrame(data = principalComponents
             , columns = ['principal component 1', 'principal component 2'])

finalDf = pd.concat([principalDf, df[['target']]], axis = 1)
print(finalDf)
#
#fig = plt.figure(figsize = (8,8))
#ax = fig.add_subplot(1,1,1) 
#ax.set_xlabel('Principal Component 1', fontsize = 15)
#ax.set_ylabel('Principal Component 2', fontsize = 15)
#ax.set_title('2 component PCA', fontsize = 20)
#targets = ['Iris-setosa', 'Iris-versicolor', 'Iris-virginica']
#colors = ['r', 'g', 'b']
#for target, color in zip(targets,colors):
#    indicesToKeep = finalDf['target'] == target
#    ax.scatter(finalDf.loc[indicesToKeep, 'principal component 1']
#               , finalDf.loc[indicesToKeep, 'principal component 2']
#               , c = color
#               , s = 50)
#ax.legend(targets)
#for i, txt in enumerate(finalDf['target']):
#    #ax.annotate(txt, (z[i], y[i]))
#    ax.annotate(txt,(finalDf['principal component 1'][i], finalDf['principal component 2'][i]));
#print(finalDf);
#ax.grid()
#
#print(pca.explained_variance_ratio_);