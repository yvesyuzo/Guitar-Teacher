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
#import funcs



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
    



def analisa_som (NOME, notas_freq, nota_desejada):
    
    cha = []
    nota_desejada

    CHUNK = 2048
    RATE = 44100 
    
    p = pyaudio.PyAudio()    
    
    threshold = 36000000000 # amplitude dos ruidos
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
        

        indata = np.array(wave.struct.unpack("%dh"%(len(data)/swidth),data))*window


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
            
        else:
            try:
                freqs.append(thefreq)
            
            except:
                pass
                
                               
        data = wf.readframes (int(CHUNK))
#            print ("------chunk ok ------")
            
    


    if data:
        stream.write(data)
    stream.close()
    p.terminate()
    
    notas = []
    
    for x in freqs:
        
        notas_temp = [i for i in notas_freq if int(x) in range(notas_freq[i][0],notas_freq[i][2])]
        
        if notas_temp != []:
            
            notas.append(notas_temp)
            
        else:
            notas.append('0')
            
            
    for n in range(1, (len(notas)-1)):
            
        if notas[n] == nota_desejada and notas[n] == notas[n+1] and notas[n] == notas[n-1]:
                
            cha.append('true')
        
    return [cha]
    
    
    
notas_freq = {'E4': [312,329,348],'B3': [234,247,261],'G3': [185,196,208],
              'D3': [140,147,155],'A2': [105,110,116],'E2': [78,82,86], 'A4': [416, 440, 465]}



#-----------------------------------------------------------------------------------------------------------------------------

pygame.init()
 
tamanho = (1080, 720)
display_width = 1080
display_height = 720
win = pygame.display.set_mode(tamanho)
#porra = pygame.display.set_mode(tamanho)
 
pygame.display.set_caption("Guitat Teacher")
 
# Loop until the user clicks the close button.
finish = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()

#----------------------------------------------------------------------------------------------------------------
# Define some colors
black = (0, 0, 0)
white = (255, 255, 255)

red = (200,0,0)
green = (0,200,0)
bright_red = (255,0,0)
bright_green = (0,255,0)
cor_certa = (117,193,189)
cor_escura = (117,189,230)

bg = pygame.image.load('tela inicial.png')
bg_play = pygame.image.load('tela play.png')

a2 =  pygame.image.load('A2.png')
e2 =  pygame.image.load('E2.png')
e4 =  pygame.image.load('E4.png')
g3 =  pygame.image.load('G3.png')
d3 =  pygame.image.load('D3.png')
b3 =  pygame.image.load('B3.png')

bg_notas = pygame.image.load('play _notas.png')

bg_notas = pygame.transform.scale(bg_notas, (420, 10000))
tela1 = True
intro = True

#------------------------------------------
# Criacao das funcoes:
def tela_inicial():
    win.blit(bg, [0,0])   
    
    botao_play(" ",660,490,360,180,"musica")
    botao_calibrar_ou_voltar("Calibrar",140,195,230,45,red,white,"calibrar")
    
    play_metal(" ",350,330,100,45)
    pygame.display.update()
    
    clock.tick(60)
    
def tela_calibrar():
    global intro
    intro = True   
    notas_freq = {'E4': [312,329,348],'B3': [234,247,261],'G3': [185,196,208],
              'D3': [140,147,155],'A2': [105,110,116],'E2': [78,82,86]}
    correto0 = True
    correto1 = True
    correto2 = True
    correto4 = True
    correto5 = True
    correto6 = True
        
   # Contragem regressiva
    while intro:
        win.fill(black)
        
        myfont=pygame.font.SysFont("monospace",30)
        label=myfont.render('Após a contagem toque a tecla da tela!!!',1,white)
        win.blit(label,(100,30))
        
        pygame.display.update()
        myfont=pygame.font.SysFont("monospace",100)
        label=myfont.render('3',1,white)
        win.blit(label,((1080/4), ((720/2)-30) ))
        pygame.display.update()
        time.sleep(1)
        
        pygame.display.update()
        myfont=pygame.font.SysFont("monospace",100)
        label=myfont.render('2',1,white)
        win.blit(label,((1080/2), ((720/2)-30) ))
        pygame.display.update()
        time.sleep(1)
        
        
        pygame.display.update()
        myfont=pygame.font.SysFont("monospace",100)
        label=myfont.render('1',1,white)
        win.blit(label,((1080-(1080/4)), ((720/2)-30) ))
        pygame.display.update()
        time.sleep(1)

        
