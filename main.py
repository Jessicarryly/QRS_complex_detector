import wfdb
import matplotlib.pyplot as plt
import pywt
import numpy as np
import csv
import os
import sys

def resetOfTabValues(tab,decompositionLevel):
    i = 0
    while (i < 3):
        tab[decompositionLevel-i] *= 0
        i = i +1
    return tab

def showSignals(tab, title, annotations=None, bpm=None):
    fig, ax = plt.subplots(3, 1)
    fig1,ax1 = plt.subplots(3,1)
    ax[0].plot(tab[0])  # db10  level=6
    ax[1].plot(tab[1])  # bior2.2 level=6
    ax[2].plot(tab[2])  # sym12 level=6
    ax1[0].plot(tab[3])  # db10  level=7
    ax1[1].plot(tab[4])  # bior2.2 level=7
    ax1[2].plot(tab[5])  # sym12 level=7
    ax[0].set_xlim(0, 2500)
    ax[1].set_xlim(0, 2500)
    ax[2].set_xlim(0, 2500)
    ax1[0].set_xlim(0, 2500)
    ax1[1].set_xlim(0, 2500)
    ax1[2].set_xlim(0, 2500)
    ax[0].set_xlabel('Probka[N]')
    ax[0].set_ylabel('Amplituda')
    ax[1].set_xlabel('Probka[N]')
    ax[1].set_ylabel('Amplituda')
    ax[2].set_xlabel('Probka[N]')
    ax[2].set_ylabel('Amplituda')
    ax1[0].set_xlabel('Probka[N]')
    ax1[0].set_ylabel('Amplituda')
    ax1[1].set_xlabel('Probka[N]')
    ax1[1].set_ylabel('Amplituda')
    ax1[2].set_xlabel('Probka[N]')
    ax1[2].set_ylabel('Amplituda')
    ax[0].set_title(title+' wavelet: db10, level=6')
    ax[1].set_title(title+' wavelet: bior2.2, level=6')
    ax[2].set_title(title+' wavelet: sym12, level=6')
    ax1[0].set_title(title+' wavelet: db10, level=7')
    ax1[1].set_title(title+' wavelet: bior2.2, level=7')
    ax1[2].set_title(title+' wavelet: sym12, level=7')


    if annotations != None and bpm != None:
        yValue = tab[0][annotations[0][0]]
        ax[0].annotate(s='QRS', xy=(annotations[0][0], yValue),
                       xytext=(annotations[0][0], yValue + 0.2),
                       arrowprops=dict(facecolor='black', shrink=0.05))
        yValue = tab[1][annotations[1][0]]
        ax[1].annotate(s='QRS', xy=(annotations[1][0], yValue),
                       xytext=(annotations[1][0], yValue + 0.2),
                       arrowprops=dict(facecolor='black', shrink=0.05))
        yValue = tab[2][annotations[2][0]]
        ax[2].annotate(s='QRS', xy=(annotations[2][0], yValue),
                       xytext=(annotations[2][0], yValue + 0.2),
                       arrowprops=dict(facecolor='black', shrink=0.05))
        yValue = tab[3][annotations[3][0]]
        ax1[0].annotate(s='QRS', xy=(annotations[3][0], yValue),
                       xytext=(annotations[3][0], yValue + 0.2),
                       arrowprops=dict(facecolor='black', shrink=0.05))
        yValue = tab[4][annotations[4][0]]
        ax1[1].annotate(s='QRS', xy=(annotations[4][0], yValue),
                       xytext=(annotations[4][0], yValue + 0.2),
                       arrowprops=dict(facecolor='black', shrink=0.05))
        yValue = tab[5][annotations[5][0]]
        ax1[2].annotate(s='QRS', xy=(annotations[5][0], yValue),
                       xytext=(annotations[5][0], yValue + 0.2),
                       arrowprops=dict(facecolor='black', shrink=0.05))
        for i in range(0,3):
            for j in range(1,len(annotations[i])):
                yValue = tab[i][annotations[i][j]]
                ax[i].annotate(s='QRS BPM:'+str(round(bpm[i][j-1], 2)), xy=(annotations[i][j], yValue),
                             xytext=(annotations[i][j], yValue + 0.2),
                             arrowprops=dict(facecolor='black', shrink=0.05))

        for i in range(3,6):
            for j in range(1,len(annotations[i])):
                yValue = tab[i][annotations[i][j]]
                ax1[i%3].annotate(s='QRS, BPM:'+str(round(bpm[i][j-1], 2)), xy=(annotations[i][j], yValue),
                             xytext=(annotations[i][j], yValue + 0.2),
                             arrowprops=dict(facecolor='black', shrink=0.05))

    plt.show()

