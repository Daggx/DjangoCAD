import SimpleITK as sitk
import numpy as np
from numpy import newaxis
from radiomics import featureextractor
from skimage import io
import warnings
import hdf5storage
import os
from os import listdir
from PIL import Image
import imageio
import pandas as pd
from sklearn.preprocessing import MinMaxScaler,minmax_scale
from scipy.spatial import distance
import numpy as geek 



def GLCMFE(img):#,path,i):
	image = img.path
	i = img.name
	i = i.replace('jpg','mat')
	ik = i.replace('irm_pics/','C:\\Users\\Admin\\Desktop\\Nouveau dossier\\BDDMAT\\')
	f1 = hdf5storage.loadmat(ik)
	mask=(f1['cjdata'][0][4]).astype('int')
	mask[mask==1]=255
	settings = {'label': 255}
	image=io.imread(image)
	#mask=io.imread(mask)
	imo = sitk.GetImageFromArray(image)
	mask = sitk.GetImageFromArray(mask)
	extractor = featureextractor.RadiomicsFeatureExtractor(**settings)
	extractor.disableAllFeatures()
	extractor.enableFeaturesByName(firstorder=['Energy','Entropy','Kurtosis','Mean','Skewness','Variance'],glcm=['ClusterProminence','ClusterShade','Contrast','Correlation','DifferenceAverage','DifferenceEntropy','DifferenceVariance','Idm','SumAverage','SumEntropy'])
	result = extractor.execute(imo, mask)
	features=[]
	for key, value in result.items():
		if(key.startswith('original')):
			features.append(value)
	features=np.asarray(features)
	F=[]
	for i in range(0,len(features)):
		F.append(features[i])
	features=F
	return features


def FEimgtrain(FEimg):
	names=['Energy','Entropy','Kurtosis','Mean','Skewness','Variance','ClusterProminence','ClusterShade','Contrast','Correlation','DifferenceAverage','DifferenceEntropy','DifferenceVariance','Idm','SumAverage','SumEntropy','tumeur']
	dataset = pd.read_csv('C:\\Users\\Admin\\Desktop\\Nouveau dossier\\featuresbesttrainnew.csv',names=names)
	#print(dataset)
	#print(dataset)
	df1 = pd.DataFrame({'Energy':[FEimg[0]], 'Entropy':[FEimg[1]],'Kurtosis':[FEimg[2]],'Mean':[FEimg[3]],'Skewness':[FEimg[4]],'Variance':[FEimg[5]],'ClusterProminence':[FEimg[6]],'ClusterShade':[FEimg[7]],'Contrast':[FEimg[8]],'Correlation':[FEimg[9]],'DifferenceAverage':[FEimg[10]],'DifferenceEntropy':[FEimg[11]],'DifferenceVariance':[FEimg[12]],'Idm':[FEimg[13]],'SumAverage':[FEimg[14]],'SumEntropy':[FEimg[15]]}, index = [2146])
	#print(df1)
	dataset=pd.concat([dataset, df1])
	#print(dataset)

	std_scalertrain = MinMaxScaler().fit(dataset[['Energy','Entropy','Kurtosis','Mean','Skewness','Variance','ClusterProminence','ClusterShade','Contrast','Correlation','DifferenceAverage','DifferenceEntropy','DifferenceVariance','Idm','SumAverage','SumEntropy']])
	df_stdtrain = std_scalertrain.transform(dataset[['Energy','Entropy','Kurtosis','Mean','Skewness','Variance','ClusterProminence','ClusterShade','Contrast','Correlation','DifferenceAverage','DifferenceEntropy','DifferenceVariance','Idm','SumAverage','SumEntropy']])
	X=df_stdtrain
	#print(X)
	Y=dataset['tumeur']

	X_train=[]
	Y_train=[]
	for i in range(0,2146):
		X_train.append(X[i])
		Y_train.append(int(Y[i]))
	#print(X_train)
	#print(Y_train)
	X_test=[]
	for i in range(2146,len(X)):
		X_test.append(X[i])
	#print(X_test)
	return(dataset,X_train,Y_train,X_test)


def distances(a,b):
	distEucl = distance.euclidean(a, b)
	return distEucl


def features():
	names=['Energy','Entropy','Kurtosis','Mean','Skewness','Variance','ClusterProminence','ClusterShade','Contrast','Correlation','DifferenceAverage','DifferenceEntropy','DifferenceVariance','Idm','SumAverage','SumEntropy','tumeur']
	dataset2 = pd.read_csv('C:\\Users\\Admin\\Desktop\\Nouveau dossier\\featuresbesttrainnew.csv',names=names)
	X_test=(dataset2[['Energy','Entropy','Kurtosis','Mean','Skewness','Variance','ClusterProminence','ClusterShade','Contrast','Correlation','DifferenceAverage','DifferenceEntropy','DifferenceVariance','Idm','SumAverage','SumEntropy']])
	Y_test=dataset2['tumeur']
	#a=X_test[5]
	#print(a)
	return (X_test,Y_test)