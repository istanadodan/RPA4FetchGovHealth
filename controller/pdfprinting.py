import os
from .context import Context
from .transaction import TRA
from app import get_config

_gdownload_folder = get_config('COMMON/download_folder',0)
_glaytency1 = get_config('LAYTENCY_TIME/printing_preview_',0)
_glaytency2 = get_config('LAYTENCY_TIME/printing_save',0)

class Printing_service1(TRA):
    def __init__(self):
        super().__init__('PDF다운로드')
        self.context = Context()

    def _initialize(self):
        if 'code' in self.context.info:
            self.title = '[{0}-{1}]{2}'.format(self.context.info['name'], self.context.info['code'],self.context.title)
        else:
            self.title = '[{0}]{2}'.format(self.context.info['name'],self.context.title)

        self._top = self.context.auto.PaneControl(searchDepth=1, Name=self.name("미리보기"))
        
    def req(self):
        self._initialize()

        self.begin("개시")
        _top = self._top
        self.act(_top,'activate')
        self.act(_top.DocumentControl(searchDepth=11,Name='Insert title here'))
        self.wait(int(_glaytency1))
        
        self.checkAndRetry()

        self.act(_top.ButtonControl(searchDepth=19,Name="인쇄"),'click')
        self.act(_top.ButtonControl(searchDepth=15,Name="인쇄"),'click')        
        self.wait(int(_glaytency2))
        
        self.act(_top.ButtonControl(searchDepth=4,Name="저장"))
        self.checkAndRetry()

        self.act(_top.ButtonControl(searchDepth=4,Name="저장"),'click')
        self.act(_top.EditControl(searchDepth=8,Name="파일 이름:"))
        self.checkAndRetry()

        # file save window
        self.begin("save_pdf")
        _full_path = os.path.join(_gdownload_folder, self.title+'.pdf')
        if os.path.exists(_full_path):
            os.remove(_full_path)

        # self.act(_top.EditControl(searchDepth=8,Name="파일 이름:"),'dbclick')
        self.act(_top.EditControl(searchDepth=8,Name="파일 이름:"),'sendkeys',text=_full_path) 
        self.act(_top.ButtonControl(searchDepth=3,Name="저장(S)"),'click')
        self.wait(1)

        if _top.ButtonControl(searchDepth=3,Name="저장(S)").Exists(0,0):
            self.doRetry()

        return _top


class Printing_service2(TRA):
    def __init__(self):
        super().__init__("Excel다운로드")
        self.context = Context()

    def _initialize(self):
        if 'code' in self.context.info:
            self.title = '[{0}-{1}]{2}'.format(self.context.info['name'], self.context.info['code'],self.context.title)
        else:
            self.title = '[{0}]{2}'.format(self.context.info['name'],self.context.title)
            
        self._top = self.context.auto.PaneControl(searchDepth=1, Name=self.name("웹EDI"))
        self._pre = self.context.auto.PaneControl(searchDepth=1, Name=self.name("미리보기"))

    def req(self):
        self._initialize()

        self.begin("개시")
        _top = self._top
        self.act(_top,'activate')
        self.act(_top.GroupControl(searchDepth=11,Name='img_open img_close'))
        self.checkAndRetry()
        
        self.act(_top.ImageControl(searchDepth=17,Name="img_open"),'click')
      
        # file save window
        self.begin("save_excel")
        _full_path = os.path.join(_gdownload_folder, self.title+'.xlsx')
        if os.path.exists(_full_path):
            os.remove(_full_path)

        self.act(_top.EditControl(searchDepth=8,Name="파일 이름:"))
        self.checkAndRetry()

        self.act(_top.EditControl(searchDepth=8,Name="파일 이름:"),'dbclick')
        self.act(_top.EditControl(searchDepth=8,Name="파일 이름:"),'sendkeys',text=_full_path) 
        self.act(_top.ButtonControl(searchDepth=3,Name="저장(S)"),'click')
        self.wait(1)

        if _top.ButtonControl(searchDepth=3,Name="저장(S)").Exists(0,0):
            self.doRetry()

        return self._pre