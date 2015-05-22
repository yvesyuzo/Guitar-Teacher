# -*- coding: utf-8 -*-
"""
Created on Fri May 22 08:21:41 2015

@author: Yves Yuzo
"""

# -*- coding: utf-8 -*-
"""
Created on Wed May 13 07:28:37 2015

@author: Yves Yuzo
"""

import pyaudio
import wave
import numpy as np
import time
import matplotlib.pyplot as plt
from Testes import*

conversor_de_frequencia = {'F':range(339, 359)}

CHUNK = 512
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 8192
RECORD_SECONDS = 0
WAVE_OUTPUT_FILENAME = "0.wav"

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)
print("* recording")
time.sleep(1)
print ('inicio')
frames = []

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    print('data:',len(data))
    print('type data ',type(data))
    frames.append(data)

print('frames:',len(frames))
print("* done recording")

stream.stop_stream()
stream.close()
p.terminate()



wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()

# open up a wave
wf = wave.open('La.wav', 'rb')
swidth = wf.getsampwidth()
print('swidth',swidth)
RATE = wf.getframerate()

# use a Blackman window
window = np.blackman(CHUNK)

# open stream
p = pyaudio.PyAudio()
stream = p.open(format =
                p.get_format_from_width(wf.getsampwidth()),
                channels = wf.getnchannels(),
                rate = RATE,
                output = True)


# read some data
data = wf.readframes (int(CHUNK)) 
# play stream and find the frequency of each chunk
print(len(data), CHUNK*swidth)
freqs=[]
while len(data) == int(CHUNK)*swidth:
    
    # write data out to the audio stream
    stream.write(data)
    # unpack the data and times by the hamming window
    #try:
    indata = np.array(wave.struct.unpack("%dh"%(len(data)/swidth),data))*window
    print("Indata ok")
    
    # Take the fft and square each value
    fftData=abs(np.fft.rfft(indata))**2
    # find the maximum
    which = fftData[1:].argmax() + 1
    # use quadratic interpolation around the max
    if which != len(fftData)-1:
        y0,y1,y2 = np.log(fftData[which-1:which+2:])
        x1 = (y2 - y0) * .5 / (2 * y1 - y2 - y0)
        # find the frequency and output it
        thefreq = (which+x1)*RATE/CHUNK
        print ("The freq is %f Hz." % (thefreq))
        freqs.append(thefreq)
    else:
        thefreq = which*RATE/CHUNK
        print ("The freq is %f Hz." % (thefreq))
        freqs.append(thefreq)
    # read some more data
    data = wf.readframes (int(CHUNK))
    print ("------chunk ok ------")
#    except:
#        indata = None        
#        print ("Not enough data")
    
print('done')

print (type(freqs))

plt.plot(freqs[int(len(freqs)*0.1):int(len(freqs)*0.9)])
plt.grid()
plt.show()

#plt.plot(freqs)
#plt.grid()
#plt.show()

if data:
    stream.write(data)
stream.close()
p.terminate()

