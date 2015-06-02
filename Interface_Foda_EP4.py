
from tkinter import *

x = 'red'

#Estado = 0



class SPFC:
    def __init__(self,raiz):
        self.canvas = Canvas(raiz, width=700, height=700, bg="blue") 
        self.canvas.pack()
        self.canvas.create_text(350, 350, text='G',font=('Arial','100','bold'), anchor=CENTER, fill= x)
        

class Janela:
    def __init__(self,toplevel):
        self.fr1 = Frame(toplevel)
        self.fr1.place(x=400, y=250)
        
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
        
        self.botao1.bind("<Motion>", self.muda_de_cor)                 #Quando o mause está em cima do botão1
        self.botao1.bind("<Leave>", self.muda_de_cor)                  #Quando o mouse sai de cima do botão1
        self.botao1.bind("<Button-1>", self.apagar_criar_novo_frame)          #Quando o botão1 é clicado

        self.botao2.bind("<Motion>",self.muda_de_cor1)                 #Quando o mause está em cima do botão2
        self.botao2.bind("<Leave>",self.muda_de_cor1)                  #Quando o mouse sai de cima do botão2
        self.botao2.bind("<Button-1>", self.apagar_criar_novo_frame)          #Quando o botão2 é clicado
        
    def apagar_criar_novo_frame(self,event):
        self.fr1.pack_forget()
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
instancia.geometry('1080x720')
instancia.title ('Guitar Teacher')
Janela(instancia)
instancia.mainloop()
