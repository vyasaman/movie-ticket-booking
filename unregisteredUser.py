from tkinter import *
import tkinter.ttk as tk
import booking

from pymysql import *
db = connect(host="localhost", user='root', port=3306,
             password='Aman@123', database='ticketbooking')
cur = db.cursor()


class User:

    def showMovies(self, c):
        self.c = c
        top = Toplevel()
        top.geometry("500x400")
        cur.execute("select movie.mov_id, movie.mov_name, theatre.th_id from movie inner join theatre on movie.theatre=theatre.th_id where theatre.City like '%{}%'".format(c))
        res = cur.fetchall()
        close = Button(top, text="Back", command=top.destroy,
                       relief=GROOVE).place(x=450, y=0)
        head = Label(top, text="MyMovie", font=(
            "Arial", 25)).place(x=180, y=30)
        tag = Label(top, text="Movie Ticket Booking System").place(x=170, y=80)

        lab1 = Label(top, text="Movies in "+self.c,
                     font=('arial', 16)).place(x=170, y=110)
        li1 = []
        for i in range(len(res)):
            li1.append(res[i])
            lab2 = Label(top, text=res[i][1], bg="yellow",
                         fg="red", borderwidth=2, relief=SOLID, font=("arial", 14)).place(x=100, y=(i*40)+150)
        lab3 = Label(top, text="Select Movie").place(x=100, y=((i+1)*40)+150)
        cb = tk.Combobox(top, textvariable=moviesdata,
                         values=tuple(li1[1])).place(x=200, y=((i+1)*40)+150)
        but1 = Button(top, text="Show Timings", command=lambda: self.selectTime(moviesdata.get(), res, top)).place(
            x=100, y=((i+2)*40)+150)

    def selectTime(self, mov, res, t):
        cur.execute(
            "select time1,time2,time3 from movie where mov_name='{}' and theatre={}".format(mov, res[2]))
        res1 = cur.fetchone()
        res1 = [i for i in res1 if i]
        showtime = []

        for i in res1:
            showtime.append(time(i))

        top = Toplevel()
        top.geometry('400x300')
        lab1 = Label(top, text="Select Timings").place(x=50, y=50)
        cb = tk.Combobox(top, textvariable=timing, values=showtime)
        but = Button(top, text="Submit",
                     command=lambda: self.selectTime(t, top, timing.get()))

    def showTheatre(self):
        pass

    def bookTicket(self, t1, t2, showtiming):

        pass

    def time(self, ti):
        ti = str(ti)
        ti = ti.split(":")
        ampm = ""
        if int(ti[0]) > 12:
            ti[0] = int(ti[0])-12
            ti[0] = str(ti[0])
            ampm = 'PM'
        else:
            ampm = 'AM'
        ti.pop(2)
        ti = ':'.join(ti)
        ti += ampm
        return ti


moviesdata = StringVar()
timing = StringVar()
