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
    correto0 = True
    correto1 = True
    correto2 = True
    correto3 = True
    correto4 = True
    correto5 = True
    correto6 = True
        
   # Contragem regressiva
    while intro:
        win.fill(white)
        
        titulo_calibrar = pygame.font.SysFont("Arial",45)
        titulo_calibrar, TextRect = text_objects("Após a contagem toque a corda da tela!", titulo_calibrar)
        TextRect.center = ((500),(30))
        win.blit(titulo_calibrar, TextRect)
        
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

        
# E4 ------------------------------------------------------------------------------------        
        while correto0 == True:
            win.fill(white)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    finish = True
          
            texto ("Começando com o E4" ,"E4",black)
        #botao_voltar("Voltar",740,595,230,45,red,bright_green,"voltar")
       
            grava_som("nao_apagar", 1)
    
            notas = analisa_som ("nao_apagar", notas_freq, ['E4'])
            
            print(notas)
        
            if 'true' in notas[0]: 
                win.fill(white)
                texto ("Começando com o E4" ,"E4",green)
                pygame.display.update()
                time.sleep(3)
                correto0 = False
                
            pygame.display.update()   
#A2 ---------------------------------------------------------------------------------------            
#        while correto1 == True:
#            win.fill(white)
#            for event in pygame.event.get():
#                if event.type == pygame.QUIT:
#                    finish = True
#          
#            texto ("Continuando com A2" ,"A2",black)
#        #botao_voltar("Voltar",740,595,230,45,red,bright_green,"voltar")
#            
#            
#            
#            grava_som("nao_apagar2", 1)
#    
#            notas1 = analisa_som ("nao_apagar2", notas_freq, ['A2'])
#            
#            print(notas1)  
#        
#            if 'true' in notas1[0]:
#                win.fill(white)                      
#                texto ("Começando com o A2" ,"A2",green)
#                pygame.display.update()
#                time.sleep(3)
#                correto1 = False
#                
#            pygame.display.update()           
#B3 ----------------------------------------------------------------------------------            
        while correto2 == True:
            win.fill(white)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    finish = True
          
            texto ("Continuando com B3" ,"B3",black)
          
        #botao_voltar("Voltar",740,595,230,45,red,bright_green,"voltar")
       
            grava_som("nao_apagar", 1)
    
            notas = analisa_som ("nao_apagar", notas_freq, ['B3'])
        
            if 'true' in notas[0]:
                win.fill(white)
                texto ("Começando com o B3" ,"B3",green)
                pygame.display.update()
                time.sleep(3)
                correto2 = False
            pygame.display.update() 
#A4 ------------------------------------------------------------------------------
        while correto3 == True:
            win.fill(white)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    finish = True
        
            texto ("Continuando com A4" ,"A4",black)
          
        #botao_voltar("Voltar",740,595,230,45,red,bright_green,"voltar")
       
            grava_som("nao_apagar", 1)
    
            notas = analisa_som ("nao_apagar", notas_freq, ['A4'])
        
            if 'true' in notas[0]:
                win.fill(white)
                texto ("Continuando com A4" ,"A4",green)
                pygame.display.update()
                time.sleep(3)             
                correto3 = False
            pygame.display.update()  
#G3 -------------------------------------------------------------------------------
        while correto4 == True:
            win.fill(white)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    finish = True
          
            texto ("Continuando com G3" ,"G3",black)
            
        #botao_voltar("Voltar",740,595,230,45,red,bright_green,"voltar")
       
            grava_som("nao_apagar", 1)
    
            notas = analisa_som ("nao_apagar", notas_freq, ['G3'])
        
            if 'true' in notas[0]:
                win.fill(white)
                texto ("Continuando com G3" ,"G3",green)
                pygame.display.update()
                time.sleep(3)             
                correto4 = False
            pygame.display.update() 
#D3 -------------------------------------------------------------------------------
        while correto5 == True:
            win.fill(white)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    finish = True
           
            texto ("Continuando com o D3" ,"D3",black)

          
        #botao_voltar("Voltar",740,595,230,45,red,bright_green,"voltar")
       
            grava_som("nao_apagar", 1)
    
            notas = analisa_som ("nao_apagar", notas_freq, ['D3'])
        
            if 'true' in notas[0]:
                win.fill(white)
                texto ("Continuando com D3" ,"D3",green)
                pygame.display.update()
                time.sleep(3)             
                correto5 = False
            pygame.display.update()         
            
#E2 -------------------------------------------------------------------------------
        while correto6 == True:
            win.fill(white)           
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    finish = True
          
            texto ("Continuando com E2" ,"E2",black)
          
        #botao_voltar("Voltar",740,595,230,45,red,bright_green,"voltar")
       
            grava_som("nao_apagar", 1)
    
            notas = analisa_som ("nao_apagar", notas_freq, ["E2"])
        
            if 'true' in notas[0]:
                win.fill(white)
                texto ("Continuando com E2" ,"E2",green)
                pygame.display.update()
                time.sleep(3)             
                correto6 = False
            pygame.display.update()
            
        clock.tick(60)
        
    
#tela_inicial()

def texto (texto1,texto2,x):
    titulo_calibrar = pygame.font.SysFont("Arial",45)
    titulo_calibrar, TextRect = text_objects(texto1, titulo_calibrar)
    TextRect.center = ((500),(30))
    win.blit(titulo_calibrar, TextRect)
    
    myfont=pygame.font.SysFont("monospace",150)
    label=myfont.render(texto2,1,x)
    win.blit(label,(520,360))
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
#            pygame.init()
#            song = pygame.mixer.Sound('')
#            clock = pygame.time.Clock()
#            song.play()
        print('susu')

        
#---------------------------------------    
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



# -------- Programa rodando: -----------
while not finish:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finish = True


    tela_inicial()
 
        
        

pygame.quit()