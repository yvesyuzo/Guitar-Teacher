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

conversor_de_frequencia = {'F':range(339, 359)}

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "test.wav"

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
    frames.append(data)

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

chunk = 2048

# open up a wave
wf = wave.open('test.wav', 'rb')
swidth = wf.getsampwidth()
RATE = wf.getframerate()
# use a Blackman window
window = np.blackman(chunk)
# open stream
p = pyaudio.PyAudio()
stream = p.open(format =
                p.get_format_from_width(wf.getsampwidth()),
                channels = wf.getnchannels(),
                rate = RATE,
                output = True)


# read some data
data = wf.readframes (int(chunk/2)) 
# play stream and find the frequency of each chunk
print(len(data), chunk*swidth)
freqs=[]
while len(data) == chunk*swidth:
    
    # write data out to the audio stream
    stream.write(data)
    # unpack the data and times by the hamming window
    indata = np.array(wave.struct.unpack("%dh"%(len(data)/swidth),\
                                         data))*window
    # Take the fft and square each value
    fftData=abs(np.fft.rfft(indata))**2
    # find the maximum
    which = fftData[1:].argmax() + 1
    # use quadratic interpolation around the max
    if which != len(fftData)-1:
        y0,y1,y2 = np.log(fftData[which-1:which+2:])
        x1 = (y2 - y0) * .5 / (2 * y1 - y2 - y0)
        # find the frequency and output it
        thefreq = (which+x1)*RATE/chunk
        print ("The freq is %f Hz." % (thefreq))
        freqs.append(thefreq)
    else:
        thefreq = which*RATE/chunk
        print ("The freq is %f Hz." % (thefreq))
        freqs.append(thefreq)
    # read some more data
    data = wf.readframes (int(chunk/2))
    
print('done')
plt.plot(freqs[1:int(len(freqs)/2)])
plt.grid()
plt.show()

if data:
    stream.write(data)
stream.close()
p.terminate()
