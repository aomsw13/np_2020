# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

from tkinter import *
from tkinter import ttk
import dns as dns
import dns.resolver

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

    # DNS

    lable = Label(dnsTab, text="DNS : ")
    lable.pack()
    lable.grid(column=0, row=0)
    inputDns = Entry(dnsTab, width=10)
    inputDns.grid(column=1, row=0)

    def searchDns():
        lable.configure(text="DNS : ")
        result = dns.resolver.resolve(inputDns.get(), 'MX')
        for data in result:
            outputDNS = ttk.Label(text=data.exchange.to_text())
            outputDNS.pack()

    btnDns = Button(dnsTab, text="Search", command=searchDns)
    btnDns.grid(column=2, row=0)

    # ttk.Label(dnsTab,
    #           text="Welcome to \
    # GeeksForGeeks").grid(column=0,
    #                      row=0,
    #                      padx=30,
    #                      pady=30)

    window.mainloop()
