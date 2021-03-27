from configparser import ConfigParser
import os

config = ConfigParser()
base_dir = os.path.dirname(__file__)
file_path = os.path.join(base_dir,'config.ini')
config.read(file_path, encoding='utf-8')

def get_config(path, index=0):
    section, item = path.split('/')
    if not section in config: return None
    if not item in config[section]: return None
    
    data = config[section][item]
    if not data: return None

    _split_comma = [v.strip() for v in data.split(',') if v]
    
    return _split_comma if index else \
           _split_comma[index]

_dn_path = get_config("COMMON/download_folder")
if not os.path.exists(_dn_path): os.mkdir(_dn_path)

class Constants:
    Biz = '사업장고지내역서'
    Idz = '개별고지내역서'
