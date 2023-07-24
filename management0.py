# -*- coding: utf-8 -*-
"""
Created on Wed Jun 21 09:55:00 2023

@author: Sudeshna Dutta
"""

from tkinter import *
import time
from PIL import ImageTk
from tkinter import ttk,messagebox,filedialog
import pymysql
import pandas

#Functionality


def toplevel_field():
    global fieldWindow,serialEntry,nameEntry,contactEntry,genderEntry,ageEntry,consultEntry
    fieldWindow=Toplevel()
    fieldWindow.resizable(0,0)
    fieldWindow.grab_set()
    fieldWindow.title('Patient Details')
    serialLabel=Label(fieldWindow,text='Token No',font=('times new roman',20,'bold'))
    serialLabel.grid(row=0,column=0,padx=30,pady=15,sticky=W)
    serialEntry=Entry(fieldWindow,font=('roman',15,'bold'),width=24)
    serialEntry.grid(row=0,column=1,padx=10,pady=15)
    
    nameLabel=Label(fieldWindow,text='Name',font=('times new roman',20,'bold'))
    nameLabel.grid(row=1,column=0,padx=30,pady=15,sticky=W)
    nameEntry=Entry(fieldWindow,font=('roman',15,'bold'),width=24)
    nameEntry.grid(row=1,column=1,padx=10,pady=15)
    
    contactLabel=Label(fieldWindow,text='Contact No',font=('times new roman',20,'bold'))
    contactLabel.grid(row=2,column=0,padx=30,pady=15,sticky=W)
    contactEntry=Entry(fieldWindow,font=('roman',15,'bold'),width=24)
    contactEntry.grid(row=2,column=1,padx=10,pady=15)
    
    genderLabel=Label(fieldWindow,text='Gender',font=('times new roman',20,'bold'))
    genderLabel.grid(row=3,column=0,padx=30,pady=15,sticky=W)
    genderEntry=Entry(fieldWindow,font=('roman',15,'bold'),width=24)
    genderEntry.grid(row=3,column=1,padx=10,pady=15)
    
    ageLabel=Label(fieldWindow,text='Age',font=('times new roman',20,'bold'))
    ageLabel.grid(row=4,column=0,padx=30,pady=15,sticky=W)
    ageEntry=Entry(fieldWindow,font=('roman',15,'bold'),width=24)
    ageEntry.grid(row=4,column=1,padx=10,pady=15)
    
    consultLabel=Label(fieldWindow,text='Consultation',font=('times new roman',20,'bold'))
    consultLabel.grid(row=5,column=0,padx=30,pady=15,sticky=W)
    consultEntry=Entry(fieldWindow,font=('roman',15,'bold'),width=24)
    consultEntry.grid(row=5,column=1,padx=10,pady=15)
    

def add_patient():
    def add_data():
        if serialEntry.get()=='' or nameEntry.get()=='' or contactEntry.get()=='' or genderEntry.get()=='' or ageEntry.get()=='' :
            messagebox.showerror('Error','Enter all mandatory fields',parent=fieldWindow)
        else:
            date=time.strftime('%d/%m/%Y')
            try:
                query ='insert into outpatient values(%s,%s,%s,%s,%s,%s,%s)'
                mycursor.execute(query,(serialEntry.get(),nameEntry.get(),contactEntry.get(),genderEntry.get(),ageEntry.get(),consultEntry.get(),date))
                con.commit()
                result=messagebox.askyesno('Success & Confirm','Data added successfully. Do you want to clean the form?',parent=fieldWindow)
                if result:
                    serialEntry.delete(0,END)
                    nameEntry.delete(0,END)
                    contactEntry.delete(0,END)
                    genderEntry.delete(0,END)
                    ageEntry.delete(0,END)
                    consultEntry.delete(0,END)
                else:
                    pass
            except:
                messagebox.showerror('Error','Entered Token No. Already Exists',parent=fieldWindow)
                return
            
            query ='select * from outpatient'
            mycursor.execute(query)
            fetched_data=mycursor.fetchall()
            patbox.delete(*patbox.get_children())
            for data in fetched_data:
                datalist=list(data)
                patbox.insert('',END,values=datalist)
    
    toplevel_field()
    add_patient_btn=Button(fieldWindow,text='ADD PATIENT',fg='white',bg='black',command=add_data)
    add_patient_btn.grid(row=6,columns=2,pady=15)
    
def search_patient():
    def search_data():
        query ='select * from outpatient where token=%s or name=%s or contact=%s or gender=%s or age=%s or consultation=%s or date=%s'
        mycursor.execute(query ,(serialEntry.get(),nameEntry.get(),contactEntry.get(),genderEntry.get(),ageEntry.get(),consultEntry.get(),dateEntry.get()))
        patbox.delete(*patbox.get_children())
        fetched_data=mycursor.fetchall()
        for data in fetched_data:
            datalist=list(data)
            patbox.insert('',END,values=datalist)
        
    toplevel_field()
    dateLabel=Label(fieldWindow,text='Date',font=('times new roman',20,'bold'))
    dateLabel.grid(row=6,column=0,padx=30,pady=15,sticky=W)
    dateEntry=Entry(fieldWindow,font=('roman',15,'bold'),width=24)
    dateEntry.grid(row=6,column=1,padx=10,pady=15)
    
    search_patient_btn=Button(fieldWindow,text='SEARCH PATIENT',fg='white',bg='black',command=search_data)
    search_patient_btn.grid(row=7,columns=2,pady=15)
    
