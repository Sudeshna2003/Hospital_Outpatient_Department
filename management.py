# -*- coding: utf-8 -*-
"""
Created on Tue Jun 20 09:26:34 2023

@author: Sudeshna Dutta
"""

from tkinter import *
from tkinter import messagebox
from PIL import ImageTk

def login():
    if usernameEntry.get()=='' or passwordEntry.get()=='':
        messagebox.showerror('Error','Username and Password can not be empty')
    elif usernameEntry.get()=='Sudeshna Dutta' and passwordEntry.get()=='08022003':
        messagebox.showinfo('Success','Welcome to XYZ Hospital OutPatient Database')
        window.destroy()
        import management0
    else:
        messagebox.showerror('Error','Wrong credentials entered')

window=Tk()

window.geometry('1400x800+0+0')
window.title("XYZ Hospital")

background=ImageTk.PhotoImage(file='C:\\Users\\Sudeshna Dutta\\Downloads\\pexels-artem-podrez-4492065.jpg')
bglabel=Label(window, image=background)
bglabel.place(x=0,y=0)
label=Label(window,text="Welcome to the Outpatient Department of XYZ Hospital!",
            font=('times new roman',32,'bold'),fg='dark blue')
label.pack(padx=30,pady=130)

loginFrame=Frame(window,bg='white')
loginFrame.place(x=450,y=250)
logoimg=ImageTk.PhotoImage(file='C:\\Users\\Sudeshna Dutta\\Downloads\\medical.png')
logoLabel=Label(loginFrame,image=logoimg)
logoLabel.grid(row=0,column=0,columnspan=2,pady=10)
usernameLabel=Label(loginFrame,text='Username',compound=LEFT,
                    font=('times new roman',20,'bold'),bg='white')
usernameLabel.grid(row=1,column=0,pady=10,padx=20)
usernameEntry=Entry(loginFrame,font=('times new roman',20,'bold'),
                    bd=5,fg='dark blue')
usernameEntry.grid(row=1,column=1,pady=10,padx=20)

passwordLabel=Label(loginFrame,text='Password',compound=LEFT,
                    font=('times new roman',20,'bold'),bg='white')
passwordLabel.grid(row=2,column=0,pady=10,padx=20)
passwordEntry=Entry(loginFrame,font=('times new roman',20,'bold'),
                    bd=5,fg='dark blue')
passwordEntry.grid(row=2,column=1,pady=10,padx=20)

loginbtn=Button(loginFrame,text='Login',font=('times new roman',14,'bold'),
                width=15,fg='white',bg='royal blue',activebackground='royal blue'
                ,cursor='hand2',command=login)
loginbtn.grid(row=3,column=1,pady=10)

window.mainloop()