# E4 ------------------------------------------------------------------------------------        
        while correto0 == True:
            win.blit(e4, [0,0])
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    finish = True
          
            texto (" " ,"E4",white)
        #botao_voltar("Voltar",740,595,230,45,red,bright_green,"voltar")
       
            grava_som("nao_apagar", 1)
    
            notas = analisa_som ("nao_apagar", notas_freq, ['E4'])
            
            print(notas)
        
            if 'true' in notas[0]: 
                win.blit(e4, [0,0])
                texto (" " ,"E4",green)
                pygame.display.update()
                time.sleep(3)
                correto0 = False
                
            pygame.display.update()   
#A2 ---------------------------------------------------------------------------------------            
#        while correto1 == True:
#            win.blit(a2, [0,0])
#            for event in pygame.event.get():
#                if event.type == pygame.QUIT:
#                    finish = True
#          
#            texto (" " ,"A2",white)
#
#            
#            grava_som("nao_apagar2", 1)
#    
#            notas1 = analisa_som ("nao_apagar2", notas_freq, ['A2'])
#            
#            print(notas1)  
#        
#            if 'true' in notas1[0]:
#                win.blit(a2, [0,0])                      
#                texto (" " ,"A2",green)
#                pygame.display.update()
#                time.sleep(3)
#                correto1 = False
#                
#            pygame.display.update()           
#B3 ----------------------------------------------------------------------------------            
#        while correto2 == True:
#            win.blit(b3, [0,0])
#            for event in pygame.event.get():
#                if event.type == pygame.QUIT:
#                    finish = True
#          
#            texto (" " ,"B3",white)
#          
#        #botao_voltar("Voltar",740,595,230,45,red,bright_green,"voltar")
#       
#            grava_som("nao_apagar", 1)
#    
#            notas = analisa_som ("nao_apagar", notas_freq, ['B3'])
#        
#            if 'true' in notas[0]:
#                win.blit(b3, [0,0])
#                texto (" " ,"B3",green)
#                pygame.display.update()
#                time.sleep(3)
#                correto2 = False
#            pygame.display.update() 

#G3 -------------------------------------------------------------------------------
#        while correto4 == True:
#            win.blit(g3, [0,0])
#            for event in pygame.event.get():
#                if event.type == pygame.QUIT:
#                    finish = True
#          
#            texto (" " ,"G3",white)
#            
#        #botao_voltar("Voltar",740,595,230,45,red,bright_green,"voltar")
#       
#            grava_som("nao_apagar", 1)
#    
#            notas = analisa_som ("nao_apagar", notas_freq, ['G3'])
#        
#            if 'true' in notas[0]:
#                win.blit(g3, [0,0])
#                texto (" " ,"G3",green)
#                pygame.display.update()
#                time.sleep(3)             
#                correto4 = False
#            pygame.display.update() 
#D3 -------------------------------------------------------------------------------
#        while correto5 == True:
#            win.blit(d3, [0,0])
#            for event in pygame.event.get():
#                if event.type == pygame.QUIT:
#                    finish = True
#           
#            texto (" " ,"D3",white)
#
#          
#        #botao_voltar("Voltar",740,595,230,45,red,bright_green,"voltar")
#       
#            grava_som("nao_apagar", 1)
#    
#            notas = analisa_som ("nao_apagar", notas_freq, ['D3'])
#        
#            if 'true' in notas[0]:
#                win.blit(d3, [0,0])
#                texto (" " ,"D3",green)
#                pygame.display.update()
#                time.sleep(3)             
#                correto5 = False
#            pygame.display.update()         
            
