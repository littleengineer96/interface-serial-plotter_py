from ast import While
import os
import time
import serial #pip install PySerial
import numpy as np
import matplotlib.pyplot as plt

# plt.style.use('ggplot')
plt.ion() #habilitando grafico interativo
# x = np.arange(1,6) # vetor de 1 a 6-1 incrementando 1
# dados = np.random.randint(20,30,5) #vetor aleatorio min = 20, max = 20, 5 valores
# # plt.bar(x,dados) # grafico barras
# plt.plot(x,dados)
# plt.pause(3) #tempo em que o grafico fica visivel

# plt.cla() #limpado eixos
# plt.clf() #limpando grafico

# dados = np.random.randint(20,30,5) #vetor aleatorio min = 20, max = 20, 5 valores
# plt.plot(x,dados)
# plt.pause(3)


serialControl = True
gateNumber = 'COM3'
# baudRate = 115200
baudRate = 576000

while serialControl:
    print("Opening Serial Communication...")
    try:
        comPort = serial.Serial(gateNumber, int(baudRate))
        print("Open Serial Communication!\n")
        serialControl = False
    except serial.serialutil.SerialException:
        print("GateError opening Serial Communication!\n")
        gateNumber = input("Insert the COM port number:")
        gateNumber = 'COM' + gateNumber
        baudRate = input('Insert speed(bps):')
    except NameError:
        print("NameError opening Serial Communication!\n")
        gateNumber = input("Insert the COM port number:")
        gateNumber = 'COM' + gateNumber
        baudRate = input('Insert speed(bps):')
    except ValueError:
        print("ValueError opening Serial Communication!\n")
        gateNumber = input("Insert the COM port number:")
        gateNumber = 'COM' + gateNumber
        baudRate = input('Insert speed(bps):')

# vetVrms = [1]*100  #inicializando vetor com tamanho=100 e valor inicial=-1 definidos
# vetFreq = [-1]*100  #inicializando vetor com tamanho e valor inicial definidos 
vetVrms = []
vetFreq = []
vetTime = []
index = 0           #indice para controle dos vetores
indexTotal = 0      #indice geral
timeus = 0
timedata = 0
frequencia = 0
while 1:
    serialData = comPort.readline().decode('utf-8').rstrip()

    if len(serialData):
        if (serialData.startswith("d")) and (serialData.endswith("us")):
            print(str(serialData))
            
            start = 1
            end = serialData.index("V")
            vrms = float(serialData[start:end])

            start = serialData.index("V") + 1 
            end = serialData.index("u")
            timeus = float(serialData[start:end]) 

            print("ID:"+ str(indexTotal) +" Vrms:" + str(vrms) + "V " + str(frequencia) + "Hz " + str(timeus) + "us")

            # if indexTotal <=99:
            #     vetTime.append(indexTotal)
            #     vetVrms.append(vrms)
            #     vetFreq.append(frequencia)
            #     print("indexTotal: " + str(index))

            # else:
            #     #preenchendo os vetores
            #     print("index: " + str(index))
            #     vetVrms[index] = vrms
            #     vetFreq[index] = frequencia
            #     vetTime[index] = indexTotal               #cada incremento equivale a 1 segundo
        
            timedata += timeus
            vetTime.append(timedata/1000) #conversão para ms
            vetVrms.append(vrms)
            vetFreq.append(frequencia)

            indexTotal +=1  
            # index +=1

            # if index == 100:
            #     index = 0
            #     while index < 99:
            #         vetFreq[index] = vetFreq[index + 1] #deslocando todos os elementos uma posição para baixa
            #         vetVrms[index] = vetVrms[index + 1] 
            #         vetTime[index] = vetTime[index + 1]
            #         index +=1
            #     index = 0

            # if indexTotal%10 == 0:
            plt.cla() #limpado eixos
            plt.clf() #limpando grafico
            # plt.ylim([100, 300])
            plt.autoscale()
            plt.title('V/ms')
            plt.ylabel('ddp(V)')
            plt.xlabel('t(ms)')
            plt.plot(vetTime,vetVrms)
            # if index >= 2:
                # timeus = vetTime[indexTotal - 1] - vetTime[indexTotal - 2]
            plt.pause(timeus / 1000000)
            serialData = "" #zerando buffer
        if (serialData.startswith("fr")) and (serialData.endswith("Hz")):

            start = str(serialData).index("f") + 2 
            end = str(serialData).index("H") - 1
            frequencia = str(serialData[start:end]) 

plt.ioff() #desabilitando modo interativo
