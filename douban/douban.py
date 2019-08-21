import re

import execjs
import requests
import xxhash
import base64
import plistlib
import struct

from plistlib import FMT_BINARY, _BinaryPlistParser, _undefined
from utils import rc4


def _read_object(self, ref):
    result = self._objects[ref]
    if result is not _undefined:
        return result

    offset = self._object_offsets[ref]
    self._fp.seek(offset)
    token = self._fp.read(1)[0]
    tokenH, tokenL = token & 0xF0, token & 0x0F

    if token == 0x00:
        result = None

    elif token == 0x08:
        result = False

    elif token == 0x09:
        result = True

    elif token == 0x0f:
        result = b''

    elif tokenH == 0x10:  # int
        result = int.from_bytes(self._fp.read(1 << tokenL),
                                'big', signed=tokenL >= 3)

    elif token == 0x22:  # real
        result = struct.unpack('>f', self._fp.read(4))[0]

    elif token == 0x23:  # real
        result = struct.unpack('>d', self._fp.read(8))[0]

    elif tokenH == 0x40:  # ascii string
        s = self._get_size(tokenL)
        result = self._fp.read(s).decode('ascii')
        result = result

    elif tokenH == 0x50:  # unicode string
        s = self._get_size(tokenL)
        result = self._fp.read(s * 2).decode('utf-16be')

    elif tokenH == 0xA0:  # array
        s = self._get_size(tokenL)
        obj_refs = self._read_refs(s)
        result = []
        self._objects[ref] = result
        result.extend(self._read_object(x) for x in obj_refs)

    elif tokenH == 0xD0:  # dict
        s = self._get_size(tokenL)
        key_refs = self._read_refs(s)
        obj_refs = self._read_refs(s)
        result = self._dict_type()
        self._objects[ref] = result
        for k, o in zip(key_refs, obj_refs):
            result[self._read_object(k)] = self._read_object(o)

    self._objects[ref] = result
    return result


# 利用猴子补丁，修改源代码的方法
# python 3.6.8。其它版本可能不行。自行修改补丁即可。
_BinaryPlistParser._read_object = _read_object


class Encrypt(object):
    def o_encrypt(self, data):
        a = base64.b64decode(data)
        i = 16
        s = max((len(a) - 2 * i) // 3, 0)
        u = a[s: s + i]
        a = a[0: s] + a[s + i:]
        sec_key = xxhash.xxh64_hexdigest(u, 41405)
        print(sec_key)

        text = rc4(a, sec_key)

        data = plistlib.loads(text, fmt=FMT_BINARY)
        return data


if __name__ == '__main__':
    params = {
        "search_text": "python",
        "cat": "1001"
    }

    url = 'https://book.douban.com/subject_search?'
    response = requests.get(url, params=params)
    r = re.search('window.__DATA__ = "([^"]+)"', response.text).group(1)  # 加密的数据

    encrypt = Encrypt()
    data = encrypt.o_encrypt(r)
    for i in data:
        if isinstance(i, dict):
            print(i)
