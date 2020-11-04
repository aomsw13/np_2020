from tkinter import*
from tkinter import messagebox
import tkinter
# from tkinter import Menu

# import sys
from email.parser import BytesParser, Parser
from email.policy import default
from socket import *
# def openfile():
#     file=filedialog.askopenfile()
#     name_file=Label(text=file).pack()
#     return
# # def sending():
# #     gui= Tk()
# #     gui.geometry("450x550")
# #     gui.title("Email Server")
# #     #text
# #     to= Label(text='To').pack()
# #     text_subject= Label(text='Subject').pack()

# #     #box
# #     from_add=Entry().pack()
# #     subject_box=Entry().pack()
# #     message=Entry().pack(ipadx=10,ipady=20)
    
# #     #butoon
# #     upload=Button(gui,text="upload",fg='red',command = openfile).pack()
# #     Button1=Button(gui,text="Submit",fg='red').pack()
# #     gui.mainloop()
  
# def login():
    
    
#     status = messagebox.askokcancel('Enter','Do you want to login ?')
#     if status ==0:
#         pass
#     else:
#         gui= Tk()
#         gui.geometry("450x550")
#         gui.title("Email Server")
#         #text
#         to= Label(text='To').pack()
#         text_subject= Label(text='Subject').pack()

#         #box
#         from_add=Entry().pack()
#         subject_box=Entry().pack()
#         message=Entry().pack(ipadx=10,ipady=20)
        
#         #butoon
#         upload=Button(gui,text="upload",fg='red',command = openfile).pack()
#         Button1=Button(gui,text="Submit",fg='red').pack()
#         gui.mainloop()        
#         sys.exit()
    
# gu1= Tk()
# gu1.geometry("450x550")
# gu1.title("Acoount")
# text = Label(text='Enter to your account ').pack(ipady=20)
 
# user=Entry()
# user.pack()
# password=Entry()
# password.pack()

# Button(gu1,text="Login",fg='red',command = login).pack()



# gu1.mainloop()
def main():
    root = Tk()
    app = Window2(root)
    root.mainloop()
############################################## Login ##########################################
# class Window1:
    # def __init__(self,master):
    #     self.master = master
    #     self.master.title("Login")
    #     self.master.geometry("430x550")
    #     self.frame=Frame(self.master)
    #     self.frame.pack()
    #     self.text=Label(self.frame,text='Login')
    #     self.text.pack()
    #     self.user=Entry(self.frame)
    #     self.user.pack()
    #     self.password=Entry(self.frame,show='*')
    #     self.password.pack()
    #     self.login = Button(self.frame,text='Login',fg='red',width=6,command=self.loginsys)
    #     self.login.pack()
       
    # def loginsys(self):
    #     self.status = messagebox.askokcancel('Enter','Do you want to login ?')
    #     if self.status ==0:
    #         pass
    #     else:
    #         self.newWinow = Toplevel(self.master)
    #         self.app = Window2(self.newWinow)
    # def new_window(self):
    #     self.newWinow = Toplevel(self.master)
    #     self.app = Window2(self.newWinow)
            
 #################################################### End ####################################   
class Window2:
    def __init__(self,master):
        self.master=master
        self.master.title("test")
        self.master.geometry("430x550")
        self.frame=Frame(self.master)
        self.frame.grid(row=10,column=10)
        self.text=Label(self.frame,text='Mail server')
        self.text.grid(row=0,column=1)
        self.text_from=Label(self.frame,text='From')
        self.text_from.grid(row=1,column=0)
     
        
                #box
        
        self.from_add=Entry(self.frame)
        self.from_add.grid(row=1,column=1)


        self.text_to=Label(self.frame,text='To')
        self.text_to.grid(row=2,column=0)

        self.to_add=Entry(self.frame)
        self.to_add.grid(row=2,column=1)
        self.subject_text=Label(self.frame,text='Subject')
        self.subject_text.grid(row=3,column=0)
        self.subject=Entry(self.frame)
        self.subject.grid(row=3,column=1)

        self.message=Text(self.frame, width= 50,height= 10)
        self.message.grid(row=4,column=1)

        self.upload = Entry(self.frame)
        self.upload.grid(row=5,column=1)

        #butoon
        # self.upload=Button(self.frame,text="upload",fg='red',command = self.openfile)
        # self.upload.grid(row=5,column=1)
        self.Button1=Button(self.frame,text="Submit",fg='red', command = self.sending)
        self.Button1.grid(row=6,column=1)
        ###################### imge
    # def openfile(self):
    #     self.file=filedialog.askopenfilename()
    #     self.name_file=Label(self.frame,text=self.file)
    #     self.name_file.grid(row=7,column=1)
        
    def sending (self):
       
        self.myHost = ''
        self.myPort = 8080
        self.sockobj = socket(AF_INET, SOCK_STREAM) 
        self.sockobj.bind((self.myHost, self.myPort)) 
        self.sockobj.listen(5)
        self.headers = Parser(policy=default).parsestr(
                'From: ' + self.from_add.get() +'\n '
                'To:'+ self.to_add.get()+'\n'
                'Subject:'+self.subject.get() +'\n'
                '\n'
                +(self.message.get('1.0',END))+'\n')
        # print(str(self.headers))
        # print(type(self.headers))
        
        self.f = open("data.txt",'a',encoding='utf8')
        # self.f.write('---------------------------------------------\n')
        self.f.write(str(self.headers))
        # self.f.write('\n---------------------------------------------\n')
        self.f.close()
        
        while True:
            self.connection, self.address = self.sockobj.accept() 
            print ('Server connected by', self.address)
            while 1:
                self.data = self.connection.recv(1024)
                if not self.data: break
                self.message = str(self.headers).encode('utf-8') + self.data
             
                self.connection.send(self.message)
        self.connection.close()
        # print('To: {}'.format(self.headers['To']))
        # print('From: {}'.format(self.headers['from']))
        # print('Subject: {}'.format(self.headers['subject']))
        # print('Recipient username: {}'.format(self.headers['to'].addresses[0].username))
        # You can also access the parts of the addresses:
    # def server(self):
       
    #     self.myHost = ''
    #     self.myPort = 50007
    #     self.sockobj = socket(AF_INET, SOCK_STREAM) 
    #     self.sockobj.bind((self.myHost, self.myPort)) 
    #     self.sockobj.listen(5)
    #     self.headers = Parser(policy=default).parsestr(
    #             'From: ' + self.from_add.get() +'\n '
    #             '\nTo:'+ self.subject_box.get()+'\n'
    #             'Subject: Hello\n'
    #             '\n'
    #             'Body would go here\n')
    #     while True:
    #         self.connection, self.address = self.sockobj.accept() 
    #         print ('Server connected by', self.address)
    #         while 1:
    #             self.data = self.connection.recv(1024)
    #             if not self.data: break
    #             self.message = self.headers.encode('utf-8') + self.data
    #             self.connection.send(self.message)
    #     self.connection.close()
  

        
        
if __name__ == "__main__":
    main()
    
