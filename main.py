# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

from tkinter import *


def clicked_DNS():
    lable = Label(window, text="Welcome to DNS", font=("Arial Bold", 20))
    lable.grid(column=1, row=0)

def clicked_FTP():
    lable = Label(window, text="Welcome to FTP", font=("Arial Bold", 20))
    lable.grid(column=1, row=0)

def clicked_Email():
    lable = Label(window, text="Welcome to Email", font=("Arial Bold", 20))
    lable.grid(column=1, row=0)

def clicked_Web():
    lable = Label(window, text="Welcome to Web", font=("Arial Bold", 20))
    lable.grid(column=1, row=0)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    window = Tk()

    window.title("Welcome to ITCS428 Project")
    
    window.geometry('750x450')

    lbl = Label(window, text="Menu", font=("Arial Bold", 20), bg="grey", width=7, height=2)
    lbl.grid(column=0, row=0)

    btn_DNS = Button(window, text="DNS", command=clicked_DNS, width=10, height=2)
    btn_DNS.grid(column=0, row=1)

    btn_FTP = Button(window, text="FTP", command=clicked_FTP, width=10, height=2)
    btn_FTP.grid(column=0, row=2)

    btn_Email = Button(window, text="Email", command=clicked_Email, width=10, height=2)
    btn_Email.grid(column=0, row=3)

    btn_Web = Button(window, text="Web", command=clicked_Web, width=10, height=2)
    btn_Web.grid(column=0, row=4)

    window.mainloop()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
