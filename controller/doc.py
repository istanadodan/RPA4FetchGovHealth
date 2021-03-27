from .context import Context
from .transaction import TRA

class Doc_service(TRA):
    def __init__(self):
        super().__init__('받은문서화면')
        self.context = Context()
       
    def _initialize(self):
        self.top=self.context.auto.PaneControl(searchDepth=1, Name=self.name("국민건강보험 EDI"))

    def req(self):
        self._initialize()

        self.begin("개시")
        self.act(self.top,'activate')
        self.act(self.top.HyperlinkControl(searchDepth=8, Name="받은문서 바로가기"))
        self.checkAndRetry()
        
        self.act(self.top.HyperlinkControl(searchDepth=8, Name="받은문서 바로가기"),'click')
        