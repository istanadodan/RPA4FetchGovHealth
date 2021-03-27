from .transaction import TRA
from .context import Context
from app import get_config

_gmedia_type = get_config('COMMON/media_type')
_gusb_name = get_config('COMMON/usb_media_name')
_gsite_name = get_config('SITE/name')
_glatency1 = get_config('LAYTENCY_TIME/login_certificate')

class Login_service(TRA):
    def __init__(self):
        super().__init__('LOGIN')
        self.context = Context()
       
    def _initialize(self):
        self.top = self.context.auto.PaneControl(searchDepth=1, Name=self.name(_gsite_name))

    def req(self):
        self._initialize()

        self.begin("개시")
        self.act(self.top, 'activate')
        self.act(self.top.ImageControl(searchDepth=7,Name='공동인증서 로그인'))
        self.checkAndRetry()
        #대기시간
        self.wait(int(_glatency1))

        self.act(self.top.ImageControl(searchDepth=7,Name='공동인증서 로그인'), 'click')
        
        if _gmedia_type=='1': self._hard_disk()
        elif _gmedia_type=='2': self._usb_disk()

    def _hard_disk(self):
        self.begin("hard_disk")

        self.act(self.top.GroupControl(searchDepth=6, Name='인증서 위치'))
        self.checkAndRetry()

        self.act(self.top.RadioButtonControl(searchDepth=11, Name='하드디스크'), 'click')

        self._select_certificate()

    def _usb_disk(self):
        self.begin("usb_disk")

        _top = self.act(self.top.GroupControl(searchDepth=6, Name='인증서 위치') )
        self.checkAndRetry()

        _step1 = self.top.RadioButtonControl(searchDepth=11, Name='이동식디스크')
        self.act(_step1, 'click')
        self.checkAndRetry()

        # 세부정보는 다음이웃노드에 존재
        _step2 = _step1.GetNextSiblingControl()
        
        _dev_name =_step2.GetFirstChildControl().Name
        # btn_name: NAME1 (A:) NMAE2 (B:)
        _cert_list = _dev_name.replace(') ','),').split(',')
        _found = [ i for i, name in enumerate(_cert_list) if _gusb_name in name ]

        if not _found:
            raise Exception("인증서가 존재하지 않음")

        usb_idx = _found[0] + 1
        self.act(_step2.ListControl(Name=_dev_name).ListItemControl(searchDepth=1, foundIndex=usb_idx), 'click')
        
        self._select_certificate()

    def _select_certificate(self):
        _corp = self.context.info['name']
        _pos = self.top.GroupControl(searchDepth=6, Name='인증서 위치')

        _tbl = _pos.GetNextSiblingControl()
        #header at 0-th position
        _step = _tbl.GetFirstChildControl().GetFirstChildControl()
        
        while _step:
            print(_step.Name)
            if _corp in _step.Name:
                #화면표시여부check
                self._check_and_wheel(_tbl,_step)

                #list대상: take(comp, nTH, children, action) y=-18
                self.take(_step,2,0,'click',y=-18)
                # self.take(_step.GetChildren(),2,0,'click')
                break
            _step = _step.GetNextSiblingControl()
        
        self.checkAndRetry()

        self.act(self.top.GetParentControl().EditControl(searchDepth=11,Name="인증서 암호"),'dbclick')
        self.act(self.top.GetParentControl().EditControl(searchDepth=11,Name="인증서 암호"),"sendkeys",text=self.context.info['passwd'])
        self.act(self.top.GetParentControl().ButtonControl(searchDepth=7,Name="확인"), 'click')

    #화면에 보이지않는 경우, 휠조작처리.
    def _check_and_wheel(self, scroller, data):
        # print('class',type(scroller))
        if not isinstance(scroller, self.context.auto.WindowControl): 
            print('not instance')
            return

        while data.IsOffscreen:
            print('data.IsOffscreen',data.IsOffscreen)
            scroller.WheelDown()
            self.wait(1)


class Login2_service(TRA):
    def __init__(self):
        super().__init__('SUB_LOGIN')
        self.context = Context()
       
    def _initialize(self):
        self.top = self.context.auto.PaneControl(searchDepth=1, Name=self.name(_gsite_name))

    def req(self):
        self._initialize()

        self.begin("개시")
        self.act(self.top, 'activate')
        self.act(self.top.EditControl(searchDepth=10, Name='아이디'))
        self.checkAndRetry()

        _id, _pw = self.context.info['subid'], self.context.info['subpw'] 
        self.act(self.top.EditControl(searchDepth=10, Name='아이디'),'dbclick')
        self.act(self.top.EditControl(searchDepth=10, Name='아이디'),'sendkeys',text=_id)

        self.act(self.top.EditControl(searchDepth=10, Name='비밀번호'),'dbclick')
        self.act(self.top.EditControl(searchDepth=10, Name='비밀번호'),'sendkeys',text=_pw)

        self.wait(0.5)
        _frame = self.top.EditControl(searchDepth=10, Name='아이디')
        self.act(_frame.GetParentControl().GetNextSiblingControl(),'click')

        self.wait(2)
