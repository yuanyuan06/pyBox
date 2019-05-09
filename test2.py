# coding: utf-8
import requests
import json
import hmac
import base64
import hashlib
import sys
sys.setdefaultencoding('utf-8')

class Encrypt:
    def __init__(self):
        self.module = 3
        self.params = {
            'appKey': 'testapp',
            'appSecret': '12345678',
            'dataKey': 'default'
        }
        self.basicUrl = 'http://10.88.27.212:8356/secret/query'
        self.secret_key = None
        self.padding = '\0'
        self.get_secret_key()

    def get_secret_key(self):
        # self.secret_key = 'tSVtrTnIGgfP75Nq'
        re = requests.get(url=self.basicUrl, params=self.params)
        re_dict = json.loads(re.content)
        self.secret_key = str(re_dict['data'])

    def generate_index(self, content):
        b64_str = ''
        for character in content:
            # 使用hmacMD5进行离散映射
            secret_char = bytearray(hmac.new(self.secret_key, character, hashlib.md5).hexdigest())
            # 分别压缩成3个字节
            compress_char = self.compress(secret_char)
            # 转成base64格式并拼接
            b64_char = base64.b64encode(compress_char)
            b64_str += b64_char
        return b64_str

    def compress(self, byte_array):
        output_array = bytearray([0, 0, 0])
        for i in range(len(byte_array)):
            index = i % self.module
            output_array[index] ^= byte_array[i]
        return output_array

    def aes_encrypt(self, content):
        content = content + (16 - len(content) % 16) * self.padding
        # aes = AES.new(secret_key, AES.MODE_CBC, Random.new().read(AES.block_size))
        aes = AES.new(self.secret_key, AES.MODE_CBC, '0102030405060708')
        encrypt_content = aes.encrypt(content)
        return base64.b64encode(encrypt_content)

    def generate_result(self, content):
        result = '~' + self.aes_encrypt(content) + '~' + self.generate_index(content) + '~'
        print(result)
        return result


if __name__ == '__main__':
    x = Encrypt()
    x.generate_result('testuser11225')