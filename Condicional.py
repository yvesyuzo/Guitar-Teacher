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


