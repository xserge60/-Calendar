#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
from tkinter import *

# Создание главного окна
root = Tk()

# создание виджета (кнопки)
but = Button(root, text = "Печать", width=30,height=5, bg="white",fg="blue")

# Установка свойств виджет
#but["text"] = "Печать"

# Определение событий и их обработчиков
def printer(event):
     print ("Как всегда очередной 'Hello World!'")
     
but.bind("<Button-1>",printer)

# Размещение виджет
but.pack()

# Отображение главного окна (Данная строчка кода должна быть всегда в конце скрипта!)
root.mainloop()


"""
"""
# то же самое с использованием класса
from tkinter import *

class But_print:
     def __init__(self):
          self.but = Button(root, text='Это кнопка')
          self.but.bind("<Button-1>",self.printer)
          self.but.pack()
     def printer(self,event):
          print ("Как всегда очередной 'Hello World!'")
 
root = Tk()
#but = Button(root, text="Это кнопка!", width=30,height=5, bg="white",fg="blue")
obj = But_print()
root.mainloop()
#"""

def kol_br(txt):
    v = 0
    for c in txt.split('<br>'):
        v += 1 + len(c) // 40
    return v
import datetime
d = datetime.date(2017, 11, 5)
n1='1'
n2='-1'
print(str(d), str(d+datetime.timedelta(days=int(n1))), str(d+datetime.timedelta(days=int(n2))))
txt="<br>— Друзья-американцы, подскажите, чем нам, русским, победить неблагоприятно складывающиеся обстоятельства?<br>— Economy. Just economy.<br>— Спасибо. Иконами так иконами.<br>"
print(kol_br(txt),len(txt.split('<br>')))
