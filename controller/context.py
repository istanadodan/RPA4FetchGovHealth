import time

class Context(object):
    exit = 0
    def __new__(cls):
        if not hasattr(cls,'_instance'):
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self._instance,'_proc_tasks'):
            self.set(_proc_tasks = list())
    
    def clear_tasks(self):
        if self.get('tasks',[]):
            self._proc_tasks.append(self._instance.tasks[:])
        self._instance.tasks = list()

    def add_task(self,task):
        self.get('tasks',[]).append(task)

    def set(self,**kargs):
        for key, v in kargs.items():
            setattr(self._instance, key, v)
    #added
    def pop_tasks(self):
        self.set(tasks=self.get('_proc_tasks',[]))
        return self.get('tasks')

    def get(self,key,_default=None):
        if hasattr(self._instance, key):
            return getattr(self._instance, key)
        return _default
    
    def checkAndRetry(self,id, max_retry):
        for n in range(max_retry):
            print("<{0}>checknAndetry:{1:02d}".format(id,n+1))

            if self._retry():
                self.clear_tasks()
                return True

        return False

    def _retry(self):
        jobs = self.get('tasks',[False])[:]
        while jobs:
            job = jobs.pop(0)

            if not self._act(job):
                # 소화하지못한 태스크를 다시 집어 넣음.
                # self.set(tasks=jobs.insert(0,job))
                return False

            time.sleep(2)

        return True

    def _act(self, dtask):
        _cntl = dtask['control']
        if not _cntl.Exists(3,1): return False
        self.evhandler(_cntl, dtask['act'], **dtask['_'])

        _name = _cntl.Name if hasattr(_cntl,'Name') else 'None'
        print("<act2 complete> {0}".format(_name))
        return True

    def evhandler(self, component, action, **kargs):
        
        if action=='click':
            component.SetFocus()
            if kargs: component.Click(**kargs)
            else: component.Click()
        elif action=='dbclick':
            component.DoubleClick()
        elif action=='activate':
            component.SetActive()
        elif action=='sendkeys':
            component.SendKeys(**kargs)