import glob,os
from controller import Cntl
from model import RPA
from view import View
from app import get_config

_gurl = get_config('SITE/url')
_gsite_name = get_config('SITE/name')
_gdown = get_config('COMMON/download_folder')

if __name__== '__main__':

    view = View()
    model = RPA(url=_gurl, title=_gsite_name)
    cntl = Cntl()
    
    view.handler(cntl)
    view.model(model)
    cntl.model(model) 

    view.mainloop()