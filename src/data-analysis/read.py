import serial
import time
import sys
import numpy as np
import matplotlib.pyplot as plt
from collections import deque
from matplotlib.animation import FuncAnimation

max_data = 100
xtick = np.arange(max_data)
data = np.zeros((max_data,3))

plt.ion()    
figure, ax = plt.subplots(3)
(lineX,) = ax[0].plot(xtick, data[:,0])
(lineY,) = ax[1].plot(xtick, data[:,1])
(lineZ,) = ax[2].plot(xtick, data[:,2])

def update_data(str_data: str):
    global data
    data_list = str_data.decode('utf-8').strip().split(',')
    try:
        append_data = np.array([float(n) for n in data_list]) if len(data_list) == 3 else np.zeros(3)
    except ValueError:
        print(f'Error converting {data_list} to float, skipping.', file=sys.stderr)
        return
    
    data = np.roll(data, -1, axis=0)
    data[-1,:] = append_data

def plot():
    lineX.set_data(xtick, data[:,0])
    lineY.set_data(xtick, data[:,1])
    lineZ.set_data(xtick, data[:,2])
    ax[2].set_ylim([np.min(data[:,2]), np.max(data[:,2])])
    figure.canvas.draw()
    figure.canvas.flush_events()

with serial.Serial('/dev/ttyACM0', 
                     115200,  
                     xonxoff = False, 
                     rtscts = False, 
                     bytesize = serial.EIGHTBITS, 
                     parity = serial.PARITY_NONE, 
                     stopbits = serial.STOPBITS_ONE,
                     timeout=1) as ser:
    with open('acc.csv', 'w') as f:
        while True:
            fline = ser.readline()
            try:
                print(fline.decode('utf-8'), file=f, end='')
                # update_data(fline)
                # plot()
            except UnicodeDecodeError:
                print(f'Error decoding UTF-8 from {fline}, skipping.', file=sys.stderr)

