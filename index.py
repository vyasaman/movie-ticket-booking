from registeredUser import User
from unregisteredUser import User as unuser
from tkinter import *
import tkinter.ttk as tk
import json
from theatreAdmin import *
from pymysql import *
db = connect(host="localhost", user='root', port=3306,
             password='Aman@123', database='ticketbooking')
cur = db.cursor()
Unuser = unuser()
user = User()
ad = Admin()


def validate(t):
    cur.execute("select * from user_data where user_email='{}' and user_pass='{}'".format(
        username.get(), login_password.get()))
    res = cur.fetchone()
    if res[-1].lower() == 'admin':
        ad.admin_dashboard(res, t)
    elif res[-1].lower() == 'user':
        user.user_dashboard(res, t)
    else:
        msg.set('Invalid Details')


def login():

    top = Toplevel()
    top.geometry('500x400')
    back = Button(top, text='Go Back', relief=GROOVE,
                  command=top.destroy).place(x=450, y=0)
    head = Label(top, text="MyMovie", font=(
        "Arial", 25)).place(x=180, y=30)
    tag = Label(top, text="Movie Ticket Booking System").place(x=170, y=80)
    lab1 = Label(top, text='Login').place(x=20, y=140)
    e1 = Entry(top, textvariable=username).place(x=100, y=140)
    lab2 = Label(top, text='Password').place(x=20, y=170)
    e1 = Entry(top, textvariable=login_password).place(x=100, y=170)
    log = Button(top, text='Login', relief=GROOVE,
                 command=lambda: validate(top)).place(x=20, y=200)
    reg = Button(top, text='Register', relief=GROOVE,
                 command=lambda: register(top)).place(x=70, y=200)
    lab3 = Label(top, textvariable=msg, text='').place(x=50, y=250)


def register(t):
    t.destroy()
    top = Toplevel()
    top.geometry('500x400')
    lab = Label(top, text='Already have an account?').place(x=300, y=0)
    back = Button(top, text='Login', relief=GROOVE,
                  command=lambda: login(top)).place(x=450, y=0)
    head = Label(top, text="MyMovie", font=(
        "Arial", 25)).place(x=180, y=30)
    tag = Label(top, text="Movie Ticket Booking System").place(x=170, y=80)
    lab3 = Label(top, text='Enter Your Name').place(x=20, y=140)
    e3 = Entry(top, textvariable=userName).place(x=150, y=140)
    lab1 = Label(top, text='Enter Email').place(x=20, y=170)
    e1 = Entry(top, textvariable=email).place(x=150, y=170)
    lab2 = Label(top, text='Create Password').place(x=20, y=200)
    e2 = Entry(top, textvariable=newPassword).place(x=150, y=200)
    lab4 = Label(top, text='Enter Mobile number').place(x=20, y=230)
    e4 = Entry(top, textvariable=contact).place(x=150, y=230)

    reg = Button(top, text='Register', relief=GROOVE,
                 command=regValid).place(x=20, y=270)
    errmsg = Label(top, textvariable=msg, text='', font=(
        'arial', 15), fg='green').place(x=50, y=260)


def regValid():
    cur.execute("insert into user_data(user_email,user_pass,user_name,user_contact) values('{}','{}','{}',{})".format(
        email.get(), newPassword.get(), userName.get(), contact.get()))
    db.commit()
    msg.set('Registered Successfully')


def index():
    root.geometry("500x400")
    login = Button(root, text="Login", command=login)
    close = Button(root, text="Exit", command=root.destroy,
                   relief=GROOVE).place(x=450, y=0)
    head = Label(root, text="MyMovie", font=("Arial", 25)).place(x=180, y=30)
    tag = Label(root, text="Movie Ticket Booking System").place(x=170, y=80)
    lab1 = Label(root, text="Select State").place(x=70, y=120)
    state = tk.Combobox(root, textvariable=state_cb,
                        values=statedata).place(x=50, y=150)

    but = Button(root, text='Select this state', command=lambda: cityvalue(
        state_cb.get(), cityList)).place(x=200, y=145)
    cityList = tk.Combobox(root, textvariable=city_cb)
    search = Button(root, text="Search Movies", command=lambda: Unuser.showMovies(
        city_cb.get())).place(x=100, y=280)


def cityvalue(s, clist):
    print(s)
    for i in cityjson['states']:
        if i['state'] == s:
            clist['values'] = i['districts']
    lab2 = Label(root, text="Select City").place(x=70, y=180)
    clist.place(x=50, y=210)


root = Tk()

f = open('citydata.json')
cityjson = json.load(f)
statedata = ('Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chandigarh (UT)', 'Chhattisgarh', 'Dadra and Nagar Haveli (UT)', 'Daman and Diu (UT)', 'Delhi (NCT)', 'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jammu and Kashmir', 'Jharkhand', 'Karnataka',
             'Kerala', 'Lakshadweep (UT)', 'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram', 'Nagaland', 'Odisha', 'Puducherry (UT)', 'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttarakhand', 'Uttar Pradesh', 'West Bengal')


city_cb = StringVar()
state_cb = StringVar()
username = StringVar()
login_password = StringVar()
msg = StringVar()
userName = StringVar()
contact = IntVar()
email = StringVar()
newPassword = StringVar()

index()

root.mainloop()
