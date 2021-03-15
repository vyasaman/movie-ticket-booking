from tkinter import *
import smtplib as smtp
import tkinter.ttk as tk
import json
from pymysql import *
db = connect(host="localhost", user='root', port=3306,
             password='Aman@123', database='ticketbooking')
cur = db.cursor()


class RegisteredUser:
    def showMovies(self, r, t):
        t.destroy()
        top = Toplevel()
        top.geometry('500x400')
        head = Label(top, text="Location"+r[-1], font=('arial', 15)).pack()
        cur.execute(
            "select movie.mov_id, movie.mov_name, theatre.th_id from movie inner join theatre on movie.theatre=theatre.th_id where theatre.City like '%{}%'".format(r[-1]))
        res = cur.fetchall()
        res = list(res)
        close = Button(top, text="Back", command=top.destroy,
                       relief=GROOVE).place(x=450, y=0)
        li1 = []
        p = 0
        for i in range(len(res)):
            p = i
            if res[i][1] in li1:
                continue
            else:
                li1.append(res[i][1])
                lab2 = Label(top, text=res[i][1], bg="yellow",
                             fg="red", borderwidth=2, relief=SOLID, font=("arial", 14)).place(x=100, y=(i*40)+150)
        lab3 = Label(top, text="Select Movie").place(x=100, y=((p+1)*40)+150)
        movieCB = tk.Combobox(top, textvariable=moviedata, values=li1).place(
            x=100, y=((p+2)*40)+150)
        but1 = Button(top, text="Show Theatres", command=lambda: self.showTheatre(moviedata.get(), top, res, r[-1], r[2])).place(
            x=250, y=((p+2)*40)+150)

    def showTheatre(self, movie, t, r1, r2, sendingMail):
        top = Toplevel()
        top.geometry('400x300')
        cur.execute("select th_name from theatre inner join movie on theatre.th_id = movie.theatre where movie.mov_name='{}' and theatre.City='{}'".format(
            movie, r2))
        res1 = cur.fetchall()
        Res = []
        for i in res1:
            Res.append(i[0])
        lab = Label(top, text="Select Theatre").place(x=100, y=70)
        thCB = tk.Combobox(top, textvariable=th_cb,
                           values=Res).place(x=100, y=100)
        but = Button(top, text="Select",
                     command=lambda: self.selectTime(movie, th_cb.get(), t, top, r2, sendingMail)).place(x=100, y=150)

    def selectTime(self, movie, thname, t, t2, c, sendingMail):
        t2.destroy()

        cur.execute(
            "select time1 from movie inner join theatre on movie.theatre=theatre.th_id where mov_name = '{}' and th_name='{}' and theatre.City='{}'".format(movie, thname, c))
        res1 = cur.fetchall()

        showtime = []
        for i in res1:
            showtime.append(self.time(i[0]))
        top = Toplevel()
        top.geometry('400x300')
        but = Button(top, text='Cancel', command=top.destroy).place(x=250, y=0)
        lab1 = Label(top, text="Select Timings").place(x=50, y=50)
        cb = tk.Combobox(top, textvariable=showTiming,
                         values=showtime).place(x=100, y=100)

        but = Button(top, text="Submit",
                     command=lambda: self.bookTicket(t, top, showTiming.get(), movie, c, thname, sendingMail)).place(x=100, y=200)

    def bookTicket(self, t1, t2, mov_time, movie, c, thname, sendingMail):
        data = json.load(open('seatsdata.json'))
        t1.destroy()
        t2.destroy()
        top = Toplevel()
        top.geometry("500x500")
        lab = Label(top, bg='red').place(
            height=10, width=15, x=20, y=10)

        lab = Label(top, text='Not Available').place(x=37, y=5)
        lab = Label(top, bg='blue').place(
            height=10, width=15, x=20, y=22)
        lab = Label(top, text='Available').place(height=17, x=37, y=20)
        head = Label(top, text="Select Your Seats", font=('arial', 18)).pack()
        head1 = Label(top, text=movie, font=('arial', 14)).pack()
        head2 = Label(top, text=thname).pack()
        d1 = data[c][movie][thname][mov_time]
        p = 50
        q = 50
        screen = Label(top, relief='solid', borderwidth=2).place(
            height=10, width=400, x=50, y=250)
        lab1 = Label(top, text="Screen This Way").place(x=200, y=270)
        for i in d1:
            seat = Label(top, font=('arial', 15), relief='solid')
            if i[0] == 'A':
                if d1[i] == 0:
                    seat.config(text=i, fg='blue')
                    seat.place(width=30, height=35, x=(p), y=80)
                else:
                    seat.config(text=i, fg='red')
                    seat.place(width=30, height=35, x=(p), y=80)
                p += 50
            else:

                if d1[i] == 0:
                    seat.config(text=i, fg='blue')
                    seat.place(width=30, height=35, x=(q), y=130)
                else:
                    seat.config(text=i, fg='red')
                    seat.place(width=30, height=35, x=(q), y=130)
                q += 50

        lab2 = Label(top, text="Enter Seat Name").place(x=50, y=300)
        e1 = Entry(top, textvariable=seatEntry).place(x=150, y=300)
        lab3 = Label(top, text="(Seperated by spaces for Multiple Entries)").place(
            x=50, y=329)
        but = Button(top, text="Select Seats", command=lambda: self.bookValidate(
            top, mov_time, movie, thname, seatEntry.get(), c, sendingMail)).place(height=25, x=280, y=297)
        error = Label(top, text='', textvariable=errorMsg,
                      fg='red', font=('arial', 14)).place(x=100, y=350)

    def bookValidate(self, t, mov_time, movie, thname, seat, c, sendingMail):
        seatList = []
        try:
            temp = seat.split(" ")
            seatList = temp
        except EXCEPTION:
            errorMsg.set(
                "Invalid Input!\n Give Correct Seat Details in correct Format")
        seatdata = json.load(open('seatsdata.json'))

        d1 = seatdata[c][movie][thname][mov_time]
        temp = True
        for i in seatList:
            if i in d1:
                temp = True
            else:
                errorMsg.set("Invalid Seat Detail:- "+i)
                temp = False
                break
        if temp == True:
            self.confirmBooking(t, movie, thname, c,
                                mov_time, seatList, d1, sendingMail)

    def time(self, ti):
        ti = str(ti)
        ti = ti.split(":")
        ampm = ""
        if int(ti[0]) > 12:
            ti[0] = int(ti[0])-12
            ti[0] = str(ti[0])
            ampm = 'PM'
        elif int(ti[0]) == 12:
            ti[0] = str(int(ti[0]))
            ampm = 'PM'
        else:
            ampm = 'AM'
        ti.pop(2)
        ti = ':'.join(ti)
        ti += ampm
        return ti

    def timeHr(self, t):
        t = t.split(":")
        if int(t[0]) < 12:
            t[0] = str(int(t[0])+12)
        return ':'.join(t)

    def confirmBooking(self, t, movie, thname, c, mov_time, seatList, d1, sendingMail):
        tempTime = mov_time[:-2]
        if mov_time[-2:] == 'PM':
            tempTime = self.timeHr(mov_time[:-2])

        cur.execute("select movie.ticket_price from movie inner join theatre on movie.theatre=theatre.th_id where movie.mov_name='{}' and theatre.th_name='{}' and theatre.City='{}' and movie.time1='{}'".format(
            movie, thname, c, tempTime))
        res = cur.fetchone()
        print(tempTime)
        totalSeats = len(seatList)
        t.destroy()
        top = Toplevel()
        top.geometry('500x400')
        head = Label(top, text="Confirm Booking", font=('arial', 20)).pack()
        lab1 = Label(top, text="Movie Name").place(x=50, y=130)
        lab2 = Label(top, text="Theatre").place(x=50, y=160)
        lab3 = Label(top, text="City").place(x=50, y=190)
        lab4 = Label(top, text="Movie Timing").place(x=50, y=220)
        lab5 = Label(top, text="Price of Ticket").place(x=50, y=250)
        lab6 = Label(top, text="Online Booking Tax").place(x=50, y=280)
        lab7 = Label(top, text="Net Ammount").place(x=50, y=310)

        dat1 = Label(top, text=movie).place(x=250, y=130)
        dat2 = Label(top, text=thname).place(x=250, y=160)
        dat3 = Label(top, text=c).place(x=250, y=190)
        dat4 = Label(top, text=mov_time).place(x=250, y=220)
        dat5 = Label(top, text=str(
            res[0]*totalSeats)+"(for {} Tickets)".format(totalSeats)).place(x=250, y=250)
        dat6 = Label(top, text="8% on Total Price").place(x=250, y=280)
        tot = res[0]*len(seatList)
        net = tot+tot*8/100
        dat7 = Label(top, text="{}".format(net)
                     ).place(x=250, y=310)

        cnfrm = Button(top, text="Confirm Ticket", command=lambda: self.payment(
            top, movie, thname, mov_time, c, seatList, sendingMail)).place(x=350, y=350)
        cancel = Button(top, text="Cancel",
                        command=top.destroy).place(x=450, y=350)

    def payment(self, t, movie, thname, mov_time, c, seatList, sendingMail):
        t.destroy()

        def click(*args):
            cno.delete(0, END)
            cno2.delete(0, END)
            netuname.delete(0, END)
            netpswd.delete(0, END)
            upid.delete(0, END)

        top = Toplevel()
        top.geometry('500x400')
        head = Label(top, text="Payment Gateway", font=('arial', 20)).pack()
        head2 = Label(top, text='Select Payment Option').pack()
        lab1 = Label(top, text='Enter e-mail address').place(x=100, y=100)
        payCB = tk.Combobox(top, textvariable=payOption)
        payCB['values'] = ("Payment Method", "Debit Card", "Credit Card", "Net Banking",
                           "UPI", "Wallets", 'Pay at Counter')
        payCB.current(0)
        payCB.place(x=100, y=130)
        but = Button(top, text='Select', comman=lambda: selectPay(
            payOption.get())).place(x=250, y=127)

        cno = Entry(top)
        cno.bind("<Button-1>", click)
        month = tk.Combobox(top)
        month['values'] = ['Expiry Month', 'January', 'February', 'March', 'April',
                           'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        month.current(0)
        year = tk.Combobox(top)
        year['values'] = ['Expiry year', 2021, 2022, 2023, 2024,
                          2025, 2026, 2027, 2028, 2029, 2030, 2031, 2032, 2033]
        year.current(0)

        cno2 = Entry(top)
        cno2.bind("<Button-1>", click)
        month2 = tk.Combobox(top)
        month2['values'] = ['Expiry Month', 'January', 'February', 'March', 'April',
                            'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        month2.current(0)

        year2 = tk.Combobox(top)
        year2['values'] = ['Expiry year', 2021, 2022, 2023, 2024,
                           2025, 2026, 2027, 2028, 2029, 2030, 2031, 2032, 2033]
        year2.current(0)

        netuname = Entry(top)
        netuname.bind("<Button-1>", click)

        netpswd = Entry(top)
        netpswd.bind("<Button-1>", click)

        upid = Entry(top)
        upid.bind("<Button-1>", click)

        but1 = Button(top, text='Paytm')
        but2 = Button(top, text='Google Pay')
        but3 = Button(top, text='PhonePe')

        def selectPay(pay):
            if pay == 'Debit Card':

                cno.place(width=210, x=100, y=160)
                month.place(width=100, x=100, y=187)
                year.place(width=100, x=210, y=187)
                cno.delete(0, END)
                cno.insert(END, "Enter Card Number")
                cno2.place_forget()
                month2.place_forget()
                year2.place_forget()
                netpswd.place_forget()
                netuname.place_forget()
                upid.place_forget()
                but1.place_forget()
                but2.place_forget()
                but3.place_forget()

            elif pay == 'Credit Card':
                cno2.place(width=210, x=100, y=160)
                cno2.insert(END, "Enter Card Number")
                month2.place(width=100, x=100, y=187)
                year2.place(width=100, x=210, y=187)

                cno.place_forget()
                month.place_forget()
                year.place_forget()
                netpswd.place_forget()
                netuname.place_forget()
                but1.place_forget()
                but2.place_forget()
                but3.place_forget()

            elif pay == 'Net Banking':
                netuname.place(width=200, x=100, y=160)
                netpswd.place(width=200, x=100, y=190)
                netuname.insert(END, "Enter NetBanking ID")
                netpswd.insert(END, "Enter Password")

                cno.place_forget()
                month.place_forget()
                year.place_forget()
                cno2.place_forget()
                month2.place_forget()
                year2.place_forget()
                upid.place_forget()
                but1.place_forget()
                but2.place_forget()
                but3.place_forget()

            elif pay == "UPI":
                upid.place(width=200, x=100, y=160)
                upid.insert(END, "Enter UPI ID")

                cno.place_forget()
                month.place_forget()
                year.place_forget()
                cno2.place_forget()
                month2.place_forget()
                year2.place_forget()
                netpswd.place_forget()
                netuname.place_forget()
                but1.place_forget()
                but2.place_forget()
                but3.place_forget()

            elif pay == "Wallets":
                but1.place(x=100, y=160)
                but2.place(x=200, y=160)
                but3.place(x=300, y=160)

                cno.place_forget()
                month.place_forget()
                year.place_forget()
                cno2.place_forget()
                month2.place_forget()
                year2.place_forget()
                upid.place_forget()
                netpswd.place_forget()
                netuname.place_forget()

            else:
                cno.place_forget()
                month.place_forget()
                year.place_forget()
                cno2.place_forget()
                month2.place_forget()
                year2.place_forget()
                upid.place_forget()
                netpswd.place_forget()
                netuname.place_forget()
                but1.place_forget()
                but2.place_forget()
                but3.place_forget()
            but4 = Button(top, text="Pay", command=lambda: self.generateTicket(
                top, movie, thname, mov_time, c, seatList, pay, sendingMail)).place(x=200, y=230)

    def generateTicket(self, t, movie, thname, mov_time, c, seatList, pay, sendingMail):

        tempTime = mov_time[:-2]
        if mov_time[-2:] == 'PM':
            tempTime = self.timeHr(mov_time[:-2])
        cur.execute("select movie.ticket_price from movie inner join theatre on movie.theatre=theatre.th_id where movie.mov_name='{}' and theatre.th_name='{}' and theatre.City='{}' and movie.time1='{}'".format(
            movie, thname, c, tempTime))
        res = cur.fetchone()
        print(tempTime)

        t.destroy()
        top = Toplevel()
        top.geometry('500x400')
        head = Label(top, text="Booking Confirm", font=('arial', 20)).pack()
        head2 = Label(top, text="Ticket Generated", font=('arial', 15)).pack()
        lab1 = Label(top, text="Movie Name").place(x=50, y=100)
        lab2 = Label(top, text="Theatre").place(x=50, y=130)
        lab3 = Label(top, text="City").place(x=50, y=160)
        lab4 = Label(top, text="Movie Timing").place(x=50, y=190)
        lab5 = Label(top, text="Price of Ticket").place(x=50, y=220)
        lab6 = Label(top, text="Online Booking Tax").place(x=50, y=250)
        lab9 = Label(top, text='Discounted Price').place(x=50, y=280)
        lab7 = Label(top, text="Net Ammount").place(x=50, y=310)
        lab8 = Label(top, text='Seat Details').place(x=50, y=340)

        dat1 = Label(top, text=movie).place(x=250, y=100)
        dat2 = Label(top, text=thname).place(x=250, y=130)
        dat3 = Label(top, text=c).place(x=250, y=160)
        dat4 = Label(top, text=mov_time).place(x=250, y=190)
        dat5 = Label(top, text=str(
            res[0]*len(seatList))+"(Rs for {} Tickets)".format(len(seatList))).place(x=250, y=220)
        dat6 = Label(top, text="+8% on Total Price").place(x=250, y=250)
        tot = res[0]*len(seatList)
        if len(seatList) >= 3:
            if pay == 'Debit Card' or pay == 'UPI':
                tot = tot-(tot*5/100)
            elif pay == 'Credit Card':
                tot = tot-(tot*8/100)
            else:
                tot = tot-(tot*1/100)
        dat9 = Label(top, text="{} Rs".format(tot)).place(x=250, y=280)

        net = tot+tot*12/100
        dat7 = Label(top, text="{}".format(net)
                     ).place(x=250, y=310)
        dat8 = Label(top, text=', '.join(seatList)).place(x=250, y=340)

        totamt = str(net)
        print(sendingMail)
        cur.execute(
            "select user_id from user_data where user_email='{}'".format(sendingMail))
        result = cur.fetchone()

        cur.execute("insert into booking(book_mov,book_th,book_seats,book_time,book_city,book_user) values('{}','{}','{}','{}','{}',{})".format(
            movie, thname, ', '.join(seatList), tempTime, c, result[0]))
        db.commit()

        cur.execute("select book_id from booking where book_mov='{}' and book_th='{}' and book_city='{}' and book_time='{}'".format(
            movie, thname, c, tempTime))
        res1 = cur.fetchone()

        sender = 'amanvyas720@gmail.com'
        reciver = [sendingMail]
        msg = """
        From: MyMovie.in
        To: """+sendingMail+"""

        Subject: Movie Ticket Booking Confirm


                    MyMovie.in

                 Ticket Generated

            Movie         '{}'

            Booking ID     {}

            Theatre       '{}'

            Booked Seats  '{}'

            City          '{}'

            Show Timing   '{}'

            Total Price   '{}'

            Payment Mode  '{}'

         """.format(movie, res1[0], thname, ', '.join(seatList), c, mov_time, totamt, pay)

        data = json.load(open('seatsdata.json'))
        for i in seatList:
            print(c, movie, thname, mov_time, i)
            data[c][movie][thname][mov_time][i] = 1
            json.dump(data, open('seatsdata.json', "w"))

        try:
            server = smtp.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender, '8823074130')
            server.sendmail(sender, reciver, msg)
            print("Email sent Successfuly")

        except Exception as e:
            print(e)

    def bookHistory(self, res):
        bookhist = StringVar()
        cur.execute(
            "select * from booking where book_user = {}".format(res[0]))
        result = cur.fetchall()
        li = []
        for i in result:
            li.append(str(i[0])+' - '+i[1])

        top = Toplevel()
        top.geometry('500x500')
        head = Label(top, text='Booking History', font=('arial', 20)).pack()
        cb = tk.Combobox(top, textvariable=bookhist,
                         values=li).place(x=150, y=50)
        but = Button(top, text='Search', command=lambda: self.searchHist(
            bookhist.get(), top)).place(x=300, y=50)

    def searchHist(self, history, top):
        history = history.split(" - ")

        cur.execute(
            "select * from booking where book_id={}".format(int(history[0])))
        res = cur.fetchone()
        lab1 = Label(top, text='Booking ID').place(x=50, y=150)
        lab2 = Label(top, text='Movie').place(x=50, y=180)
        lab3 = Label(top, text='Theatre').place(x=50, y=210)
        lab4 = Label(top, text='Seats').place(x=50, y=240)
        lab5 = Label(top, text='Timing').place(x=50, y=270)
        lab6 = Label(top, text='City').place(x=50, y=300)

        dat1 = Label(top, text=str(res[0])).place(x=250, y=150)
        dat2 = Label(top, text=res[1]).place(x=250, y=180)
        dat3 = Label(top, text=res[2]).place(x=250, y=210)
        dat4 = Label(top, text=res[3]).place(x=250, y=240)
        dat5 = Label(top, text=res[4]).place(x=250, y=270)
        dat6 = Label(top, text=res[5]).place(x=250, y=300)

    def giftGards(self):
        pass

    def showProfile(self, res):

        dataName = StringVar()
        dataEmail = StringVar()
        dataPass = StringVar()
        dataContact = IntVar()
        dataCity = StringVar()

        top = Toplevel()
        top.geometry('550x400')
        head = Label(top, text='User Profile', font=('arial', 20)).pack()

        lab1 = Label(top, text="Name").place(x=50, y=130)
        lab2 = Label(top, text="E-Mail").place(x=50, y=160)
        lab3 = Label(top, text="Password").place(x=50, y=190)
        lab4 = Label(top, text="Contact Number").place(x=50, y=220)
        lab5 = Label(top, text="City").place(x=50, y=250)

        dat1 = Entry(top, textvariable=dataName,
                     fg='green').place(x=250, y=130)
        dat2 = Entry(top, textvariable=dataEmail,
                     fg='green').place(x=250, y=160)
        dat3 = Entry(top, textvariable=dataPass,
                     fg='green').place(x=250, y=190)
        dat4 = Entry(top, textvariable=dataContact,
                     fg='green').place(x=250, y=220)
        dat5 = Entry(top, textvariable=dataCity,
                     fg='green').place(x=250, y=250)
        dataName.set(res[1])
        dataEmail.set(res[2])
        dataPass.set(res[3])
        dataContact.set(res[4])
        dataCity.set(res[-1])

        but1 = Button(top, text='Update Name', command=lambda: self.profileUpdate(
            res[2], 'user_name', dataName.get(), 0)).place(x=400, y=130)
        but2 = Button(top, text='Update email', command=lambda: self.profileUpdate(
            res[2], 'user_email', dataEmail.get(), 0)).place(x=400, y=160)
        but3 = Button(top, text='Update password', command=lambda: self.profileUpdate(
            res[2], 'user_pass', dataPass.get(), 0)).place(x=400, y=190)
        but4 = Button(top, text='Update contact', command=lambda: self.profileUpdate(
            res[2], 'user_mob', dataContact.get(), 1)).place(x=400, y=220)
        but5 = Button(top, text='Update city', command=lambda: self.profileUpdate(
            res[2], 'user_city', dataCity.get(), 0)).place(x=400, y=250)

    def profileUpdate(self, res, col, userdata, flag):
        if flag == 0:
            cur.execute(
                "update user_data set {} = '{}' where user_email = '{}'".format(col, userdata, res))
            db.commit()
            print('Updated')
        elif flag == 1:
            cur.execute("update user_data set {} = {} where user_email = '{}'".format(
                col, userdata, res))
            db.commit
            print('Updated')

    def user_dashboard(self, res, t):
        t.destroy()
        top = Toplevel()
        top.geometry('500x400')
        name = Label(top, text="AMan Vyas", fg='white',
                     bg='black').place(x=10, y=0)
        head = Label(top, text="Dashboard", font=('arial', 20)).pack()

        frame = Label(top, bg='white').place(
            height=200, width=350, x=50, y=100)
        but1 = Button(top, text='Book Tickets', command=lambda: self.showMovies(res, top), relief=GROOVE).place(
            width=150, x=70, y=160)
        but2 = Button(top, text='Gift Cards', relief=GROOVE).place(
            width=150, x=70, y=190)
        but3 = Button(top, text='Update Profile', command=lambda: self.showProfile(res), relief=GROOVE).place(
            width=150, x=230, y=190)
        but4 = Button(top, text='Booking History', command=lambda: self.bookHistory(res), relief=GROOVE).place(
            width=150, x=230, y=160)


class UnRegisteredUser:
    def showMovies(self, c):
        top = Toplevel()
        top.geometry("500x400")
        cur.execute("select movie.mov_id, movie.mov_name, theatre.th_id from movie inner join theatre on movie.theatre=theatre.th_id where theatre.City like '%{}%'".format(c))
        res = cur.fetchall()
        res = list(res)
        close = Button(top, text="Back", command=top.destroy,
                       relief=GROOVE).place(x=450, y=0)
        head = Label(top, text="MyMovie", font=(
            "Arial", 25)).place(x=180, y=30)
        tag = Label(top, text="Movie Ticket Booking System").place(x=170, y=80)
        lab1 = Label(top, text="Movies in "+c,
                     font=('arial', 16)).place(x=170, y=110)
        li1 = []
        for i in range(len(res)):
            if res[i][1] in li1:
                continue
            else:
                li1.append(res[i][1])
                lab2 = Label(top, text=res[i][1], bg="yellow",
                             fg="red", borderwidth=2, relief=SOLID, font=("arial", 14)).place(x=100, y=(i*40)+150)
        lab3 = Label(top, text="Select Movie").place(x=100, y=((i+1)*40)+150)
        movieCB = tk.Combobox(top, textvariable=moviedata, values=li1).place(
            x=100, y=((i+2)*40)+150)
        but1 = Button(top, text="Show Theatres", command=lambda: self.selectTheatre(moviedata.get(), top, res, c)).place(
            x=250, y=((i+2)*40)+150)

    def selectTheatre(self, movie, t, res, c):
        top = Toplevel()
        top.geometry('400x300')
        cur.execute("select th_name from theatre inner join movie on theatre.th_id = movie.theatre where movie.mov_name='{}' and theatre.City='{}'".format(
            movie, c))
        res1 = cur.fetchall()
        Res = []
        for i in res1:
            Res.append(i[0])
        lab = Label(top, text="Select Theatre").place(x=100, y=70)
        thCB = tk.Combobox(top, textvariable=th_cb,
                           values=Res).place(x=100, y=100)
        but = Button(top, text="Select",
                     command=lambda: self.selectTime(movie, th_cb.get(), t, top, c)).place(x=100, y=150)

    def selectTime(self, movie, thname, t, t1, c):

        t1.destroy()

        cur.execute(
            "select time1 from movie inner join theatre on movie.theatre=theatre.th_id where mov_name = '{}' and th_name='{}' and theatre.City='{}'".format(movie, thname, c))
        res1 = cur.fetchall()

        showtime = []
        for i in res1:
            showtime.append(self.time(i[0]))
        top = Toplevel()
        top.geometry('400x300')
        but = Button(top, text='Cancel', command=top.destroy).place(x=250, y=0)
        lab1 = Label(top, text="Select Timings").place(x=50, y=50)
        cb = tk.Combobox(top, textvariable=showTiming,
                         values=showtime).place(x=100, y=100)

        but = Button(top, text="Submit",
                     command=lambda: self.bookTicket(t, top, showTiming.get(), movie, c, thname)).place(x=100, y=200)

    def bookTicket(self, t1, t2, mov_time, movie, c, thname):
        data = json.load(open('seatsdata.json'))
        t1.destroy()
        t2.destroy()
        top = Toplevel()
        top.geometry("500x500")
        lab = Label(top, bg='red').place(
            height=10, width=15, x=20, y=10)

        lab = Label(top, text='Not Available').place(x=37, y=5)
        lab = Label(top, bg='blue').place(
            height=10, width=15, x=20, y=22)
        lab = Label(top, text='Available').place(height=17, x=37, y=20)
        head = Label(top, text="Select Your Seats", font=('arial', 18)).pack()
        head1 = Label(top, text=movie, font=('arial', 14)).pack()
        head2 = Label(top, text=thname).pack()
        d1 = data[c][movie][thname][mov_time]
        p = 50
        q = 50
        screen = Label(top, relief='solid', borderwidth=2).place(
            height=10, width=400, x=50, y=250)
        lab1 = Label(top, text="Screen This Way").place(x=200, y=270)
        for i in d1:
            seat = Label(top, font=('arial', 15), relief='solid')
            if i[0] == 'A':
                if d1[i] == 0:
                    seat.config(text=i, fg='blue')
                    seat.place(width=30, height=35, x=(p), y=80)
                else:
                    seat.config(text=i, fg='red')
                    seat.place(width=30, height=35, x=(p), y=80)
                p += 50
            else:

                if d1[i] == 0:
                    seat.config(text=i, fg='blue')
                    seat.place(width=30, height=35, x=(q), y=130)
                else:
                    seat.config(text=i, fg='red')
                    seat.place(width=30, height=35, x=(q), y=130)
                q += 50

        lab2 = Label(top, text="Enter Seat Name").place(x=50, y=300)
        e1 = Entry(top, textvariable=seatEntry).place(x=150, y=300)
        lab3 = Label(top, text="(Seperated by spaces for Multiple Entries)").place(
            x=50, y=329)
        but = Button(top, text="Select Seats", command=lambda: self.bookValidate(
            top, mov_time, movie, thname, seatEntry.get(), c)).place(height=25, x=280, y=297)
        error = Label(top, text='', textvariable=errorMsg,
                      fg='red', font=('arial', 14)).place(x=100, y=350)

    def bookValidate(self, t, mov_time, movie, thname, seat, c):
        seatList = []
        try:
            temp = seat.split(" ")
            seatList = temp
        except EXCEPTION:
            errorMsg.set(
                "Invalid Input!\n Give Correct Seat Details in correct Format")
        seatdata = json.load(open('seatsdata.json'))

        d1 = seatdata[c][movie][thname][mov_time]
        temp = True
        for i in seatList:
            if i in d1:
                temp = True
            else:
                errorMsg.set("Invalid Seat Detail:- "+i)
                temp = False
                break
        if temp == True:
            self.confirmBooking(t, movie, thname, c, mov_time, seatList, d1)

    def timeHr(self, t):
        t = t.split(":")
        if int(t[0]) < 12:
            t[0] = str(int(t[0])+12)
        return ':'.join(t)

    def confirmBooking(self, t, movie, thname, c, mov_time, seatList, d1):

        tempTime = mov_time[:-2]
        if mov_time[-2:] == 'PM':
            tempTime = self.timeHr(mov_time[:-2])

        cur.execute("select movie.ticket_price from movie inner join theatre on movie.theatre=theatre.th_id where movie.mov_name='{}' and theatre.th_name='{}' and theatre.City='{}' and movie.time1='{}'".format(
            movie, thname, c, tempTime))
        res = cur.fetchone()
        print(tempTime)
        totalSeats = len(seatList)
        t.destroy()
        top = Toplevel()
        top.geometry('500x400')
        head = Label(top, text="Confirm Booking", font=('arial', 20)).pack()
        lab1 = Label(top, text="Movie Name").place(x=50, y=130)
        lab2 = Label(top, text="Theatre").place(x=50, y=160)
        lab3 = Label(top, text="City").place(x=50, y=190)
        lab4 = Label(top, text="Movie Timing").place(x=50, y=220)
        lab5 = Label(top, text="Price of Ticket").place(x=50, y=250)
        lab6 = Label(top, text="Online Booking Tax").place(x=50, y=280)
        lab7 = Label(top, text="Net Ammount").place(x=50, y=310)

        dat1 = Label(top, text=movie).place(x=250, y=130)
        dat2 = Label(top, text=thname).place(x=250, y=160)
        dat3 = Label(top, text=c).place(x=250, y=190)
        dat4 = Label(top, text=mov_time).place(x=250, y=220)
        dat5 = Label(top, text=str(
            res*totalSeats)+"(for  Tickets)").place(x=250, y=250)
        dat6 = Label(top, text="8% on Total Price").place(x=250, y=280)
        tot = res[0]*len(seatList)
        net = tot+tot*8/100
        dat7 = Label(top, text="{}".format(net)
                     ).place(x=250, y=310)

        cnfrm = Button(top, text="Confirm Ticket", command=lambda: self.payment(
            top, movie, thname, mov_time, c, seatList)).place(x=350, y=350)
        cancel = Button(top, text="Cancel",
                        command=top.destroy).place(x=450, y=350)

    def payment(self, t, movie, thname, mov_time, c, seatList):
        t.destroy()

        def click(*args):
            cno.delete(0, END)
            cno2.delete(0, END)
            netuname.delete(0, END)
            netpswd.delete(0, END)
            upid.delete(0, END)

        top = Toplevel()
        top.geometry('500x400')
        head = Label(top, text="Payment Gateway", font=('arial', 20)).pack()
        head2 = Label(top, text='Select Payment Option').pack()
        lab1 = Label(top, text='Enter e-mail address').place(x=100, y=100)
        email = Entry(top, textvariable=senderEmail).place(x=250, y=100)
        payCB = tk.Combobox(top, textvariable=payOption)
        payCB['values'] = ("Payment Method", "Debit Card", "Credit Card", "Net Banking",
                           "UPI", "Wallets", 'Pay at Counter')
        payCB.current(0)
        payCB.place(x=100, y=130)
        but = Button(top, text='Select', comman=lambda: selectPay(
            payOption.get())).place(x=250, y=127)

        cno = Entry(top)
        cno.bind("<Button-1>", click)
        month = tk.Combobox(top)
        month['values'] = ['Expiry Month', 'January', 'February', 'March', 'April',
                           'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        month.current(0)
        year = tk.Combobox(top)
        year['values'] = ['Expiry year', 2021, 2022, 2023, 2024,
                          2025, 2026, 2027, 2028, 2029, 2030, 2031, 2032, 2033]
        year.current(0)

        cno2 = Entry(top)
        cno2.bind("<Button-1>", click)
        month2 = tk.Combobox(top)
        month2['values'] = ['Expiry Month', 'January', 'February', 'March', 'April',
                            'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        month2.current(0)

        year2 = tk.Combobox(top)
        year2['values'] = ['Expiry year', 2021, 2022, 2023, 2024,
                           2025, 2026, 2027, 2028, 2029, 2030, 2031, 2032, 2033]
        year2.current(0)

        netuname = Entry(top)
        netuname.bind("<Button-1>", click)

        netpswd = Entry(top)
        netpswd.bind("<Button-1>", click)

        upid = Entry(top)
        upid.bind("<Button-1>", click)

        but1 = Button(top, text='Paytm')
        but2 = Button(top, text='Google Pay')
        but3 = Button(top, text='PhonePe')

        def selectPay(pay):
            if pay == 'Debit Card':

                cno.place(width=210, x=100, y=160)
                month.place(width=100, x=100, y=187)
                year.place(width=100, x=210, y=187)
                cno.delete(0, END)
                cno.insert(END, "Enter Card Number")
                cno2.place_forget()
                month2.place_forget()
                year2.place_forget()
                netpswd.place_forget()
                netuname.place_forget()
                upid.place_forget()
                but1.place_forget()
                but2.place_forget()
                but3.place_forget()

            elif pay == 'Credit Card':
                cno2.place(width=210, x=100, y=160)
                cno2.insert(END, "Enter Card Number")
                month2.place(width=100, x=100, y=187)
                year2.place(width=100, x=210, y=187)

                cno.place_forget()
                month.place_forget()
                year.place_forget()
                netpswd.place_forget()
                netuname.place_forget()
                but1.place_forget()
                but2.place_forget()
                but3.place_forget()

            elif pay == 'Net Banking':
                netuname.place(width=200, x=100, y=160)
                netpswd.place(width=200, x=100, y=190)
                netuname.insert(END, "Enter NetBanking ID")
                netpswd.insert(END, "Enter Password")

                cno.place_forget()
                month.place_forget()
                year.place_forget()
                cno2.place_forget()
                month2.place_forget()
                year2.place_forget()
                upid.place_forget()
                but1.place_forget()
                but2.place_forget()
                but3.place_forget()

            elif pay == "UPI":
                upid.place(width=200, x=100, y=160)
                upid.insert(END, "Enter UPI ID")

                cno.place_forget()
                month.place_forget()
                year.place_forget()
                cno2.place_forget()
                month2.place_forget()
                year2.place_forget()
                netpswd.place_forget()
                netuname.place_forget()
                but1.place_forget()
                but2.place_forget()
                but3.place_forget()

            elif pay == "Wallets":
                but1.place(x=100, y=160)
                but2.place(x=200, y=160)
                but3.place(x=300, y=160)

                cno.place_forget()
                month.place_forget()
                year.place_forget()
                cno2.place_forget()
                month2.place_forget()
                year2.place_forget()
                upid.place_forget()
                netpswd.place_forget()
                netuname.place_forget()

            else:
                cno.place_forget()
                month.place_forget()
                year.place_forget()
                cno2.place_forget()
                month2.place_forget()
                year2.place_forget()
                upid.place_forget()
                netpswd.place_forget()
                netuname.place_forget()
                but1.place_forget()
                but2.place_forget()
                but3.place_forget()
            but4 = Button(top, text="Pay", command=lambda: self.finalBooking(
                top, movie, thname, mov_time, c, seatList, pay, senderEmail.get())).place(x=200, y=230)

    def finalBooking(self, t, movie, thname, mov_time, c, seatList, pay, sendingMail):

        tempTime = mov_time[:-2]
        if mov_time[-2:] == 'PM':
            tempTime = self.timeHr(mov_time[:-2])
        cur.execute("select movie.ticket_price from movie inner join theatre on movie.theatre=theatre.th_id where movie.mov_name='{}' and theatre.th_name='{}' and theatre.City='{}' and movie.time1='{}'".format(
            movie, thname, c, tempTime))
        res = cur.fetchone()
        print(tempTime)

        t.destroy()
        top = Toplevel()
        top.geometry('500x400')
        head = Label(top, text="Booking Confirm", font=('arial', 20)).pack()
        head2 = Label(top, text="Ticket Generated", font=('arial', 15)).pack()
        lab1 = Label(top, text="Movie Name").place(x=50, y=100)
        lab2 = Label(top, text="Theatre").place(x=50, y=130)
        lab3 = Label(top, text="City").place(x=50, y=160)
        lab4 = Label(top, text="Movie Timing").place(x=50, y=190)
        lab5 = Label(top, text="Price of Ticket").place(x=50, y=220)
        lab6 = Label(top, text="Online Booking Tax").place(x=50, y=250)
        lab7 = Label(top, text="Net Ammount").place(x=50, y=280)
        lab8 = Label(top, text='Seat Details').place(x=50, y=310)

        dat1 = Label(top, text=movie).place(x=250, y=100)
        dat2 = Label(top, text=thname).place(x=250, y=130)
        dat3 = Label(top, text=c).place(x=250, y=160)
        dat4 = Label(top, text=mov_time).place(x=250, y=190)
        dat5 = Label(top, text=str(
            res[0]*len(seatList))+"(for {} Tickets)".format(len(seatList))).place(x=250, y=220)
        dat6 = Label(top, text="8% on Total Price").place(x=250, y=250)
        tot = res[0]*len(seatList)
        net = tot+tot*8/100
        dat7 = Label(top, text="{}".format(net)
                     ).place(x=250, y=280)
        dat8 = Label(top, text=', '.join(seatList)).place(x=250, y=310)

        totamt = str(net)

        cur.execute("insert into booking(book_mov,book_th,book_seats,book_time,book_city) values('{}','{}','{}','{}','{}')".format(
            movie, thname, ', '.join(seatList), tempTime, c))
        db.commit()

        cur.execute("select book_id from booking where book_mov='{}' and book_th='{}' and book_city='{}' and book_time='{}'".format(
            movie, thname, c, tempTime))
        res1 = cur.fetchone()

        sender = 'amanvyas720@gmail.com'
        reciver = [sendingMail]
        msg = """
        From: MyMovie.in
        To: """+sendingMail+"""

        Subject: Movie Ticket Booking Confirm


                    MyMovie.in

                 Ticket Generated

            Movie         '{}'

            Booking ID     {}

            Theatre       '{}'

            Booked Seats  '{}'

            City          '{}'

            Show Timing   '{}'

            Total Price   '{}'

            Payment Mode  '{}'

         """.format(movie, res1[0], thname, ', '.join(seatList), c, mov_time, totamt, pay)

        data = json.load(open('seatsdata.json'))
        for i in seatList:
            print(c, movie, thname, mov_time, i)
            data[c][movie][thname][mov_time][i] = 1
            json.dump(data, open('seatsdata.json', "w"))

        try:
            server = smtp.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender, '8823074130')
            server.sendmail(sender, reciver, msg)
            print("Email sent Successfuly")

        except Exception as e:
            print(e)

    def time(self, ti):
        ti = str(ti)
        ti = ti.split(":")
        ampm = ""
        if int(ti[0]) > 12:
            ti[0] = int(ti[0])-12
            ti[0] = str(ti[0])
            ampm = 'PM'
        elif int(ti[0]) == 12:
            ti[0] = str(int(ti[0]))
            ampm = 'PM'
        else:
            ampm = 'AM'
        ti.pop(2)
        ti = ':'.join(ti)
        ti += ampm
        return ti


class Administrator:
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
        e3 = Entry(top, textvariable=uname).place(x=150, y=140)
        lab1 = Label(top, text='Enter Email').place(x=20, y=170)
        e1 = Entry(top, textvariable=e_mail).place(x=150, y=170)
        lab2 = Label(top, text='Create Password').place(x=20, y=200)
        e2 = Entry(top, textvariable=pswd).place(x=150, y=200)
        lab4 = Label(top, text='Enter Mobile number').place(x=20, y=230)
        e4 = Entry(top, textvariable=cont).place(x=150, y=230)
        reg = Button(top, text='Register', relief=GROOVE,
                     command=regValid).place(x=20, y=270)
        errmsg = Label(top, text='', textvariable=msg).place(x=50, y=260)

    def regValid(self):
        cur.execute("insert into user_data(user_email,user_pass,user_name,user_contact,user_role) values('{}','{}','{}',{},'Admin')".format(
            e_mail.get(), pswd.get(), uname.get(), cont.get()))
        db.commit()
        msg.set('Registered Successfully')

    def admin_dashboard(self, res, t):
        t.destroy()
        top = Toplevel()
        top.geometry("500x400")
        out = Button(top, text="Logout", command=top.destroy,
                     relief=GROOVE).place(x=450, y=0)
        head = Label(top, text="MyMovies.in", font=(
            'arial', 25)).place(x=170, y=30)
        head = Label(top, text=res[3]+"'s Dashboard",
                     font=('arial', 15)).place(x=170, y=80)
        but1 = Button(top, text="Add Theatre",
                      command=lambda: addTheatre).place(x=100, y=150)
        but1 = Button(top, text="Add Movie",
                      command=lambda: addMovie(top)).place(x=250, y=150)
        but1 = Button(top, text="Update Movie",
                      command=lambda: update(top)).place(x=100, y=200)
        but1 = Button(top, text="Add Admin",
                      command=lambda: addAdmin(top)).place(x=250, y=200)


def validate(t):
    cur.execute("select * from user_data where user_email='{}' and user_pass='{}'".format(
        username.get(), login_password.get()))
    res = cur.fetchone()
    if res[-2].lower() == 'admin':
        ad.admin_dashboard(res, t)
    elif res[-2].lower() == 'user':
        user.user_dashboard(res, t)
    else:
        msg.set('Invalid Details')
    username.set("")
    login_password.set("")


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
    e2 = Entry(top, textvariable=login_password, show='*')
    e2.place(x=100, y=170)
    log = Button(top, text='Login', relief=GROOVE,
                 command=lambda: validate(top)).place(x=20, y=200)
    reg = Button(top, text='Register', relief=GROOVE,
                 command=lambda: register(top)).place(x=70, y=200)
    lab3 = Label(top, textvariable=msg, text='').place(x=50, y=250)


def register(t):
    t.destroy()
    top = Toplevel()
    top.geometry('500x400')
    back = Button(top, text='Back', relief=GROOVE,
                  command=lambda: top.destroy()).place(x=450, y=0)
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
    lab5 = Label(top, text='Select State').place(x=20, y=260)
    cb1 = tk.Combobox(top, textvariable=state_cb2,
                      values=statedata).place(x=150, y=260)
    cb2 = tk.Combobox(top, textvariable=city_cb2)
    st = Button(top, text='Select',
                command=lambda: city2(state_cb2.get(), cb2, top)).place(x=300, y=260)
    reg = Button(top, text='Register', relief=GROOVE,
                 command=lambda: regValid(userName.get(), email.get(), newPassword.get(), contact.get(), city_cb2.get())).place(x=20, y=350)


def city2(s, cli, top):
    for i in cityjson['states']:
        if i['state'] == s:
            cli['values'] = i['districts']
    cli.place(x=150, y=290)
    lab = Label(top, text='Select City').place(x=20, y=290)


def regValid(un, em, pa, con, ci):
    cur.execute("insert into user_data(user_email,user_pass,user_name,user_mob,user_city) values('{}','{}','{}',{},'{}')".format(
        em, pa, un, con, ci))
    db.commit()

    top = Toplevel()
    top.geometry('300x200')
    lab = Label(top, text='Registered Successfully',
                font=('airal', 15), fg='green').place(x=50, y=50)
    but = Button(top, text='OK', command=top.destroy).place(x=250, y=130)
    email.set("")
    userName.set("")
    newPassword.set("")
    contact.set(0)


def index():
    root.geometry("500x400")
    log = Button(root, text="Login", command=login)
    close = Button(root, text="Exit", command=root.destroy,
                   relief=GROOVE).place(x=450, y=0)
    log = Button(root, text='Login', command=lambda: login(),
                 relief=GROOVE).place(x=400, y=0)
    head = Label(root, text="MyMovie", font=("Arial", 25)).place(x=180, y=30)
    tag = Label(root, text="Movie Ticket Booking System").place(x=170, y=80)
    lab1 = Label(root, text="Select State").place(x=70, y=120)
    state = tk.Combobox(root, textvariable=state_cb,
                        values=statedata).place(x=50, y=150)

    cityList = tk.Combobox(root, textvariable=city_cb)
    but = Button(root, text='Select this state', command=lambda: cityvalue(
        state_cb.get(), cityList)).place(x=200, y=145)
    search = Button(root, text="Search Movies", relief=GROOVE, command=lambda: ureg.showMovies(
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

ad = Administrator()
user = RegisteredUser()
ureg = UnRegisteredUser()
city_cb = StringVar()
state_cb = StringVar()
username = StringVar()
login_password = StringVar()
msg = StringVar()
userName = StringVar()
contact = IntVar()
email = StringVar()
newPassword = StringVar()
e_mail = StringVar()
pswd = StringVar()
uname = StringVar()
cont = IntVar()
moviedata = StringVar()
showTiming = StringVar()
th_cb = StringVar()
seatid = StringVar()
seatEntry = StringVar()
errorMsg = StringVar()
payOption = StringVar()
senderEmail = StringVar()
state_cb2 = StringVar()
city_cb2 = StringVar()

index()

root.mainloop()
