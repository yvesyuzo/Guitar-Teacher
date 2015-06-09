# -*- coding: utf-8 -*-
"""
Created on Tue Jun  9 11:08:30 2015

@author: Yves Yuzo
"""


import pyaudio
import wave
import numpy as np
import time
import matplotlib.pyplot as plt


def grava_som(NOME, segundos):

    CHUNK = 2048
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    RECORD_SECONDS = segundos
    WAVE_OUTPUT_FILENAME =  str(NOME) + ".wav"
    
    p = pyaudio.PyAudio()
    
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    print('3')
    time.sleep(1)
    print('2')
    time.sleep(1)
    print('1')
    time.sleep(1)                     
    print("* recording")
    time.sleep(1)

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
    
    
    #LEITURA
    
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()


grava_som('jovem2', 3)



