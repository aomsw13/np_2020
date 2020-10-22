# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

from tkinter import *
from tkinter import ttk

if __name__ == '__main__':
    window = Tk()

    window.title("Welcome to ITCS428 Project")
    window.geometry('750x450')

    tabControl = ttk.Notebook(window)

    dnsTab = ttk.Frame(tabControl)
    ftpTab = ttk.Frame(tabControl)
    emailTab = ttk.Frame(tabControl)
    webTab = ttk.Frame(tabControl)

    tabControl.add(dnsTab, text='DNS')
    tabControl.add(ftpTab, text='FTP')
    tabControl.add(emailTab, text='Email')
    tabControl.add(webTab, text='Web')
    tabControl.pack(expand=1, fill="both")

    ttk.Label(dnsTab,
              text="Welcome to \
    GeeksForGeeks").grid(column=0,
                         row=0,
                         padx=30,
                         pady=30)

    # lable = Label(dnsTab, text="DNS", font=("Arial Bold", 10)).place(x=375, y=20)
    # # lable.grid(column=2, row=0)
    # search = Label(dnsTab, text="Search:").place(x=255, y=50)
    # v = StringVar()
    # input = Entry(dnsTab, width=25, textvariable=v)
    # input.pack()
    # input.grid(column=1, row=0)
    # input = v.get()
    # goBtn = Button(dnsTab, text="Go!", command=goDNS(input)).place(x=450, y=47)

    window.mainloop()