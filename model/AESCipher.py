import hashlib
import Crypto
import Crypto.Random
from Crypto.Cipher import AES

class AESCipher:
    def __init__(self, key):
        self.key = key.encode('utf-8')

    def gen_sha256_hashed_key_salt(self):
        salt1 = hashlib.sha256(self.key).digest()
        return hashlib.sha256(salt1+self.key).digest()

    def gen_random_iv(self):
        return Crypto.Random.new().read(AES.block_size)

    def AES256Decrypt(self,iv,cipher):
        try:
            encryptor = AES.new(self.gen_sha256_hashed_key_salt(), AES.MODE_CBC, IV=iv)
            plain = encryptor.decrypt(cipher).decode('utf-8')
            plain = plain[0:-ord(plain[-1])]

            return plain
        except UnicodeDecodeError as e:
            return None

    def AES256Encrypt(self,plain):
        length = AES.block_size - (len(plain) % AES.block_size)
        plain += chr(length)*length
        iv = self.gen_random_iv()
        
        encryptor = AES.new(self.gen_sha256_hashed_key_salt(), AES.MODE_CBC, IV=iv)
        return {'cipher': encryptor.encrypt(plain.encode('utf-8')), 'iv': iv}