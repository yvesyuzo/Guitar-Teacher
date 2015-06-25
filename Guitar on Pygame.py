# -*- coding: utf-8 -*-

"""
Created on Tue Jun 16 07:08:30 2015

@author: rodrigo
"""
import pyaudio
import wave
import numpy as np
import time
import pygame
from funcs import*
#-----------------------------------------------------------------------------------------------------------------------------

pygame.init()

# -------- Programa rodando: -----------
while not finish:    

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            finish = True

    tela_inicial()
    
pygame.quit()



