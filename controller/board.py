import re
from datetime import datetime, date
from .context import Context
from .transaction import TRA
from .doc_detail import Detail_service1,Detail_service2
from app import get_config, Constants as C

_glatency1 = int(get_config('LAYTENCY_TIME/board_read_article'))
_gmin_value = get_config('COMMON/min_count_of_total_articles')
_gsel_month = int(get_config('COMMON/sel_month'))

class Board_service(TRA):
    def __init__(self):
        super().__init__('받은문서목록')
        self.context = Context()
        
    def _initialize(self):
        self._top = self.context.auto.PaneControl(searchDepth=1, Name=self.name("웹EDI"))
        self.home = self.context.auto.PaneControl(searchDepth=1, Name=self.name("국민건강보험 EDI"))
        self.detail_service = {C.Biz:Detail_service1(), C.Idz:Detail_service2()}
        self.bbs_title = set()

    def req(self):
        self._initialize()

        self.begin("개시")
        self.act(self._top,'activate')
        self.act(self._top.TextControl(searchDepth=23, Name="1"))
        self.checkAndRetry()
        
        #건강보험, 국민연금, 고용보험, 산재보험; depth=16,img_tab2~5
        self.act(self._top.TextControl(searchDepth=19,Name="전체"),'click')

        #임의의 행 6행이 인식되는지를 체크. 6행이 없는 회사인 경우엔 오류발생 가능성있음.
        self.act(self._top.TextControl(searchDepth=23, Name=_gmin_value))
        self.checkAndRetry()
        
        _depth = 15
        _name = "순번 받은일자 번호 서식명 구분 최종 받은 일자"
        _base = self._top.GroupControl(searchDepth=_depth, Name=_name)

        bbs = list()
        _dictinct_title = set()
        #증손자노드취득(첫째,첫번째,첫번째)
        row_C = self.take(_base.GetNextSiblingControl(),0,3) 
        while row_C:
            # _gsel_month:당월0,전월-1,...
            _month = date.today().month + _gsel_month
            
            _drst = self._traverse(row_C, _depth + 3)
            
            #동일게시물 제외
            _bbs_title = _drst['title']
            if _bbs_title not in _dictinct_title and self._checkmonth_type(_drst, _month):
                bbs.append(_drst)
                _dictinct_title.add(_bbs_title)

            row_C = row_C.GetNextSiblingControl()
        
        print("complete to load bbs")
        self._read_board(bbs)

    def _checkmonth_type(self, ddata, month): 
        _date = ddata['date']
        _title = ddata['title']
        get_month = lambda ym: int(ym[4:6])

        if not (_date!='' and get_month(_date) == month): return False

        _type = C.Biz if C.Biz in _title else C.Idz

        ddata['type'] = _type
        return True

    def _read_board(self, bbs):
        for idx, article in enumerate(bbs):
            # 임시코드: 마지막 1건만을 테스트
            # if idx < len(bbs)-1: continue
            self._top.SetActive()
            
             #_title = 순번 + title;공백치환
            _iorder = article['no']
            _title = "{0:2d}_".format(_iorder) + re.sub('[: ]','_',article['title'])

            self.context.set(title=_title)
            print('<파일명>{0}'.format(self.context.title))
                        
            # self._top.ImageControl(searchDepth=16,Name="img_search").Click()
            
            _depth = article['depth']
            _name = article['name']
            self.act(self._top.TextControl(searchDept=_depth,Name=_name),'dbclick')
            #Laytency Time
            self.wait(_glatency1)

            # 세부화면으로 화면전이
            _type = article['type']
            self.detail_service[_type].req()

    def _traverse(self, base_C, depth):
        # _sel_keyword = '사업장고지내역서'
        _date_keyword = "고지년월"
        _target = base_C.GetFirstChildControl().GetFirstChildControl()
        
        #_order:게시물순번
        _order = int(_target.GetChildren()[0].Name)
        text_C = _target.GetChildren()[3].GetFirstChildControl().GetFirstChildControl()
        
        #_board_title = 가입자고지내역서(건강) 고지년월: 202005 고지차수: 1 회계코드: 00
        _board_title = text_C.Name
        _idx = _board_title.index(_date_keyword) if _date_keyword in _board_title else -1 
       
        _date = _board_title[_idx+6:_idx+6+6] if _idx >=0 else ''
        
        # return {'name':base_C.Name,'no':_order,'title':_board_title,'date':_date,'depth':depth}
        return {'name':text_C.Name,'no':_order,'title':_board_title,'date':_date,'depth':depth+5}
