# -*- coding: utf-8 -*-
"""
Created on Sun Jul  5 13:00:21 2020

@author: Usuario
"""

##################################################################
#                             TAREA 4                            #
##################################################################

##################################################################
# Paso 1'Crear un esquema de modulación BPSK
##################################################################
import pandas as pd
import numpy as np
from scipy import stats
from scipy import signal
from scipy import integrate
import matplotlib.pyplot as plt
#se usa pandas para leer los archivos csv
misbits = pd.read_csv('bits10k.csv',names=['A'],header=None)
bits=misbits['A']

#print(len(bits))
#Parte 1.Esquema de modulación BPSK para los bits presentados
#frecuencia de portadora 5 kHz y N=10000 bits
f=5000 #Hz
N=len(bits)

#se establece el Periodo
T=1/f # 0,2 ms
#se pone un numero de Puntos de muestreo
P=50
# aca se pone los Puntos de muestreo de cada periodo
tp=np.linspace(0,T,P)

#forma de onda de la portadora
seno =np.sin(2*np.pi*f*tp)

#se grafica la onda portadora
plt.plot(tp,seno)
plt.title('Onda portadora')
plt.xlabel('Tiempo(s)')
plt.ylabel('Amplitu de la señal')
plt.ticklabel_format(axis = "x", style = "sci", scilimits=(0,0))
plt.figure(1)
plt.savefig('Onda.png')

#frecuencia de muestreo
fs= P/T #500 kHz
#linea temporal para toda la senal
t = np.linspace(0,N*T,N*P)
#Inicializador
senal= np.zeros(t.shape)
#Creacion de la senal modulada BPSK
for i,b in enumerate(bits):
    if b==1:
        senal[i*P:(i+1)*P]=b*seno
    else:
        senal[i*P:(i+1)*P]=-seno
           
##se grafica para los primeros bits modulados
plt.figure(2)
plt.plot(senal[0:5*P])
plt.xlabel('Tiempo(s)')
plt.ylabel('Amplitu de la señal')
plt.title('Señal modulada para los primeros 5 bits')
plt.show()

#######################################################################
#PARTE 2 
#######################################################################

#potencia instantanea 
Pins=senal**2

#potencia promedio
Prom=integrate.trapz(Pins,t)/(N*T)
print('Potencia promedio en watts:', Prom,'W')


#este corresponde al PUNTO 4 pero tiene que ir aca por orden antes del ruido
# Antes del canal ruidoso
fw, PSD = signal.welch(senal, fs, nperseg=1024)
plt.figure(4)
plt.semilogy(fw, PSD)
plt.title ('Densidad espectral antes del canal ruidoso')
plt.xlabel('Frecuencia / Hz')
plt.ylabel('Densidad espectral de potencia / V**2/Hz')
plt.show()


#######################################################################
#PARTE 3 generacion de un canal ruidoso  
#######################################################################

# Relación señal-a-ruido deseada
SNR = range(-4,2)#se cambia el intrvalo ORIGINAL para visualizar mejor los errores 
BER=[]
for snr in SNR:
    # Potencia del ruido para SNR y potencia de la señal dadas
    Pn = Prom / (10**(snr / 10))

    # Desviación estándar del ruido
    sigma = np.sqrt(Pn)

    # Crear ruido (Pn = sigma^2)
    ruido = np.random.normal(0, sigma, senal.shape)

    # Simular "el canal": señal recibida
    Sr = senal + ruido

    # se grafican el canal ruisodo de los primeros bits recibidos
    pb = 5 #primeros bits 
    plt.figure(3)
    plt.plot(Sr[0:pb*P])
    plt.title('AWGN de {} dB para los primeros 5 bits'.format(snr))
    plt.xlabel('Tiempo(s)')
    plt.ylabel('Amplitu de la señal')
    plt.show()

    #######################################################################
    #PARTE 4 GRAFICAS DE DENSIDAD 
    ######################################################################

    
    #Grafica de densida Después del canal ruidoso
    fw, PSD = signal.welch(Sr, fs, nperseg=1024)
    plt.figure(5)
    plt.semilogy(fw, PSD)
    plt.title ('Densidad espectral despues del canal ruidoso para {} dB'.format(snr))
    plt.xlabel('Frecuencia / Hz')
    plt.ylabel('Densidad espectral de potencia / V**2/Hz')
    plt.show()
    #por error de orden  en el enunciado se generan 6 graficas una para cada 
    # SNR pero solo se pone una por recomedacion del profesor 

    #######################################################################
    #PARTE 5 Calculos de error y tasa de error
    #######################################################################

    # Pseudo-energía de la onda original (esta es suma, no integral)
    Es = np.sum(seno**2)
    # Inicialización del vector de bits recibidos
    bitsSr = np.zeros(bits.shape)

    # Decodificación de la señal por detección de energía
    for i, b in enumerate(bits):
        Ep = np.sum(Sr[i*P:(i+1)*P] * seno)
        if Ep > Es/2:
            bitsSr[i] = 1
        else:
            bitsSr[i] = 0  
    #Se clculan los erroes y la tasa de error de los 10k bits para cada SNR      
    err = np.sum(np.abs(bits - bitsSr))
    BER.append(err/N)# SE HACE UN VECTOR DE BER 
    print('Hay un total de {} errores en {} bits para una tasa de error de {} para el SNR de {}'.format(err, N, err/N, snr))

#######################################################################
#PARTE 6 grafcar versus
#######################################################################

#grafica la la recion de snr con BER 
plt.semilogy(SNR, BER)
plt.title("SNR vrs BER")
plt.xlabel('SNR')
plt.ylabel('BER ')
plt.show()