#E2 -------------------------------------------------------------------------------
#        while correto6 == True:
#            win.blit(e2, [0,0])          
#            for event in pygame.event.get():
#                if event.type == pygame.QUIT:
#                    finish = True
#          
#            texto (" " ,"E2",white)
#          
#        #botao_voltar("Voltar",740,595,230,45,red,bright_green,"voltar")
#       
#            grava_som("nao_apagar", 1)
#    
#            notas = analisa_som ("nao_apagar", notas_freq, ["E2"])
#        
#            if 'true' in notas[0]:
#                win.blit(e2, [0,0])
#                texto (" " ,"E2",green)
#                pygame.display.update()
#                time.sleep(3)             
#                correto6 = False
#            pygame.display.update()
            
        win.fill(black)
        pygame.display.update()
        myfont=pygame.font.SysFont("monospace",50)
        label=myfont.render('Parabens!',1,white)
        win.blit(label,((150), ((720/2)-70) ))
        pygame.display.update()
        time.sleep(3)
        myfont=pygame.font.SysFont("monospace",50)
        label=myfont.render('Sua guitarra foi calibrada!',1,white)
        win.blit(label,((100), ((720/2)-10) ))
        pygame.display.update()
        time.sleep(3)
        
        clock.tick(60)
        
        break
    tela_inicial()

def texto (texto1,texto2,x):
    titulo_calibrar = pygame.font.SysFont("Arial",45)
    titulo_calibrar, TextRect = text_objects(texto1, titulo_calibrar)
    TextRect.center = ((300),(30))
    win.blit(titulo_calibrar, TextRect)
    
    myfont=pygame.font.SysFont("monospace",200)
    label=myfont.render(texto2,1,x)
    win.blit(label,(520,30))
    pygame.display.update()
    
def tela_play():
    global intro
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        win.blit(bg_play, [0,0])   
        #win.blit(bg_notas, [0,600])         
        #win.fill(white)
        #titulo_calibrar = pygame.font.SysFont("Arial",60)
        #titulo_calibrar, TextRect = text_objects("Let's do some rock!!!", titulo_calibrar)
        #TextRect.center = ((500),(30))
        #win.blit(titulo_calibrar, TextRect)
        
        botao_calibrar_ou_voltar("Voltar",40,595,230,45,red,white,"voltar")
       
        pygame.display.update()
        clock.tick(60)
        
    tela_inicial()
    
def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()
     
def botao_play(msg,x,y,w,h,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    
    if x+w > mouse[0] > x and y+h > mouse[1] > y:    
        if click[0]==1 and action=="musica":
            tela_play()
        
   
def botao_calibrar_ou_voltar(msg,x,y,w,h,cor1,cor2,action=None):   
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x+w > mouse[0] > x and y+h > mouse[1] > y:  
        pygame.draw.rect(win, cor1,(x,y,w,h))
        if click[0]==1 and action=="calibrar":
            tela_calibrar()
        if click[0]==1 and action=="voltar":
            global intro
            intro = False
            print('xuxu beleza')

    else: 
        pygame.draw.rect(win, cor2,(x,y,w,h))
        
    smallText = pygame.font.Font("freesansbold.ttf",20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    win.blit(textSurf, textRect)   
  

def play_metal(msg,x,y,w,h):
    mouse = pygame.mouse.get_pos()
    #click = pygame.mouse.get_pressed()

    if x+w > mouse[0] > x and y+h > mouse[1] > y:
#             pygame.draw.rect(win, red,(x,y,w,h))
#            pygame.init()
#            song = pygame.mixer.Sound('')
#            clock = pygame.time.Clock()
#            song.play()
             print('susu')

        




# -------- Programa rodando: -----------
while not finish:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finish = True


    tela_inicial()
 
        
        

pygame.quit()