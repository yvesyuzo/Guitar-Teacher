# -*- coding: utf-8 -*-
"""
Created on Sun May 24 16:18:45 2015

@author: Yves Yuzo
"""

from pylab import plot, show, title, xlabel, ylabel, subplot, savefig
from scipy import fft, arange, ifft
from numpy import sin, linspace, pi
from scipy.io.wavfile import read,write

def plotSpectru(y,Fs):
 n = len(y) # lungime semnal
 k = arange(n)
 T = n/Fs
 frq = k/T # two sides frequency range
 frq = int(frq[range(n/2)]) # one side frequency range

 Y = fft(y)/n # fft computing and normalization
 Y = Y[range(n/2)]
 
 plot(frq,abs(Y),'r') # plotting the spectrum
 xlabel('Freq (Hz)')
 ylabel('|Y(freq)|')

Fs = 44100;  # sampling rate

rate,data=read('Riff2.wav')
y=data[::1]
lungime=len(y)
timp=len(y)/44100.
t=linspace(0,timp,len(y))

subplot(2,1,1)
plot(t,y)
xlabel('Time')
ylabel('Amplitude')
subplot(2,1,2)
plotSpectru(y,Fs)
show()