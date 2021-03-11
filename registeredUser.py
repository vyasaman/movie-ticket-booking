from tkinter import *

from pymysql import *
db = connect(host="localhost", user='root', port=3306,
             password='Aman@123', database='ticketbooking')
cur = db.cursor()


class User:

    def showMovies(self):
        pass

    def showTheatre(self):
        pass

    def bookTicket(self):
        pass

    def offers(self):
        pass

    def giftGards(self):
        pass

    def profileUpdate(self):
        pass

    def user_dashboard(self, res, t):
        t.destroy()
        pass
