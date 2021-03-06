# -*- coding: utf-8 -*-
"""
Created on Tue Jun  9 11:08:30 2015

@author: Yves Yuzo
"""


import pyaudio
import wave
import numpy as np
import time



#CHUNK = 2048
#FORMAT = pyaudio.paInt16
#CHANNELS = 1
#RATE = 44100
#p = pyaudio.PyAudio()





def grava_som(NOME, segundos):
      
    
    RATE = 44100                # Frequencias em Hz da quantidade de dados colhidos por segundo
    CHUNK = 2048                # numero de vezes em que cada dado do RATE sera dividido para analise individual
    FORMAT = pyaudio.paInt16
    CHANNELS = 1    
    RECORD_SECONDS = segundos
    WAVE_OUTPUT_FILENAME =  str(NOME) + ".wav" # adiciona a extenção .wav para o NOME de entrada da função para conseguir salvar o audio
    
    p = pyaudio.PyAudio()
    
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

#Começa a gravar
    frames = []
    
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):#(RATE / CHUNK * RECORD_SECONDS) é o numero de analizes total
        data = stream.read(CHUNK) #data é do tipo 'bytes' e tem o len = 4096 

        frames.append(data)    
#    print('frames:',len(frames))
#    print(RATE / CHUNK * RECORD_SECONDS)
#    print("* done recording")
    
    stream.stop_stream()
    stream.close()     #Para de gravar
    p.terminate()
    
    
    #LEITURA
    
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    
    return frames
    



def analiza_som (NOME, notas_freq):

    CHUNK = 2048
    RATE = 44100 
    
    p = pyaudio.PyAudio()    
    
#    threshold = 36000000000 # amplitude dos ruidos
    threshold = 0
        
    # open up a wave
    wf = wave.open( (NOME + '.wav'), 'rb')
    swidth = wf.getsampwidth() #swidth = 2
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
    #print(len(data), CHUNK*swidth)
    
    freqs = []
        
        
    while len(data) == int(CHUNK)*swidth:
        
        # write data out to the audio stream
        #stream.write(data)
        # unpack the data and times by the hamming window
        #try:
        indata = np.array(wave.struct.unpack("%dh"%(len(data)/swidth),data))*window
#        print("Indata ok")
        
        # Take the fft and square each value
        #
        fftData= abs(np.fft.rfft(indata))**2# Pega o eixo imaginario e o real e retorna a magnitude(hipotenusa, amplitude)
        # find the maximum
        which = fftData[1:].argmax() + 1
    
    #    print("fft data: ", fftData[which])
        
        
        if fftData[which] > threshold:
                
            # use quadratic interpolation around the max
            if which != len(fftData)-1:
                y0,y1,y2 = np.log(fftData[which-1:which+2:])
                x1 = (y2 - y0) * .5 / (2 * y1 - y2 - y0)
                # find the frequency and output it
                thefreq = (which+x1)*RATE/CHUNK
#                print ("The freq is %f Hz." % (thefreq))
                freqs.append(thefreq)
            else:
                thefreq = which*RATE/CHUNK
#                print ("The freq is %f Hz." % (thefreq))
                freqs.append(thefreq)
            # read some more data
            data = wf.readframes (int(CHUNK))
#            print ("------chunk ok ------")
            
        data = wf.readframes (int(CHUNK))
            

#    print('done')
#    
#    print('As freqs são:')
#    for i in freqs:
#        print(i)
#    
#    print("O len das freqs é: ", len(freqs))
#    print (type(freqs))
#    print(freqs)
    
    if data:
        stream.write(data)
    stream.close()
    p.terminate()
    
    notas = []
    
    for x in freqs:
        
        notas_temp = [i for i in notas_freq if int(x) in range(notas_freq[i][0],notas_freq[i][2])]
        if notas_temp != []:
            notas.append(notas_temp)
        
    return notas
    
    
    

    
    
#def conversor_freq_nota(lista_de_freqs, notas_freq):
#    
#    notas = []
#    for x in lista_de_freqs:
#        
#        notas_temp = [i for i in notas_freq if int(x) in range(notas_freq[i][0],notas_freq[i][2])]
#        if notas_temp != []:
#            notas.append(notas_temp)
#        
#    return notas
    
notas_freq = {'E4': [312,329,348],'B3': [234,247,261],'G3': [185,196,208],
              'D3': [140,147,155],'A2': [105,110,116],'E2': [78,82,86], 'A4': [416, 440, 465]}


#tempo1 = time.time()
#
#Teste = grava_som('feroz2', 1)
#
#tempo2 = time.time()       
#    
#banana = analiza_som('feroz2')
#print(banana)
#
#tempo3 = time.time()
#
#batata = conversor_freq_nota (banana, notas_freq)
#
#print(batata)
#
#tempo4 = time.time()
#
#
#tempo_grava = tempo2 - tempo1
#tempo_analiza = tempo3 - tempo2
#tempo_converte = tempo4 - tempo3
#
#print('grava som demora ',tempo_grava )
#print('analiza demora ', tempo_analiza)
#print('converter demora ', tempo_converte)
#print('o len de freqs é: ', len(banana))

grava_som ('feroz', 1)

banana =  analiza_som('feroz', notas_freq)

print(banana)





