from .context import Context
from .transaction import TRA

class Logout_service(TRA):
    def __init__(self):
        super().__init__('로그아웃')
        self.context = Context()
        
    def _initialize(self):
        self._top = self.context.auto.PaneControl(searchDepth=1, Name=self.name("웹EDI"))
        self.home = self.context.auto.PaneControl(searchDepth=1, Name=self.name("국민건강보험 EDI"))

    def req(self):
        self._initialize()
        self.begin("문서닫기개시")

        print("close window")
        self.act(self._top,'activate')
        self.checkAndRetry()
        self._top.PaneControl(searchDepth=2,Name='Chrome').GetFirstChildControl().GetLastChildControl().Click()

        self.wait(0.5)

        print("logout")
        self.act(self.home,'activate')
        self.checkAndRetry()
        self.home.ImageControl(searchDepth=9,Name='로그아웃').Click()
