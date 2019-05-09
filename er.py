# coding: utf-8
import base64
import hashlib
import hmac
import json
import sys
from imp import reload

import requests

reload(sys)
from jpype import *


class Encrypt:
    def __init__(self):
        self.module = 3
        self.params = {
            # 'appKey': 'testapp',
            'appKey': 'VOC_SDK',
            'appSecret': '12345678',
            'dataKey': 'default'
        }
        # self.basicUrl = 'http://10.88.27.212:8356/secret/query'
        self.basicUrl = 'https://api-base-ecs.baozun.com/api/zkproxy/secret/query'
        self.secret_key = None
        self.get_secret_key()
        self.tmp_key = None

    def get_secret_key(self):
        re = requests.get(url=self.basicUrl, params=self.params)
        re_dict = json.loads(re.content)
        self.secret_key = str(re_dict['data'])

    def generate_index(self, content):
        b64_str = ''
        for character in content:
            # 使用hmacMD5进行离散映射
            b = bytes(self.secret_key, encoding="utf8")
            secret_char = bytearray(hmac.new(b, character.encode("utf8"), hashlib.md5).digest())
            # 分别压缩成3个字节
            compress_char = self.compress(secret_char)
            # 转成base64格式并拼接
            b64_char = base64.b64encode(compress_char)
            b64_str += str(b64_char, "utf8")
        return b64_str

    def compress(self, byte_array):
        output_array = bytearray([0, 0, 0])
        for i in range(len(byte_array)):
            index = i % self.module
            output_array[index] ^= byte_array[i]
        return output_array

    def trans_key(self, secret_key, content):
        startJVM("D:\\dev\\jdk1.8.0_191\\jre\\bin\\server\\jvm.dll", "-ea",
                 "-Djava.class.path=.\\",
                 "-Dfile.encoding=UTF-8")
        AES = JClass("AesUtils")
        a = AES()
        re = a.aesUtil(secret_key, content)
        # shutdownJVM()
        return re

    def aes_encrypt(self, content):
        print(self.secret_key)
        encrypt_content = self.trans_key(self.secret_key, content)
        return encrypt_content

    def generate_result(self, content):
        result = '~' + self.aes_encrypt(content) + '~' + self.generate_index(content) + '~'
        print(result)
        return result


if __name__ == '__main__':
    x = Encrypt()
    # print(x.trans_key('s6rUGgXEdnP8XvVV'))
    x.generate_result(u'#*it izzue男运动长裤2018春夏新品字母饰条6706S8A')