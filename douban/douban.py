import re

import execjs
import requests
import xxhash
import base64
import plistlib
from plistlib import FMT_BINARY, _BinaryPlistParser, _undefined
import struct


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
_BinaryPlistParser._read_object = _read_object


class Encrypt(object):
    def o_encrypt(self, data):
        a = base64.b64decode(data)
        i = 16
        s = max((len(a) - 2 * i) // 3, 0)
        u = a[s: s + i]
        a = a[0: s] + a[s + i:]
        sec_key = xxhash.xxh64_hexdigest(u, 41405).encode("utf-8")
        print(sec_key)

        text = self.r_encrypt(a, sec_key)
        local_packet = bytearray()
        local_packet.append(text[0])
        for i in text[1:]:
            local_packet.extend(bytes([i]))
        # print(local_packet)

        data = plistlib.loads(local_packet, fmt=FMT_BINARY)
        return data

    def r_encrypt(self, e, sec_key):
        r = list(map(ord, sec_key.decode("utf-8")))
        print(r)
        s = 0
        o = list(range(256))
        i = 0
        while s < 256:
            i = (i + o[s] + r[s % len(r)]) % 256
            n = o[s]
            o[s] = o[i]
            o[i] = n
            s += 1

        # print(o[:10])
        s = 0
        i = 0
        a = list(range(len(e)))
        for u in range(len(e)):
            s = (s + 1) % 256
            i = (i + o[s]) % 256
            n = o[s]
            o[s] = o[i]
            o[i] = n
            a[u] = e[u] ^ o[(o[s] + o[i]) % 256]
        # print(a[:10])
        return a


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

    with open('bundle.js', 'r', encoding='gbk') as f:
        decrypt_js = f.read()
    ctx = execjs.compile(decrypt_js)
    data = ctx.call('decrypt', r)
    count = 0
    for item in data['payload']['items']:
        print(item)
        count += 1
        if count == 3:
            break
    print(count)
