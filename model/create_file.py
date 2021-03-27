import json, os
from .AESCipher import AESCipher
from app import get_config

_glogininfo = get_config('COMMON/logininfo')
_gcertificate = get_config('COMMON/certificate')
_gcertificate_sub = get_config('COMMON/certificate_sub')

def _merge():
    _lcompany = list()
    with open(_gcertificate,'r',encoding='utf-8') as f:
        while True:
            _record = f.readline()
            if not _record: break

            _a = _record.split(',')
            name, pkey = _a[0], _a[1].replace('\n','')
            
            _lcompany.append({'name':name,'passwd':pkey})

    _dmanager = dict()
    with open(_gcertificate_sub,'r',encoding='utf-8') as f:
        while True:
            _record = f.readline()
            if not _record: break

            _a = _record.split(',')
            name, id, pw, code = _a[0], _a[1], _a[2], _a[3].replace('\n','')

            if name not in _dmanager:
                _dmanager[name] = list()

            _dmanager[name].append((id,pw,code))

    result = list()
    for el in _lcompany:
        _name = el['name']
        _t = dict(name=_name, passwd=el['passwd'])

        if _name not in _dmanager: 
            result.append(_t)
            continue
        
        for mng in _dmanager[_name]:
            _r = _t.copy()
            _r.update( dict(subid=mng[0], subpw=mng[1], code=mng[2]) )
            result.append(_r)

    return result

def _get_aes(pkey, plan):
    encrypted = AESCipher(pkey).AES256Encrypt(plan)
    if not encrypted:
        raise Exception("인증키가 일치하지 않습니다.")
    
    return (encrypted["iv"] + encrypted["cipher"]).decode('latin-1')

def create_file(pkey):
    if not os.path.exists(_gcertificate): 
        raise Exception(_gcertificate, "파일이 존재하지 않습니다.")
    
    if not os.path.exists(_gcertificate_sub): 
        raise Exception(_gcertificate_sub,"파일이 존재하지 않습니다.")
    
    data = list()
    for el in _merge():
        _t = dict(name=el['name'])
        for key in ('passwd','subid','subpw','code'):
            if key not in el: continue
            _t.update({key:_get_aes(pkey, el[key])})
        
        data.append(_t)
    
    with open(_glogininfo,'w',encoding='utf-8') as fs:
        json.dump(data, fs)
    
    #텍스트파일삭제
    os.remove(_gcertificate)
    os.remove(_gcertificate_sub)


if __name__=='__main__':
    _pkey = 'etners2020!!!'
    create_file(_pkey)
    