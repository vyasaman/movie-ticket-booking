from tkinter import *
import tkinter.ttk as tk


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


def dash(c):

    top = Toplevel()
    top.geometry('500x400')
    back = Button(top, text='Go Back', relief=GROOVE,
                  command=top.destroy).place(x=450, y=0)


def index():
    root = Tk()
    root.geometry("500x400")
    close = Button(root, text="Exit", command=root.destroy,
                   relief=GROOVE).place(x=450, y=0)
    head = Label(root, text="MyMovie", font=("Arial", 25)).place(x=180, y=30)
    tag = Label(root, text="Movie Ticket Booking System").place(x=170, y=80)
    city = tk.Combobox(root)
    city['values'] = ('Select Your City', 'Bhopal', 'Indore',
                      'Delhi', 'Mumbai', 'Heydrabad', 'Banglore')
    city.current(0)
    city.place(x=100, y=200)
    go = Button(root, text='Go', command=lambda: dash(
        city.current()), relief=GROOVE).place(x=300, y=200)
    root.mainloop()


index()
