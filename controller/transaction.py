from abc import ABCMeta, abstractmethod
import uiautomation as auto
import time
from app import get_config
from .context import Context

RETRY_MAX = int(get_config('COMMON/retry_max',0))
_gchrome_name_prefix = get_config('WEB_BROWSER/chrome_name_prefix',0)

class TRA(metaclass=ABCMeta):
    def __init__(self, id):
        self.id = id
        self.context = Context()
        self.__initialize()

    def __initialize(self):
        self.cur=''
        self.cr_flag=False
        self.err = False
        self.tr_flag = False

    @abstractmethod
    def req(self): pass

    def begin(self, title):
        print("[{0}]<{1}>".format(self.id,title))

    #c:control, h:n-th, v:depth, _a:action
    def take(self,c,h=0,v=0,_a=None,**kargs):
        #index from 1
        _t = c.GetChildren()[h-1] if h > 0 else c
        n=0
        while v > 0 and n <= v-1:
            _t = _t.GetFirstChildControl()
            n += 1

        if _a:
            self.act(_t, _a, **kargs)
        return _t   

    def doRetry(self):
        
        self.tr_flag = False

        if not self.context.checkAndRetry(self.id,RETRY_MAX):
            print("checkAndretry Fails")
            raise Exception("checkAndRetry {}-times Fails".format(RETRY_MAX))

    def checkAndRetry(self):
        # 익셉션발생되어 스트링이 들어가는 경우대비.
        if isinstance(self.cur, str) or self.cur.Exists(1,1):
            self.context.clear_tasks()
            return

        self.doRetry()

    def act(self, c, action=None, **kargs):

        if self.context.exit!=0:
            #사용자중지
            raise Exception('STOP')
        
        try:
            self.context.add_task({'control':c,'act':action,'_':kargs})
            self.cur = c

            if self.tr_flag: return c

            if not c.Exists(5,1): 
                print("act fail:",c.Name)
                self.tr_flag=True
                return c

            self.context.evhandler( c, action, **kargs)
            self.wait(0.5)
            print("<act complete> {0}".format(c.Name))
            return c

        except Exception as e:
            print("<act:Exception>{0}".format(e))

    def name(self,name):
        return name + ' '+_gchrome_name_prefix

    def wait(self,sec):
        time.sleep(sec)