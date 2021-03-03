from tkinter import *
import tkinter.ttk as tk
from pymysql import *
from admin import Admin
from registeredUser import User

db=connect(host="localhost",user='root',port=3306,password='incorrect@06',database='ticketbooking')
cur = db.cursor()
ad=Admin()
user=User()
def validate(t):
    cur.execute("select * from user_data where user_email='{}' and user_pass='{}'".format(
        username.get(), login_password.get()))
    res = cur.fetchone()
    if res[-1].lower() == 'admin':
        ad.admin_dashboard(res, t)
    elif res[-1].lower()=='user':
        user.user_dashboard(res,t)
    else:
        msg.set('Invalid Details')
        

def login(t):
    t.destroy()
    top = Toplevel()
    top.geometry('500x400')
    back = Button(top, text='Go Back', relief=GROOVE,
                  command=top.destroy).place(x=450, y=0)
    head = Label(top, text="MyMovie", font=("Arial", 25)).place(x=180, y=30)
    tag = Label(top, text="Movie Ticket Booking System").place(x=170, y=80)
    lab1 = Label(top, text='Login').place(x=20, y=140)
    e1 = Entry(top, textvariable=username).place(x=100, y=140)
    lab2 = Label(top, text='Password').place(x=20, y=170)
    e1 = Entry(top, textvariable=login_password).place(x=100, y=170)

    log = Button(top, text='Login', relief=GROOVE,
                 command=lambda: validate(top)).place(x=20, y=200)
    reg = Button(top, text='Register', relief=GROOVE,
                 command=lambda: register(top)).place(x=70, y=200)
    lab3=Label(top,textvariable=msg,text='').place(x=50,y=250)

def register(t):
    t.destroy()
    top=Toplevel()
    top.geometry('500x400')
    lab=Label(top,text='Already have an account?').place(x=300,y=0)
    back = Button(top, text='Login', relief=GROOVE,
                  command=lambda:login(top)).place(x=450, y=0)
    head = Label(top, text="MyMovie", font=("Arial", 25)).place(x=180, y=30)
    tag = Label(top, text="Movie Ticket Booking System").place(x=170, y=80)
    lab3=Label(top,text='Enter Your Name').place(x=20,y=140)
    e3=Entry(top,textvariable=userName).place(x=100,y=140)
    lab1 = Label(top, text='Enter Email').place(x=20, y=170)
    e1 = Entry(top, textvariable=email).place(x=100, y=170)
    lab2 = Label(top, text='Create Password').place(x=20, y=200)
    e2 = Entry(top, textvariable=newPassword).place(x=100, y=200)
    lab4=Label(top,text='Enter Mobile number').place(x=20,y=230)
    e4=Entry(top,textvariable=contact).place(x=100,y=230)

    reg = Button(top, text='Register', relief=GROOVE,
                 command=lambda: register(top)).place(x=20, y=270)
    errmsg=Label(top,textvariable=msg,text='').place(x=50,y=260)

def dash(c):

    top = Toplevel()
    top.geometry('500x400')
    back = Button(top, text='Go Back', relief=GROOVE,
                  command=top.destroy).place(x=450, y=0)
    Login = Button(top, text='Login', relief=GROOVE,
                   command=lambda: login(top)).place(x=400, y=0)
    head = Label(top, text="MyMovie", font=("Arial", 25)).place(x=180, y=30)
    tag = Label(top, text="Movie Ticket Booking System").place(x=170, y=80)
    lab = Label(top, text='Movies in '+c,
                font=('Arial', 15)).place(x=170, y=100)




def index():
    root.geometry("500x400")
    close = Button(root, text="Exit", command=root.destroy,
                   relief=GROOVE).place(x=450, y=0)
    head = Label(root, text="MyMovie", font=("Arial", 25)).place(x=180, y=30)
    tag = Label(root, text="Movie Ticket Booking System").place(x=170, y=80)
    city = tk.Combobox(root,textvariable=city_cb)
    city['values'] = ('Select Your City', 'Bhopal', 'Indore',
                      'Delhi', 'Mumbai', 'Heydrabad', 'Banglore')
    city.current(0)
    city.place(x=100, y=200)
    go = Button(root, text='Go', command=lambda: dash(
        city_cb.get()), relief=GROOVE).place(x=300, y=200)

root = Tk()

city_cb=StringVar()
username = StringVar()
login_password = StringVar()
msg=StringVar()
userName=StringVar()
contact=IntVar()
email=StringVar()
newPassword=StringVar()
index()
root.mainloop()