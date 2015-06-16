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
import time
import pyaudio
import wave
import numpy as np
import matplotlib.pyplot as plt

x = 10

def grava_som ():

    CHUNK = 2048
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100 # de acordo com Nyquist é possivel ler
    RECORD_SECONDS = 5
    WAVE_OUTPUT_FILENAME = "0.wav" #nome do arquivo de saida.
    
    p = pyaudio.PyAudio()
    
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    print('Prepara')
    print('3')
    time.sleep(1)
    print('2')
    time.sleep(1)
    print('1')
    time.sleep(1)                
    print("* recording")
    
    frames = []
    
    
    
    
    '''
    Grava
    '''
    
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
    
    return WAVE_OUTPUT_FILENAME, frames




testd = []

CHUNK = 2048
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

p = pyaudio.PyAudio()    

#LEITURA
tempo = time.time()
wf = wave.open('tuning', 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()

# open up a wave
wf = wave.open('tuning.wav', 'rb')
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



maior_data = 0

threshold = 36000000000

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
            print ("The freq is %f Hz." % (thefreq))
            freqs.append(thefreq)
        else:
            thefreq = which*RATE/CHUNK
            print ("The freq is %f Hz." % (thefreq))
            freqs.append(thefreq)
        # read some more data
        data = wf.readframes (int(CHUNK))
        print ("------chunk ok ------")
        
    data = wf.readframes (int(CHUNK))
        
    
    testd.append(fftData[1])    
#    except:
#        indata = None        
#        print ("Not enough data")
#    plt.plot((fftData))
#    plt.ylabel("dividido por 2")
#    plt.show()
#    plt.close()
print('done')

print('As freqs são:')
for i in freqs:
    print(i)

print("O len das freqs é: ", len(freqs))
print (type(freqs))
#print('O tipo de cada freq é: ', type(freqs[2]))

#plt.plot(freqs[int(len(freqs)*0.1):int(len(freqs)*0.9)])
plt.plot(freqs)
plt.grid()
plt.show()

#plt.plot(freqs)
#plt.grid()
#plt.show()

print('maior data', maior_data)

print(tempo)

if data:
    stream.write(data)
stream.close()
p.terminate()




'''
Dicionário com as 6 notas da afinação padrão de guitarra como keys e 3 numeros 
    como values onde o segundo valor é a frequencia exata e os outros dois são a 
    margem de erro de +-1 com relação a nota seguinte.
    
    exemplo: DS4 = 311, E4 = 329, F4 = 349| portanto {'E4':[(311+1), 329, (349-1)]} 

'''


notas_freq = {'E4': [312,329,348],'B3': [234,247,261],'G3': [185,196,208],
              'D3': [140,147,155],'A2': [105,110,116],'E2': [78,82,86], 'A4': [416, 440, 465]}

notas_SevenNationArmy = {'E3': [157,165,175],'G3': [186,196,207],'D3': [140,147,155],
                         'C3': [127,131,135],'B2': [120,123,126]}

'''
Função que recebe frequencias e retorna as notas equivalentes
ENTRADAS: 
            lista_de_freqs = lista com frequencias
            notas_freq     = dicionario com notas(keys)  e suas frequencias(values) com margem de erro

SAÍDAS:
            notas = lista com as notas na ordem de aparição

              'D3': [140,147,155],'A2': [105,110,116],'E2': [78,82,86], 'A4': [416, 440, 465]}            
'''


def conversor_freq_nota(lista_de_freqs, notas_freq):
    
    notas = []
    for x in lista_de_freqs:
        
        notas_temp = [i for i in notas_freq if int(x) in range(notas_freq[i][0],notas_freq[i][2])]
        if notas_temp != []:
            notas.append(notas_temp)
        
    return notas



#print(conversor_freq_nota(freqs, notas_freq))

