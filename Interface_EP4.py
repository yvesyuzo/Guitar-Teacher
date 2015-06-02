
from tkinter import *

x = 'purple'

class SPFC:
    
    def __init__(self,raiz):
        self.canvas = Canvas(raiz, width=500, height=500, bg='dodgerblue') 
        self.canvas.pack()


        self.canvas.create_text(250, 250, text='S P F C',
                                font=('Arial','100','bold'), 
                                anchor=CENTER, fill= x)
    
        

class Janela:
    def __init__(self,toplevel):
        self.fr1 = Frame(toplevel)
        self.fr1.pack()
        
        self.botao1 = Button(self.fr1,text='Notas')
        self.botao1['fg']='black'
        self.botao1['font']=('Verdana','12','italic','bold') 
        self.botao1['height']=7
        self.botao1['width']=30
        self.botao1.pack()
        
        self.botao2 = Button(self.fr1,text='Música') 
        self.botao2['fg']='black'
        self.botao2['font']=('Verdana','12','italic','bold')
        self.botao2['height']=7
        self.botao2['width']=30
        self.botao2.pack()
        
        self.botao1.bind("<Motion>", self.muda_de_cor)
        self.botao1.bind("<Leave>", self.muda_de_cor)
        self.botao1.bind("<Button-1>", self.abre_nova_janela)

        self.botao2.bind("<Motion>",self.muda_de_cor1)
        self.botao2.bind("<Leave>",self.muda_de_cor1)
        self.botao2.bind("<Button-1>", self.abre_nova_janela)
        
    def abre_nova_janela(self,event):
        instancia = Tk()
        
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
Janela(instancia)
instancia.mainloop()
