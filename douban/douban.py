import requests
import execjs
import re
import hashlib
import base64

from binascii import a2b_hex

from Crypto.Cipher import AES

params = {
    "search_text": "python",
    "cat": "1001"
}


# url = 'https://book.douban.com/subject_search?'
# response = requests.get(url, params=params)
# print(response.text)
# r = re.search('window.__DATA__ = "([^"]+)"', response.text).group(1)  # 加密的数据
#
# # 导入js
# with open('main.js', 'r', encoding='gbk') as f:
#     decrypt_js = f.read()
# ctx = execjs.compile(decrypt_js)
# data = ctx.call('decrypt', r)
# for item in data['payload']['items']:
#     print(item)

class Encrypt(object):
    def __init__(self):
        pass

    def o_encrypt(self, data):
        a = base64.b64decode(data)
        print(r.__len__())
        print(a.__len__())
        i = 16
        s = max((len(a) - 2 * i) // 3, 0)
        u = a[s: s + i]
        print(u[0])
        a = a[0: s] + a[s + i:]
        sec_key = b"3e40b362a5662c48"
        self.aes_decrypt(a, sec_key)

    def key_encrypt(self):
        return "3e40b362a5662c48"

    def aes_decrypt(self, text, sec_key):
        cryptor = AES.new(sec_key, AES.MODE_CBC, sec_key)
        ciphertext = cryptor.decrypt(a2b_hex(text))
        return ciphertext


if __name__ == '__main__':
    encrypt = Encrypt()
    r = "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"
    encrypt.o_encrypt(r)
