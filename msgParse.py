#!/usr/bin/python
# -*- coding: UTF-8 -*-
import base64
import hashlib
import json
import os
import tkinter as tk

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

window=tk.Tk()
window.title('bz rmq 解析')
window.geometry('1098x650')
# window.resizable(width = False, height = False)
window.iconbitmap('./ooopic_1535094442.ico')
a = tk.Label(window,text='输入topic: ')
a.place(x=18,y=10,anchor='nw')

e = tk.StringVar()
b = tk.Entry(window, width=30, textvariable=e, font = ('Calibri', '11'))
b.place(x=100,y=10,anchor='nw')

c = tk.Label(window,text='输入密文: ')
c.place(x=20,y=45,anchor='nw')

d = tk.Text(window, height=40,width=30)
d.place(x=100,y=45,anchor='nw')

e = tk.Label(window,text='明文: ').place(x=390,y=45,anchor='nw')

f = tk.Text(window,height=40)
f.place(x=450,y=45,anchor='nw')


def aes_ecb_encrypt(message, key):
    '''
    use AES CBC to encrypt message, using key and init vector
    :param message: the message to encrypt
    :param key: the secret
    :return: bytes init_vector + encrypted_content
    '''
    iv_len = 0
    assert type(message) in (str,bytes)
    assert type(key) in (str,bytes)
    if type(message) == str:
        message = bytes(message, 'utf-8')
    if type(key) == str:
        key = bytes(key, 'utf-8')
    backend = default_backend()
    iv = os.urandom(iv_len)
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=backend)
    encryptor = cipher.encryptor()
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(message) + padder.finalize()
    enc_content = encryptor.update(padded_data) + encryptor.finalize()
    return iv + enc_content

def aes_ecb_decrypt(content, key):
    '''
    use AES CBC to decrypt message, using key
    :param content: the encrypted content using the above protocol
    :param key: the secret
    :return: decrypted bytes
    '''
    assert type(content) == bytes
    assert type(key) in (bytes, str)
    if type(key) == str:
        key = bytes(key, 'utf-8')
    iv_len = 0
    assert len(content) >= (iv_len + 16)
    iv = content[:iv_len]
    enc_content = content[iv_len:]
    backend = default_backend()
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=backend)
    unpadder = padding.PKCS7(128).unpadder()
    decryptor = cipher.decryptor()
    dec_content = decryptor.update(enc_content) + decryptor.finalize()
    real_content = unpadder.update(dec_content) + unpadder.finalize()
    return real_content

def parse():
    key = b.get()
    hexdigest_ = hashlib.md5(key.encode('utf-8')).hexdigest()[8:-8]
    print(hexdigest_)
    context = d.get("0.0", "end")
    decode = base64.b64decode(context)
    rs = aes_ecb_decrypt(decode, hexdigest_)
    rs_decode = rs.decode('utf-8')
    print(rs_decode)
    loads = json.loads(rs_decode)
    msgBody = loads['msgBody']
    if msgBody.strip() == '':
        print('msg body is null')
    else:
        try:
            decdsdsode = base64.b64decode(msgBody)
        except  Exception:
            print("msg body 非密文")
        else:
            print("msg body 密文")
            decryptss = aes_ecb_decrypt(decdsdsode, hashlib.md5(loads['msgType'].encode('utf-8')).hexdigest()[8:-8])
            json_loadsss = json.loads(decryptss.decode('utf-8'))
            loads['msgBody'] = json_loadsss

    f.delete(1.0, tk.END)
    dumpsss = json.dumps(loads, sort_keys = True, indent = 2, separators = (',', ': '))

    f.insert(tk.END, dumpsss)

a1 = tk.Button(None,text='解密', width=15, height=1, command=parse).place(x=390, y=7, anchor='nw')

tk.mainloop()