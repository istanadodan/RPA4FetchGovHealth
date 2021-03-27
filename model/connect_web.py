import json
import uiautomation as auto
import subprocess as ps
from app import get_config
from .AESCipher import AESCipher
import time

_gchrome_path = get_config('WEB_BROWSER/chrome')
_gchrome_keyword = get_config('WEB_BROWSER/chrome_search_keyword')
_gchrome_name_prefix = get_config('WEB_BROWSER/chrome_name_prefix')
_gcertificate = get_config('COMMON/logininfo')

class RPA:
    
    def __init__(self,**kargs):
        self.auto = auto
        self.site(**kargs)
        
    def site(self, **kargs):
        self.url = kargs['url']
        self.url_title = kargs['title']

    def close_page(self):
        top = self.auto.PaneControl(searchDepth=1, Name=self.name(self.url_title))

        _w = top.PaneControl(searchDepth=2, Name='Chrome')
        _close_b = _w.ButtonControl(searchDepth=2, Name='닫기')
        if _close_b.Exists(0,0):
            _close_b.Click()

    def open_page(self):
        _url = self.url

        top = self.auto.PaneControl(searchDepth=1, Name=self.name(self.url_title))
        if top.Exists(1,1):
            _logout = top.ImageControl(searchDepth=9,Name='로그아웃')
            if _logout.Exists(0,0):
                _logout.Click()
                time.sleep(0.5)
                top.SetActive()
                top.EditControl(searchDepth=7, Name="주소창 및 검색창").Click()
                top.EditControl(searchDepth=7, Name="주소창 및 검색창").SendKeys(_url+'{Enter}')
        else:
            if _gchrome_path:
                ps.Popen(_gchrome_path)
            else:
                self.auto.ButtonControl(searchDepth=3, Name='검색하려면 여기에 입력하십시오.').Click()
                self.auto.EditControl(searchDepth=3,Name='검색 상자').SendKeys(_gchrome_keyword)
                self.auto.TextControl(searchDepth=10, Name=_gchrome_keyword).Click()
            
            top = self.auto.PaneControl(searchDepth=1, Name=self.name('새 탭'))
            
            top.SetActive()
            top.EditControl(searchDepth=7, Name="주소창 및 검색창").SendKeys(_url+'{Enter}')
            

        #최대화
        _chrome_main_w = top.PaneControl(searchDepth=2, Name='Chrome')
        _max_b = _chrome_main_w.ButtonControl(searchDepth=2, Name='최대화')
        if _max_b.Exists(0,0):
            _max_b.Click()

        self.processId = str(top.ProcessId)
    
    def name(self,name):
        return name + ' '+_gchrome_name_prefix

    def load_task(self, private_key):
        results = list()
        with open(_gcertificate,'r',encoding='utf-8') as f:
            tasks = json.load(f)
            try:
                for task in tasks:
                    _d = dict({'name':task['name']})
                    for att in ('passwd','subid','subpw','code'):
                        if att not in task: continue

                        _value = task[att].encode('latin-1')
                        _iv, _cipher = _value[:16],_value[16:]
                        data = AESCipher(private_key).AES256Decrypt(_iv, _cipher)
                        if data==None: 
                            raise Exception("키가 일치하지 않습니다.")
                        
                        _d.update({att:data})
                    
                    results.append(_d)

            except Exception as e:
                results = None

        self.task_list = results

    def get_task_list(self):
        return self.task_list
    
    def check_password(self, key):
        self.load_task(key)
        return self.task_list != None