def thresholding(signal):
    for i in range(0,len(signal)):
        if signal[i] < -0.60:
            signal[i] = -0.60
    return signal

def waveletTransform(signal):
    tabOfSignals = []
    for i in range(0, 2):
        for j in range(0, 3):
            tree = pywt.wavedec(signal1, wavelets[j], level=decompositionLevel[i])
            tree = resetOfTabValues(tree, decompositionLevel[i])
            recSignal = pywt.waverec(tree, wavelets[j])
            recSignal = thresholding(recSignal)
            tabOfSignals.append(recSignal)
    return tabOfSignals

def createAnnotations(signal):
    tabOfAnnotation = []
    space = 150
    for i in range(1,len(signal)):
        if signal[i] > 0:
            if signal[i] > signal[i-1] and signal[i] > signal[i+1]:
                if len(tabOfAnnotation) == 0 or i - tabOfAnnotation[-1] > space:
                    tabOfAnnotation.append(i)
                elif signal[tabOfAnnotation[-1]] < signal[i]:
                        tabOfAnnotation[-1] = i
    return tabOfAnnotation

def getBPM(QRS):
    bpm = []
    for i in range(0,len(QRS)-1):
        difference = QRS[i+1] - QRS[i]
        difference /= record.fs
        difference = 60/difference
        bpm.append(difference)
    return bpm

def getSample(second):
    fs = record.fs
    sample = second * fs
    return sample

def annotationValidate(annotations):
    isHit = False
    TP = 0
    FP = 0
    FN = 0
    for i in range(1,len(annotation.annsamp)):
        for j in range(0,len(annotations)):
            if annotation.annsamp[i] - getSample(0.150) < annotations[j] and annotation.annsamp[i] + getSample(0.150) > annotations[j]:
                if isHit == False:
                    isHit = True
                    TP += 1
                else:
                    FP += 1
            elif annotations[j] > annotation.annsamp[i] + getSample(0.150):
                break;
        if isHit == False:
            FN += 1
        isHit = False
    Se = TP / (TP + FN)
    Px = TP / (TP + FP)
    Delta = 0;
    for i in range(1, len(annotation.annsamp)):
        for j in range(0, len(annotations)):
            if annotation.annsamp[i] - getSample(0.150) < annotations[j] and annotation.annsamp[i] + getSample(0.150) > \
                    annotations[j]:
                Delta += (annotation.annsamp[i] + getSample(0.150) - annotations[j])
            elif annotations[j] > annotation.annsamp[i] + getSample(0.150):
                break;

    Delta /= TP
    print('TP: '+str(TP))
    print('FP: '+str(FP))
    print('FN: '+str(FN))
    print('Se: '+str(round(Se,2)))
    print('Px: '+str(Px))
    print('Delta: '+str(round(Delta,3)))

    tabOfValues = [TP, FP, FN, round(Se,2),Px, round(Delta,3)]
    return tabOfValues

def saveToCSV(annotations,bpm,fileName):
    with open('csvFiles/'+fileName,'w', newline='') as file:
        a = csv.writer(file,delimiter=";")
        data =[]
        data.append([str(annotations[0]), 'Brak obliczen dla pierwszego QRS'])
        for i in range(1,len(annotations)):
            data.append([str(annotations[i]), str(round(bpm[i-1]))])
        a.writerows(data)
        file.close()

