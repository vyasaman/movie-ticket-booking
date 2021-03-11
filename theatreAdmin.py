from tkinter import *
from pymysql import *
db = connect(host="localhost", user='root', port=3306,
             password='Aman@123', database='ticketbooking')
cur = db.cursor()


class Admin:
    def addTheatre(self):

        pass

    def addMovie(self):
        pass

    def update(self):
        pass

    def addAdmin(self, t):
        t.destroy()
        top = Toplevel()
        top.geometry('500x400')
        close = Button(top, tex="Back", command=top.destroy)
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
                     command=self.regValid).place(x=20, y=270)
        errmsg = Label(top, textvariable=msg, text='').place(x=50, y=260)

    def regValid(self):
        cur.execute("insert into user_data(user_email,user_pass,user_name,user_contact,user_role) values('{}','{}','{}',{},'Admin')".format(
            email.get(), newPassword.get(), userName.get(), contact.get()))
        db.commit()
        msg.set('Registered Successfully')

    def admin_dashboard(self, res, t):
        t.destroy()
        top = Toplevel()
        top.geometry("500x400")
        out = Button(top, text="Logout", command=self.top.destroy,
                     relief=GROOVE).place(x=450, y=0)
        head = Label(top, text="MyMovies.in", font=(
            'arial', 25)).place(x=170, y=30)
        head = Label(top, text=res[3]+"'s Dashboard",
                     font=('arial', 15)).place(x=170, y=80)
        but1 = Button(top, text="Add Theatre",
                      command=lambda: self.addTheatre).place(x=100, y=150)
        but1 = Button(top, text="Add Movie",
                      command=lambda: self.addMovie(top)).place(x=250, y=150)
        but1 = Button(top, text="Update Movie",
                      command=lambda: self.update(top)).place(x=100, y=200)
        but1 = Button(top, text="Add Admin",
                      command=lambda: self.addAdmin(top)).place(x=250, y=200)


userName = StringVar()
contact = IntVar()
email = StringVar()
newPassword = StringVar()
msg = StringVar()