def update_patient():
    def update_data():
        date=time.strftime('%d/%m/%Y')
        query='update outpatient set name=%s, contact=%s, gender=%s, age=%s, consultation=%s, date=%s where token=%s'
        mycursor.execute(query,(nameEntry.get(),contactEntry.get(),genderEntry.get(),ageEntry.get(),consultEntry.get(),date,serialEntry.get()))
        con.commit()
        messagebox.showinfo('Success','Data Updated Successfully',parent=fieldWindow)
        fieldWindow.destroy()
        show_patient()
    
    toplevel_field()
    update_patient_btn=Button(fieldWindow,text='UPDATE PATIENT',fg='white',bg='black',command=update_data)
    update_patient_btn.grid(row=6,columns=2,pady=15)
    
    index=patbox.focus()
    info=patbox.item(index)
    listinfo=info['values']
    serialEntry.insert(0,listinfo[0])
    nameEntry.insert(0,listinfo[1])
    contactEntry.insert(0,listinfo[2])
    genderEntry.insert(0,listinfo[3])
    ageEntry.insert(0,listinfo[4])
    consultEntry.insert(0,listinfo[5])

def show_patient():
    query='select * from outpatient'
    mycursor.execute(query)
    fetched_data=mycursor.fetchall()
    patbox.delete(*patbox.get_children())
    for data in fetched_data:
        patbox.insert('',END,values=data)

def delete_patient():
    index=patbox.focus()
    info=patbox.item(index)
    serialinfo=info['values'][0]
    query ='delete from outpatient where token=%s'
    mycursor.execute(query,serialinfo)
    con.commit()
    messagebox.showinfo('Deleted','Selected Data has been Deleted Successfully')
    query='select * from outpatient'
    mycursor.execute(query)
    fetched_data=mycursor.fetchall()
    patbox.delete(*patbox.get_children())
    for data in fetched_data:
        patbox.insert('',END,values=data)
        
def export_data():
    url=filedialog.asksaveasfilename(defaultextension='.csv')
    index=patbox.get_children()
    l=[]
    for it in index:
        info=patbox.item(it)
        datalist=info['values']
        l.append(datalist)
    table=pandas.DataFrame(l,columns=['Token No.','Name','Contact No.','Gender','Age','Consultation','Date'])
    table.to_csv(url,index=False)
    messagebox.showinfo('Success','Data Saved Successfully')
    
def exit_window():
    result=messagebox.askyesno('Confirm','Do you want to exit?')
    if result:
        root.destroy()
    else:
        pass

def calender():
    date=time.strftime('%d/%m/%Y')
    dateLabel.config(text=f'Date: {date}')

def connect_database():
    def connect():
        global mycursor,con
        try:
            #con=pymysql.connect(host=hostentry.get(),user=userentry.get(),password=passentry.get())
            con=pymysql.connect(host='localhost',user='root',password='Doyel2003')
            mycursor=con.cursor()
            messagebox.showinfo('Success','Database Connection Established!',
                                parent=connectWindow)
            connectWindow.destroy()
        except:
            messagebox.showerror('Error','Invalid Details',parent=connectWindow)
            return
        try:
            query ='create database outpatientdatabase'
            mycursor.execute(query)
            query ='use outpatientdatabase'
            mycursor.execute(query)
            query ='create table outpatient(token int not null primary key,name varchar(30),contact varchar(10),gender varchar(20),age int,consultation varchar(30),date varchar(20))'
            mycursor.execute(query)
        except:
            query ='use outpatientdatabase'
            mycursor.execute(query)
        addbtn.config(state=NORMAL)
        searchbtn.config(state=NORMAL)
        updatebtn.config(state=NORMAL)
        showbtn.config(state=NORMAL)
        exportbtn.config(state=NORMAL)
        deletebtn.config(state=NORMAL)
    
    connectWindow=Toplevel()
    connectWindow.grab_set()
    connectWindow.geometry('470x250+730+230')
    connectWindow.title('Database Connection')
    connectWindow.resizable(0,0)
    
    hostnameLabel=Label(connectWindow,text='Host Name',font=('arial',18,'bold'),fg='firebrick3')
    hostnameLabel.grid(row=0,column=0,padx=20)
    
    hostentry=Entry(connectWindow,font=('roman',15,'bold'),bd=3)
    hostentry.grid(row=0,column=1,padx=30,pady=20)
    
    usernameLabel=Label(connectWindow,text='User Name',font=('arial',18,'bold'),fg='firebrick3')
    usernameLabel.grid(row=1,column=0,padx=20)
    
    userentry=Entry(connectWindow,font=('roman',15,'bold'),bd=3)
    userentry.grid(row=1,column=1,padx=30,pady=20)
    
    passLabel=Label(connectWindow,text='Password',font=('arial',18,'bold'),fg='firebrick3')
    passLabel.grid(row=2,column=0,padx=20)
    
    passentry=Entry(connectWindow,font=('roman',15,'bold'),bd=3)
    passentry.grid(row=2,column=1,padx=30,pady=20)
    
    connectbttn=Button(connectWindow,text='CONNECT',bg='dodgerblue4',fg='white',cursor='hand2',width=20,command=connect)
    connectbttn.grid(row=3,column=1)

