import json
import requests
from binascii import b2a_hex
from Crypto.Cipher import DES
from Crypto.Util.Padding import pad
from requests.utils import dict_from_cookiejar


def get_key_iv_phpsessid():
    _url = "http://passport.ziroom.com/account/des/index.html"
    r = requests.get(_url)
    cookie = dict_from_cookiejar(r.cookies)
    if r.json()["status"] == "success":
        data = r.json()["data"]
        return data["secret_key"], data["secret_iv"], cookie["PHPSESSID"]
    return "", "", ""


def get_encrypt_data(phone, pwd, key, iv):
    data = {
        "phone": phone,
        "password": pwd,
        "seven": 1
    }
    data = json.dumps(data, separators=(',', ':'))
    cryptor = DES.new(key.encode("utf8"), DES.MODE_CBC, iv.encode("utf8"))
    pad_pkc7 = pad(data.encode("utf8"), DES.block_size, "pkcs7")
    data = cryptor.encrypt(pad_pkc7)
    data = b2a_hex(data).decode("utf8")
    return {"data": data}


def login():
    phone = "********"
    pwd = "****"
    key, iv, php_sess_id = get_key_iv_phpsessid()
    if not key:
        return

    data = get_encrypt_data(phone, pwd, key, iv)
    print(data)
    _url = "http://passport.ziroom.com/account/login/login.html"
    headers = {
        'Host': 'passport.ziroom.com ',
        'Accept': 'application/json, text/plain, */*',
        'Origin': 'http://www.ziroom.com',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
        'Referer': 'http://www.ziroom.com/',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    cookies = {
        'PHPSESSID': php_sess_id,
    }
    r = requests.post(_url, data, headers=headers, cookies=cookies)
    print(r.json())


if __name__ == '__main__':
    login()
