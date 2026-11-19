# -*- coding: utf-8 -*-
# Program za sniamnje podataka tijekom deset sekundi i njihovo prikazivanje na
#grafu
import serial
import time
import matplotlib.pyplot as plt
import numpy as np
import datetime
#import scipy.fftpack
import matplotlib.dates as mdates
def waitResponse(char):
    # Čekanje potvrde od Arduina dok prikuplja podatke sa ADC-a
    while 1:
        print 'Waiting...'
        time.sleep(0.2)
        ser.write(char)
        if "Response" in ser.readline():
            break
# duljina snimanja
test_time = 10.0
# omogućiti FFT graf
fft_enable = False
# Inicijalizacija serijske komunikacije (Port, brzina)
ser = serial.Serial('COM3', 115200)
# Čekanje za inicijalizaciju
time.sleep(2)
# Otvaranje bloka za podatke
waitResponse("1")
# Čekanje da se otvori blok za podatke
time.sleep(2)
print 'Connected!'
data_array = np.array([], dtype=np.uint16)
#times_array = np.array([], dtype=np.float32)
times_array = np.array([])
counter = 0
ser.flushInput()
first_read = True 
while 1:
    #start_time = time.clock()
    if not first_read:
        if (time.clock() - test_start >= test_time):
            break
    try:
        b1 = ord(ser.read(1))
        b2 = ord(ser.read(1))
    except:
        continue
    # Sastavljanje prave vrijednosti 16-bitnog podatka koji je poslan u 2 dijela serijskom komunikacijom
    serial_value = b1 + b2*256
    if serial_value != '':
        if first_read:
            first_read = False
            test_start = time.clock()
            print 'start', test_start
        #print serial_value
        # Dodavanje vrijednosti u listu podataka
        try:
            # Numpy arrays
            #data_array = np.append(data_array, [4096-serial_value])
            data_array = np.append(data_array, [serial_value])
            #times_array = np.append(times_array, [counter])
            times_array = np.append(times_array, [datetime.datetime.utcnow()])
            counter += 1
        except:
            print 'Error!'
            print serial_value
            break
        # dodavanje vremena na listu
test_duration = time.clock() - test_start
print 'Ending data capture'
# zatvaranje bloka za podatke
waitResponse('0')
# Zatvaranje serijske komunikacije
ser.close()
# Uzorci u sekundi
sps = len(data_array) / test_duration
print 'Izračunato SPS: ', sps
print data_array[0:10]
print 'max:', max(data_array)
# Plot data
if fft_enable:
    fig, ax = plt.subplots()
    fig.subplots_adjust(hspace=.3)
    plt.subplot(2, 1, 1)
# Koordinatne osi
plt.title('Svjetlosna krivulja')
plt.xlabel('Vrijeme (s)')
plt.ylabel('ADU')
plt.plot(times_array, data_array)
plt.ylim((0, 256*256))
# omogućiti krivulju i odabrati format podataka za graf
myFmt = mdates.DateFormatter('%S')
ax = plt.gca()
ax.xaxis.set_major_formatter(myFmt)
ax.grid(True)
# FFT
if fft_enable:
    plt.subplot(2, 1, 2)
    plt.title('FFT')
    plt.xlabel('Frekvencija (Hz)')
    plt.ylabel('Amplituda')
    # Broj točaka uzoraka
    N = len(data_array)
    # razmak uzoraka
    T = 1.0 / sps
    x = np.linspace(0.0, N*T, N)
    y = data_array
    yf = scipy.fftpack.fft(y)
    xf = np.linspace(0.0, 1.0/(2.0*T), N/2)
    fft_amplitude = 2.0/N * np.abs(yf[0:N/2])
    plt.plot(xf, fft_amplitude)
    plt.ylim((0, max(fft_amplitude[5:])))
plt.show()