#GUI

root=Tk()

root.geometry('1400x800+0+0')
root.title("Database of XYZ Hospital")

dateLabel=Label(root,font=('times new roman',24,'bold'))
dateLabel.place(x=30,y=25)
calender()

st='XYZ Hospital - Outpatient Database'
headlineLabel=Label(root,text=st,font=('Times new roman',32,'italic bold'),fg='navy blue')
headlineLabel.place(x=400,y=20)

connectbtn=Button(root,text="Connect database",font=('times new roman',16,'bold'),
                  fg='white',bg='black',activebackground='grey',
                  activeforeground='green2',cursor='hand2',command=connect_database)
connectbtn.place(x=1150,y=25)

leftFrame=Frame(root,bg='midnight blue',bd=5)
leftFrame.place(x=20,y=100,width=300,height=580)
addbtn=Button(leftFrame,text="Add Patient Details",font=(18),width=20,
              state=DISABLED,fg='navy blue',bg='mistyrose',
                             activebackground='teal',activeforeground='white',cursor='hand2',command=add_patient)
addbtn.grid(row=1,column=1,padx=50,pady=25)
searchbtn=Button(leftFrame,text="Search Patient Details",font=(18),width=20,
                 state=DISABLED,fg='navy blue',bg='mistyrose',
                                activebackground='teal',activeforeground='white',cursor='hand2',command=search_patient)
searchbtn.grid(row=2,column=1,padx=50,pady=25)
updatebtn=Button(leftFrame,text="Update Patient Details",font=(18),width=20,
                 state=DISABLED,fg='navy blue',bg='mistyrose',
                                activebackground='teal',activeforeground='white',cursor='hand2',command=update_patient)
updatebtn.grid(row=3,column=1,padx=50,pady=25)
showbtn=Button(leftFrame,text="Show Patient Details",font=(18),width=20,
               state=DISABLED,fg='navy blue',bg='mistyrose',
                              activebackground='teal',activeforeground='white',cursor='hand2',command=show_patient)
showbtn.grid(row=4,column=1,padx=50,pady=25)
deletebtn=Button(leftFrame,text="Delete Patient Details",font=(18),width=20,
                 state=DISABLED,fg='navy blue',bg='mistyrose',
                                activebackground='teal',activeforeground='white',cursor='hand2',command=delete_patient)
deletebtn.grid(row=5,column=1,padx=50,pady=25)
exportbtn=Button(leftFrame,text="Export Patient Details",font=(18),width=20,
                 state=DISABLED,fg='navy blue',bg='mistyrose',
                                activebackground='teal',activeforeground='white',cursor='hand2',command=export_data)
exportbtn.grid(row=6,column=1,padx=50,pady=25)
exitbtn=Button(leftFrame,text="Exit",font=(18),width=20,fg='navy blue',bg='mistyrose',
               activebackground='teal',activeforeground='white',cursor='hand2',command=exit_window)
exitbtn.grid(row=7,column=1,padx=50,pady=25)

rightFrame=Frame(root)
rightFrame.place(x=350,y=100,width=985,height=600)
scrollx=Scrollbar(rightFrame,orient=HORIZONTAL)
scrolly=Scrollbar(rightFrame,orient=VERTICAL)
patbox=ttk.Treeview(rightFrame,columns=('Token No','Name','Contact No.',
                                        'Gender','Age','Consultation','Date'),xscrollcommand=scrollx.set,yscrollcommand=scrolly.set)
scrollx.config(command=patbox.xview)
scrolly.config(command=patbox.yview)
scrollx.pack(side=BOTTOM,fill=X)
scrolly.pack(side=RIGHT,fill=Y)
patbox.pack(fill=BOTH,expand=1)
patbox.heading('Token No',text='Token No.')
patbox.heading('Name',text='Patient Name')
patbox.heading('Contact No.',text='Contact No.')
patbox.heading('Gender',text='Gender')
patbox.heading('Age',text='Age')
patbox.heading('Consultation',text='Consultation')
patbox.heading('Date',text='Date')

patbox.column('Token No',width=150,anchor=CENTER)
patbox.column('Name',width=300,anchor=CENTER)
patbox.column('Contact No.',width=300,anchor=CENTER)
patbox.column('Gender',width=200,anchor=CENTER)
patbox.column('Age',width=100,anchor=CENTER)
patbox.column('Consultation',width=300,anchor=CENTER)
patbox.column('Date',width=200,anchor=CENTER)

style=ttk.Style()
style.configure('Treeview',rowheight=40,font=('arial',12))
style.configure('Treeview.Heading',font=('times new roman',20,'bold'))

patbox.config(show='headings')

root.mainloop()