def saveValidateToCsv(ValuesOfValidate, fileName):
    with open('csvFiles/'+fileName, 'w', newline='') as file:
        a = csv.writer(file,delimiter=";")
        data = []
        j =0
        data.append(['File',ekgFileName])
        for i in range(0,len(ValuesOfValidate)):
            data.append([wavelets[i%3],'Level',str(decompositionLevel[j])])
            data.append(['TP', ValuesOfValidate[i][0]])
            data.append(['FP', ValuesOfValidate[i][1]])
            data.append(['FN', ValuesOfValidate[i][2]])
            data.append(['Se', ValuesOfValidate[i][3]])
            data.append(['Px', ValuesOfValidate[i][4]])
            data.append(['Delta', ValuesOfValidate[i][5]])
            if i == 2:
                j+=1
        a.writerows(data)
        file.close()

ekgFileName = ''
if len(sys.argv) > 1:
    ekgFileName = str(sys.argv[1])
else:
    ekgFileName = '100'
print('Wyswietlenie obu sygnalow...')
record = wfdb.rdsamp(ekgFileName,sampto=3000)
annotation = wfdb.rdann(ekgFileName,'atr',sampto=3000)
wfdb.plotrec(record,annotation=annotation,title='Część pliku: '+ekgFileName,)
record = wfdb.rdsamp(ekgFileName)
annotation = wfdb.rdann(ekgFileName,'atr')

if ekgFileName == '100':
    drainName1 = 'MLII'
    drainName2 = 'V5'
elif ekgFileName == '113' or ekgFileName == '231':
    drainName1 = 'MLII'
    drainName2 = 'V1'
else:
    drainName1 = 'indefinite'
    drainName2 = 'indefinite'



signal1 = []
signal2 = []
for i in range(0,record.siglen):
    signal1.append(record.p_signals[i][0])
    signal2.append(record.p_signals[i][1])

wavelets = ['db10', 'bior2.2', 'sym12']
decompositionLevel = [6,7]
print("Tranformacja falkowa....")
tabOfSignals1 = waveletTransform(signal1)
tabOfSignals2 = waveletTransform(signal2)
print("Wyswietlenie sygnalow po tranformacji falkowej...")
showSignals(tabOfSignals1, drainName1)
showSignals(tabOfSignals2, drainName2)

annotationsForSignals1 = []
annotationsForSignals2 = []
for i in range(0,len(tabOfSignals1)):
    annotationsForSignals1.append(createAnnotations(tabOfSignals1[i]))
for i in range(0,len(tabOfSignals2)):
    annotationsForSignals2.append(createAnnotations(tabOfSignals2[i]))

bpmForSignal1 = []
bpmForSignal2 = []

for i in range(0,len(annotationsForSignals1)):
    bpmForSignal1.append(getBPM(annotationsForSignals1[i]))
for i in range(0, len(annotationsForSignals2)):
    bpmForSignal2.append(getBPM(annotationsForSignals2[i]))

print("Wyswietlenie sygnalow z adnotacjami oraz wartosciami bpm...")
showSignals(tabOfSignals1,drainName1,annotationsForSignals1, bpmForSignal1)
showSignals(tabOfSignals2,drainName2, annotationsForSignals2, bpmForSignal2)


os.makedirs('csvFiles',exist_ok=True)
print("Zapisanie wartosci adnotacji i BPM do pliku csv")
z = 0
for i in range(0,len(tabOfSignals1)):
    saveToCSV(annotationsForSignals1[i],bpmForSignal1[i], 'csv_'+str(z+1)+"_Plik_"+ekgFileName+".csv")
    z += 1
for i in range(0, len(tabOfSignals2)):
    saveToCSV(annotationsForSignals2[i], bpmForSignal2[i], 'csv_'+str(z+1)+"_Plik_"+ekgFileName+".csv")
    z += 1

valuesOfAnnotationValidate = []
print("Obliczanie wartosci sprawdzajacych poprawnosc lokalizacji adnotacji...")
for i in range(0,len(annotationsForSignals1)):
    valuesOfAnnotationValidate.append(annotationValidate(annotationsForSignals1[i]))

print("Zapisanie wartosci poprawnosci adnotacji do pliku csv...")
saveValidateToCsv(valuesOfAnnotationValidate,"wartosciKoncowe_pliku_"+ekgFileName+".csv")