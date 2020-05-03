from .CBIRfct import GLCMFE, FEimgtrain, distances, features
import numpy as np
import os
from os import listdir
import pandas as pd
import csv
import numpy as geek


def CBIR(img):

    #******************* calculer les features de l'img *******************

    FEimg = GLCMFE(img)
# print(FEimg)

#******************* lire fichier csv,appliquer minmaxscaler et claculer distacnce *******************
    dataset, X_train, Y_train, X_test = FEimgtrain(FEimg)
# print(X_test)

    dis = []
    for i in range(0, len(X_train)):
        distEucl = distances(X_test, X_train[i])
        dis.append(distEucl)
# print(distEucl)
# print(dis)


#******************* recuperer les noms des img du train dataset *******************
    nam = ['nomimg']
    nomscsv = pd.read_csv(
        'C:\\Users\\Admin\\Desktop\\Nouveau dossier\\imgtrain.csv', names=nam)
    noms = nomscsv['nomimg']
    listnoms = []
    for k in range(0, len(noms)):
        listnoms.append(noms[k])
#print ("\n\n\n\nles noms non triés:\n",listnoms)


#******************* retourner liste des img train trié selon distance ordre croissant *******************

    distrie = sorted(dis)
#print("\n\n\n\nles distances triées:\n",distrie)
    in_arr = geek.array(dis)
    out_arr = geek.argsort(in_arr)
#print("\n\n\n\les indices des distances triées:\n",out_arr)
#print("\n\n\n\nles noms triés:\n", noms[out_arr].tolist())
    images = noms[out_arr].tolist()

#********************** supprimet les features de l'image du fichier csv des features de train **************
# print(dataset)
    dataset = dataset.drop(dataset.index[len(dataset) - 1])
# print(dataset)
    return images[:10]


"""
#********************** inserer les features de l'image dans le fichier csv des features de train **************
with open('featuresbesttrainnew.csv','a',newline='') as f:
	thewriter= csv.writer(f)
	thewriter.writerow(FEimg)
"""
