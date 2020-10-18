# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

from tkinter import *


def clicked():
    lable = Label(window, text="Hello New Clicked", font=("Arial Bold", 20))
    lable.grid(column=0, row=0)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    window = Tk()

    window.title("Welcome to ITCS428 Project")
    window.geometry('750x450')

    lbl = Label(window, text="Hello", font=("Arial Bold", 20))

    lbl.grid(column=0, row=0)

    btn = Button(window, text="Click Me", command=clicked)

    btn.grid(column=1, row=0)

    window.mainloop()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
