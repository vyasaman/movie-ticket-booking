from tkinter import *
import tkinter.ttk as tk
from pymysql import *
db = connect(host='localhost', port=3306, user='root',
             password='Aman@123', database='ticketbooking')
cur = db.cursor()


class Adding:
    def addTheatre(self):
        pass

    def addMovie(self):
        pass

    def update(self):
        pass


class User:
    def showMovies(self):
        pass

    def showTheatre(self):
        pass

    def bookTicket(self):
        pass


class Admin(Adding):
    def showFunctions(self):
        pass


def validate(t):
    cur.execute("select * from user_data where user_email='{}' and user_pass='{}'".format(
        username.get(), login_password.get()))
    res = cur.fetchone()
    if res[-1].lower == 'admin':
        admin(res, t)


def admin(res, t):
    t.destroy()
    top = Toplevel()
    top.geometry('500x400')
    Logout = Button(top, text='Logout', relief=GROOVE,
                    command=top.destroy).place(x=450, y=0)
    head = Label(top, text="MyMovie", font=("Arial", 25)).place(x=180, y=30)
    tag = Label(top, text="Welcome "+res[3]).place(x=170, y=80)


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
    city = tk.Combobox(root, textvariable=city_cb)
    city['values'] = ('Select Your City', 'Bhopal', 'Indore',
                      'Delhi', 'Mumbai', 'Heydrabad', 'Banglore')
    city.current(0)
    city.place(x=100, y=200)
    go = Button(root, text='Go', command=lambda: dash(
        city_cb.get()), relief=GROOVE).place(x=300, y=200)


root = Tk()
city_cb = StringVar()
username = StringVar()
login_password = StringVar()
index()
root.mainloop()
