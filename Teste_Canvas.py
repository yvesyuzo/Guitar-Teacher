# -*- coding: utf-8 -*-
"""
Created on Tue May 26 09:55:54 2015

@author: MatheusVentrilho
"""

from tkinter import *

#x = 'purple'

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
        self.botao1 = Button(self.fr1,text='Oi!')
        self.botao1['background']='green' 
        self.botao1['font']=('Verdana','12','italic','bold') 
        self.botao1['height']=3
        self.botao1.pack()
        
        self.botao2 = Button(self.fr1,bg='red', font=('Times','16')) 
        self.botao2['text']='Tchau!'
        self.botao2['fg']='yellow'
        self.botao2['width']=12
        self.botao2.pack()
                                
                              
                              
                              

        
        
#instancia=Tk()
#SPFC(instancia)
#instancia.mainloop()        
        
# -------------------------------------------------


i = 0

while i <=10:  
    m  = int(input("Escreva 0 ou 1:"))  
                              
    if m == 0:
        x = 'green'
        i += 1
    else:
        x = 'red'   
        i += 1      
        
    instancia=Tk()
    SPFC(instancia)
    instancia.mainloop()                      


# -------------------------------------------------
                              
"""         
m  = int(input("Escreva 0 ou 1:")) 
                     
if m == 0:
    x = 'green'
else:
    x = 'red'   
 """              

                


