import subprocess
from threading import Thread
from .context import Context
from .login import Login_service,Login2_service
from .doc import Doc_service
from .board import Board_service
from .logout import Logout_service

class Cntl(Thread):

    def __init__(self):
        Thread.__init__(self)
        self.unFinished_tasks = []
        self.context = Context()
        self.retry = False
    
    def model(self,model):
        self.model = model
        self.context.set(auto=self.model.auto)

    def thread_initialize(self):
        self.context.auto.InitializeUIAutomationInCurrentThread()
        newRoot = self.context.auto.GetRootControl()
        self.context.auto.EnumAndLogControl(newRoot, 1)
        self.context.auto.UninitializeUIAutomationInCurrentThread()

    def run(self):
        corps = self.model.get_task_list() if not self.unFinished_tasks \
           else self.unFinished_tasks
        if not corps: return

        self.open_page()

        for corp in corps:
            print(corp['name'],"<작업개시>")
            self.context.clear_tasks()
            self.input(corp)
            try:
                self.login()
                self.preparation()
                self.processing()
                self.logout()

            except Exception as e:
                print("<오류> ",e)
                print(corp['name'], "<처리보류>")
                if e.args[0] =='STOP':
                    print("<사용자중지>")
                    self.context.messagebox('작업이 중지되었습니다.')
                    return

                self.unFinished_tasks.append(corp)
                self.retry==True
                try:
                    _test = self.context.auto.PaneControl(searchDepth=1, Name=self.name("웹EDI"))
                    if _test.Exists(0,0):
                        _test.PaneControl(searchDepth=2,Name='Chrome').GetFirstChildControl().GetLastChildControl().Click()

                    _test = self.context.auto.PaneControl(searchDepth=1, Name=self.name("국민건강보험 EDI"))
                    if _test.Exists(0,0):
                        _test.ImageControl(searchDepth=9,Name='로그아웃').Click()
                    
                    # subprocess.check_call(['taskkill','/F','/T','/IM',self.model.processId])
                except Exception: pass

                self.open_page()
        
        if self.retry==False and self.unFinished_tasks: 
            print([task['name'] for task in self.unFinished_tasks],"<작업재시도>")
            self.retry=True
            self.run()
        
        self.model.close_page()
        self.context.messagebox('작업이 완료되었습니다.')

    #open brower
    def open_page(self):
        self.model.open_page()

    #input certificate info
    def input(self, info):
        self.context.set(info=info)

    #login through certification from hard disk or usb media
    def login(self):
        _proc = Login_service()
        _proc.req()

        if 'subid' in self.context.info:
            Login2_service().req()

    #open inbox page to the board
    def preparation(self):
        _proc = Doc_service()
        _proc.req()

    #select a post and carry out printing for the pdf file and circulate the processing
    def processing(self):
        _proc = Board_service()
        _proc.req()

    #login through certification from hard disk or usb media
    def logout(self):
        _proc = Logout_service()
        _proc.req()