from tkinter import Tk, Button, Label, Text, Frame, Scrollbar, messagebox, StringVar, Entry
from controller import Context
from app import get_config

class View(Tk):
    def __init__(self):
        super().__init__()
        self.context = Context()
        self.context.messagebox = lambda msg:messagebox.showinfo("완료",msg)
        self._initialize()
        self.show()

    def _initialize(self):
        self.title('RPA V0.1')
        self.geometry("220x120+%d+%d"%(self.centering()))
        self.stop_flag = False
      
    def centering(self):
        self.update_idletasks()
        x = (self.winfo_screenwidth() - self.winfo_width())/3
        y = (self.winfo_screenheight() - self.winfo_height())/3
        return x,y

    def model(self, m):
        self.model = m

    def show(self):
        self.auth_input = StringVar(self)
        #,bg='dim gray'
        f1 = Frame(self)
        l_pw = Label(f1,text='실행코드',relief="flat")
        e_pw = Entry(f1,textvariable=self.auth_input, bg='powder blue',relief="flat")
        l_pw.pack(side='left')
        e_pw.pack(side='right',fill='x',expand=True,padx=2)

        f2 = Frame(self)
        b1 = Button(f2,text='START',command=self.start)
        b2 = Button(f2,text="STOP",command=self.stop)
        b2.config(state='disabled')
        b1.pack(side='left',fill='both',expand=True,padx=5,pady=1)
        b2.pack(side='left',fill='both',expand=True,padx=5,pady=1)

        f3 = Frame(self)
        b3 = Button(f3,text="CREATE KEY",command=self.create_key)
        b3.pack(fill='both',padx=5,pady=1)

        f1.pack(side='top', fill='x')
        f3.pack(side='bottom', fill='x')
        f2.pack(side='top', fill='both', expand=True)

        self.start_button = b1
        self.stop_button = b2
        
        self.auth_input.set("etners2020!!!")
    def create_key(self):
        from model import create_file
        try:
            create_file(self.auth_input.get())
        except Exception as e:
            self.context.messagebox(e)
            return
        
        self.context.messagebox('키생성이 완료되었습니다.')

    def start(self):
        
        if not self.model.check_password(self.auth_input.get()): 
            messagebox.showerror("에러",'인증키가 일치하지 않습니다.')
            self.auth_input.set("")
            return

        self.start_button.config(state='disabled')
        self.stop_button.config(state='normal')
        
        self.cntl.thread_initialize()
        self.cntl.daemon = True
        self.cntl.start()

    def handler(self, c):
        self.cntl = c

    def print(self, log):
        self.dsp.insert('end',log+'\n')

    def stop(self):
        if self.stop_flag:
            self.destroy()
            return

        self.start_button.config(state='disabled')
        self.context.set(exit=1)
        self.stop_flag = True