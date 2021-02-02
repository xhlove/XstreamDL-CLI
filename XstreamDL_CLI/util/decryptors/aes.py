from Crypto.Cipher import AES


class CommonAES:
    '''
    这是一个常规的AES-128-CBC解密类
    '''

    def __init__(self, aes_key: bytes, aes_iv: bytes = None):
        self.aes_key = aes_key # type: bytes
        self.aes_iv = aes_iv # type: bytes
        if self.aes_iv is None:
            self.aes_iv = bytes([0] * 16)

    def decrypt(self, data: bytes) -> bytes:
        '''
        初始化解密器
        '''
        cipher = AES.new(self.aes_key, AES.MODE_CBC, iv=self.aes_iv)
        return cipher.decrypt(data)