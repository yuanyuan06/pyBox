import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


class Aesutils:

    @staticmethod
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

    @staticmethod
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