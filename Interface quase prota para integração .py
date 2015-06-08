# -*- coding: utf-8 -*-
"""
Created on Sat May 30 19:42:49 2015

@author: Rodrigo & Matheus
"""

__author__ = 'Rodrigo'

from tkinter import *
#import partedosom



x = 'red'
nota = ''

#Criar um def para parte do som, cujo um dos inputs será o tempo de ele ficará gravando.

class SPFC:
    def __init__(self,instancia):
        self.canvas = Canvas(instancia, width=720, height=480, bg='dodgerblue')
        self.canvas.pack()
        self.canvas.create_text(360, 240, text='G',font=('Arial','100','bold'), anchor=CENTER, fill= x)

        self.back = Button(self.canvas, text = 'Voltar')
        self.back['fg']='dodgerblue'
        self.back['font']=('Verdana','12','italic','bold')
        self.back['height']=7
        self.back['width']=10
        self.back['bg']= 'dodgerblue'
        self.back.place(x = 590, y = 350)

        self.back.bind("<Button-1>", self.voltar)

    def voltar(self, event):

        self.canvas.pack_forget()
        Janela(instancia)

class Janela:


    def __init__(self,toplevel):


        self.fr1 = Frame(toplevel)
        self.fr1.place(x=210, y=125)

        #self.canvas_inicial = Canvas(toplevel,width = 720, height = 480, bg = 'white')
        #self.canvas_inicial.pack(expand = YES, fill = BOTH)
        #self.gif1 = PhotoImage(file = 'Pg #1 1080.gif')
        #self.canvas_inicial.create_image(360,240,image = self.gif1)

        # Configurações estéticas dos botões:
        self.botao1 = Button(self.fr1,text='Calibrar')
        self.botao1['fg']='black'
        self.botao1['font']=('Verdana','12','italic','bold')
        self.botao1['height']=7
        self.botao1['width']=30
        self.botao1.pack()

        self.botao2 = Button(self.fr1,text='Play')
        self.botao2['fg']='black'
        self.botao2['font']=('Verdana','12','italic','bold')
        self.botao2['height']=7
        self.botao2['width']=30
        self.botao2.pack()


        # Configurações funcionais dos botões:
        self.botao1.bind("<Motion>", self.muda_de_cor)                 #Quando o mause está em cima do botão1
        self.botao1.bind("<Leave>", self.muda_de_cor)                  #Quando o mouse sai de cima do botão1
        self.botao1.bind("<Button-1>", self.apagar_criar_novo_frame)          #Quando o botão1 é clicado

        self.botao2.bind("<Motion>",self.muda_de_cor1)                 #Quando o mouse está em cima do botão2
        self.botao2.bind("<Leave>",self.muda_de_cor1)                  #Quando o mouse sai de cima do botão2
        self.botao2.bind("<Button-1>", self.apagar_criar_novo_frame)          #Quando o botão2 é clicado

    def apagar_criar_novo_frame(self,event):
        #self.canvas_inicial.delete()
        self.fr1.place_forget()
        SPFC(instancia)



    def muda_de_cor (self,event1):
        if self.botao1['fg']=='black':
            self.botao1['fg']='yellow'
        else:
            self.botao1['fg']='black'


    def muda_de_cor1 (self,event12):
        if self.botao2['fg']=='black':
            self.botao2['fg']='yellow'
        else:
            self.botao2['fg']='black'



instancia=Tk()
instancia.geometry('720x480')
instancia.title ('Guitar Teacher')

# canvas = Canvas(width = 720, height = 480, bg = 'white')
# canvas.pack(expand = YES, fill = BOTH)
# gif1 = PhotoImage(file = 'Pg #1 1080.gif')
# canvas.create_image(0, 0, image = gif1, anchor = NW)

Janela(instancia)

instancia.mainloop()


while True:
    '''
    if 'A' in freq:
        x = 'green'

    '''
    Janela(instancia)
    instancia.mainloop()


