
import numpy as np
import csv
from os import listdir
from os.path import isfile, join
#start loop
#open file
#convert to Lose unimportant info
#write to .CSV

#Took 54 mins to run through 415 files for max's data


DataFile = open("/home/user/Desktop/Data/Max Data/DataTXT.txt","w")
InfoFile = open("/home/user/Desktop/Data/Max Data/InfoTXT.txt","w")



mypath = "/home/user/Desktop/Data/Max Data/Max data set 2 (Big boy time)"
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
print(onlyfiles)


for i in range(len(onlyfiles)):
    Data = open("/home/user/Desktop/Data/Max Data/Max data set 2 (Big boy time)/"+onlyfiles[i],"r")


    for count, line in enumerate(Data):
            pass
    print('Total Lines', count + 1)
    noofdatapoints = count

    Data.close()

    Dimensions = []

    infoLines = []
    dataLines = []

    Data = open("/home/user/Desktop/Data/Max Data/Max data set 2 (Big boy time)/large_cascade6400eV.0.vox64.xyz","r")
        
    count = 0 #count reset

    for z in Data:
        Lines = z
        if count<=1:
            infoLines.append(Lines)
            count+=1
        elif count<= noofdatapoints:
            dataLines.append(Lines)
            count+=1
        else:
            pass

    # for i in range(0, noofdatapoints-2):
    #         DataFile.write(dataLines[i])
    # for x in range(2):
    #         InfoFile.write(infoLines[x])

    DataLength = len(dataLines)


    X_Positions = []
    Y_Positions = []
    Z_Positions = []
    ScalarStrainFactor = []

    positionSplit = []

    for j in range(DataLength):
        position = dataLines[j]
        x = 2

        positionSplit = position.split(" ")

        # print(positionSplit)
        # print(positionSplit)
        Xposition = positionSplit[x]
        Yposition = positionSplit[x+2]
        Zposition = positionSplit[x+4]
        X_Positions.append(Xposition)
        Y_Positions.append(Yposition)
        Z_Positions.append(Zposition)
        
        for x in positionSplit:
            if len(x)<4:
                positionSplit.remove(x)
        
        vonMises = positionSplit[10]
        VonMisesString = vonMises.split("\n")
        ScalarStrainFactor.append(VonMisesString[0])

    ConvertedFile = open("/home/user/Desktop/Data/Max Data/ConvertedData/Converted - "+onlyfiles[i]+".csv","w")
    writer = csv.writer(ConvertedFile)
    Row = []
    ConvertedFile.write("X Position" + "," + "Y Position" + "," + "Z Position" + "," + "Strain Scaling Factor" + "\n")

    count = 0

    print("X - " + str(len( X_Positions)))
    print("Y - " + str(len(Y_Positions)))
    print("Z - " + str(len(Z_Positions)))
    print("Strain - " + str(len( ScalarStrainFactor)))
    for x in range(DataLength):
        Row = str(X_Positions[x]) + "," + str(Y_Positions[x]) + "," + str(Z_Positions[x]) + "," + str(ScalarStrainFactor[count])  + "\n"

        count+=1
        ConvertedFile.write(Row)

    count = 0
        
    ConvertedFile.close()