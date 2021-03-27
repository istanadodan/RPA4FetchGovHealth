from .context import Context
from .transaction import TRA
from .pdfprinting import Printing_service1,Printing_service2
from app import get_config

_glatency1 = get_config('LAYTENCY_TIME/detail_doc_print_button',0)
# 사업장고지내역서
class Detail_service1(TRA):
    def __init__(self):
        super().__init__('게시물세부화면')
        self.context = Context()
        
    def _initialize(self):
        self._top = self.context.auto.PaneControl(searchDepth=1, Name=self.name("웹EDI"))
        self.printing_service = Printing_service1()

    def req(self):
        self._initialize()

        self.begin("개시")
        self.act(self._top,'activate')
        self.act(self._top.ImageControl(searchDepth=16, Name="img_tab2"))
        self.checkAndRetry()
        
        self.wait(int(_glatency1))

        # 출력버튼 클릭
        self.act(self._top.ImageControl(searchDepth=16, Name="img_print"),'click')
        
        # 인쇄화면으로 전이
        _window = self.printing_service.req()
                
        # 작업완료되면 작업창 닫기
        # 닫기버튼은 노드를 별개로 지정해서 버튼을 찾도록 한다.
        # 단순히 최상단에서 Name으로 찾는 경우, can move the cursor경고가 나옴.
        # (참고)프로세스 제거시 - subprocess.check_call(['taskkill','/F','/T','/IM',str(_im)])
        _menu = _window.PaneControl(searchDepth=2,Name='Chrome')
        _menu.ButtonControl(searchDepth=2, Name='닫기').Click()
        
        self._top.SetActive()
        #서식닫기버튼 클릭
        self._top.ImageControl(searchDepth=16,Name="img_close").Click()

# 개별고지내역서
class Detail_service2(TRA):
    def __init__(self):
        super().__init__('게시물세부화면')
        self.context = Context()
        
    def _initialize(self):
        self._top = self.context.auto.PaneControl(searchDepth=1, Name=self.name("웹EDI"))
        self.printing_service = Printing_service2()

    def req(self):
        self._initialize()

        self.begin("개시")
        
        self.act(self._top,'activate')
        self.act(self._top.TextControl(searchDepth=23, Name="1"))
        self.act(self._top.ImageControl(searchDepth=16, Name="bt_FileDw"))
        self.checkAndRetry()

        # 출력버튼 클릭
        self.act(self._top.ImageControl(searchDepth=16, Name="bt_FileDw"),'click')
        
        # 다운로드화면을 곧바로 연다
        self.printing_service.req()

        self._top.SetActive()
        #서식닫기버튼 클릭
        self._top.ImageControl(searchDepth=16,Name="img_close").Click()


                

