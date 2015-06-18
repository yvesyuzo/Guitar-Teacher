# -*- coding: utf-8 -*-

"""
Created on Tue Jun 16 07:08:30 2015

@author: rodrigo
"""
import pyaudio
import wave
import numpy as np
import time
import matplotlib.pyplot as plt
import pygame
import Funções
import time

# Define some colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (200,0,0)
green = (0,200,0)
bright_red = (255,0,0)
bright_green = (0,255,0)
cor_certa = (117,193,189)
cor_escura = (117,189,230)

bg = pygame.image.load('guitar.jpg')
bg_play = pygame.image.load('play.png')
bg_notas = pygame.image.load('play _notas.png')
bg_notas = pygame.transform.scale(bg_notas, (420, 10000))
tela1 = True
intro = True
#------------------------------------------
# Criacao das funcoes:
def tela_inicial():
    win.blit(bg, [0,0])   

    
    botao_play("Play",740,235,325,140,white,bright_green,"musica")
    botao_calibrar("Calibrar",140,195,230,45,cor_certa,bright_green,"calibrar")
    
    play_metal(" ",400,195,230,45,red)
    pygame.display.update()
    
    clock.tick(60)
    
def tela_calibrar():
    global intro
    intro = True   
    notas_freq = {'E4': [312,329,348],'B3': [234,247,261],'G3': [185,196,208],
              'D3': [140,147,155],'A2': [105,110,116],'E2': [78,82,86], 'A4': [416, 440, 465]}        
    a = 0
    

    while intro:
        win.fill(white)
        if a == 0:
            pygame.display.update()
            smallText = pygame.font.Font("freesansbold.ttf",100)
            textSurf, textRect = text_objects("3", smallText)
            textRect.center = ( (1080/4), ((720/2)-30) )
            win.blit(textSurf, textRect)
            pygame.display.update()
            time.sleep(1)
            
            smallText = pygame.font.Font("freesansbold.ttf",100)
            textSurf, textRect = text_objects("2", smallText)
            textRect.center = ( (1080/2), ((720/2)-30)  )
            win.blit(textSurf, textRect)
            pygame.display.update()
            time.sleep(1)
            
            
            smallText = pygame.font.Font("freesansbold.ttf",100)
            textSurf, textRect = text_objects("1", smallText)
            textRect.center = ( (1080-(1080/4)), ((720/2)-30)  )
            win.blit(textSurf, textRect)
            pygame.display.update()
            time.sleep(1)
            a = 1
        
       # 'Notas a serem calibradas:'
       # ' E4    B3    G3   D3    A2     E2    A4'
        while intro:
            win.fill(white)
            
            for event in pygame.event.get():
                  if event.type == pygame.QUIT:
                      finish = True
            
           
            titulo_calibrar = pygame.font.SysFont("Arial",45)
            titulo_calibrar, TextRect = text_objects("Toque uma corda de cada vez para calibrar sua guitarra!", titulo_calibrar)
            TextRect.center = ((500),(30))
            win.blit(titulo_calibrar, TextRect)
            
            smallText = pygame.font.Font("freesansbold.ttf",160)
            textSurf, textRect = text_objects("E4", smallText)
            textRect.center = ( (1080/2), (720/2) )
            win.blit(textSurf, textRect)
              
            botao_voltar("Voltar",740,595,230,45,red,bright_green,"voltar")
           
            grava_som("nao_apagar", 5)
        
            notas = analiza_som ("nao_apagar", notas_freq)
            
            if 'E4' in notas:
                x = green
           
           
            pygame.display.update()
            clock.tick(60)
            
        
    tela_inicial()
    
def tela_play():
    global intro
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        win.blit(bg_play, [0,0])   
        win.blit(bg_notas, [0,600])         
        #win.fill(white)
        #titulo_calibrar = pygame.font.SysFont("Arial",60)
        #titulo_calibrar, TextRect = text_objects("Let's do some rock!!!", titulo_calibrar)
        #TextRect.center = ((500),(30))
        #win.blit(titulo_calibrar, TextRect)
        
        botao_voltar("Voltar",740,595,230,45,red,bright_green,"voltar")
       
        pygame.display.update()
        clock.tick(60)
        
    tela_inicial()
    
def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()
     
def botao_play(msg,x,y,w,h,ic,ac,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    
    if 740+325 > mouse[0] > 740 and 235+140 > mouse[1] > 235:
        pygame.draw.rect(win,cor_escura,(740,235,325,140))
        
        if click[0]==1 and action=="musica":
            tela_play()
        
    else:
        pygame.draw.rect(win, white,(740,235,325,140))
        
    smallText = pygame.font.Font("freesansbold.ttf",50)
    textSurf, textRect = text_objects("Play", smallText)
    textRect.center = ( (740+(325/2)), (235+(140/2)) )
    win.blit(textSurf, textRect)
 
   
def botao_calibrar(msg,x,y,w,h,ic,ac,action=None):   
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    ' A4'
    if 140+230 > mouse[0] > 140 and 195+45 > mouse[1] > 195:
        pygame.draw.rect(win, cor_escura,(140,195,230,45))
        
        if click[0]==1 and action=="calibrar":
            tela_calibrar()
            
    else:
        pygame.draw.rect(win, cor_certa,(140,195,230,45))
        
    smallText = pygame.font.Font("freesansbold.ttf",20)
    textSurf, textRect = text_objects("Calibrar", smallText)
    textRect.center = ( (140+(230/2)), (195+(45/2)) )
    win.blit(textSurf, textRect)
    
    
    
def botao_voltar(msg,x,y,w,h,ic,ac,action=None):   
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
        
    if 740+230 > mouse[0] > 740 and 595+45 > mouse[1] > 595:
        pygame.draw.rect(win, red,(740,595,230,45))
        
        if click[0]==1 and action=="voltar":
            global intro
            intro = False
            print('xuxu beleza')
            #tela_inicial()
            
    else:
        pygame.draw.rect(win, cor_certa,(740,595,230,45))
        
    smallText = pygame.font.Font("freesansbold.ttf",20)
    textSurf, textRect = text_objects("Voltar", smallText)
    textRect.center = ( (740+(230/2)), (595+(45/2)) )
    win.blit(textSurf, textRect)
    

def play_metal(msg,x,y,w,h,ic):
    mouse = pygame.mouse.get_pos()
    #click = pygame.mouse.get_pressed()

    if 280+130 > mouse[0] > 200 and 500+80 > mouse[1] > 500:
            pygame.init()
            song = pygame.mixer.Sound('')
            clock = pygame.time.Clock()
            song.play()

        
#---------------------------------------    
pygame.init()
 
tamanho = (1080, 720)
display_width = 1080
display_height = 720
win = pygame.display.set_mode(tamanho)
porra = pygame.display.set_mode(tamanho)
 
pygame.display.set_caption("Guitat Teacher")
 
# Loop until the user clicks the close button.
finish = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()



# -------- Programa rodando: -----------
while not finish:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finish = True


    tela_inicial()
 
        
        

pygame.quit()