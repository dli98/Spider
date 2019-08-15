import requests
import execjs
import re
import xxhash
import base64
import plistlib

params = {
    "search_text": "python",
    "cat": "1001"
}

# url = 'https://book.douban.com/subject_search?'
# response = requests.get(url, params=params)
# print(response.text)
# plistlib.loads(response.content)


# r = re.search('window.__DATA__ = "([^"]+)"', response.text).group(1)  # 加密的数据


#
# # 导入js
# with open('bundle.js', 'r', encoding='gbk') as f:
#     decrypt_js = f.read()
# ctx = execjs.compile(decrypt_js)
# data = ctx.call('decrypt', r)
# print(data)
# for item in data['payload']['items']:
#     print(item)
#     break

class Encrypt(object):
    def __init__(self):
        pass

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

        w = text[-32:]
        print(w)
        _ = w[6]
        E = w[7]
        self.E = E
        print(_, E)

        A = self.s(w, 8, 4)
        C = self.s(w, 16, 4)
        S = self.s(w, 24, 4)
        print(A, C, S)

        x = []
        for o in range(A):
            t = text[S + o * _: S + (o + 1) * _]
            x.append(self.i(t, 0))

        print(x)
        # self.export(text, x, C)

    def get_key(self, u, t=41405):
        a00 = 65535 & t
        a16 = t >> 16
        a32 = 0
        a48 = 0

    def export(self, t, x, e):
        r = x[e]
        n = t[r]
        o = (240 & n) >> 4
        i = 15 & n
        a = {
            "offset": r,
            "type": n,
            "objType": o,
            "objInfo": i,
            "tableOffset": e
        }
        if o == 10:
            return self.v(t, a)

    def v(self, t, n):
        o = n["offset"]
        a = n["objInfo"]
        s = a
        u = 1
        if (15 == a):
            c = t[o + 1]
            f = (240 & c) / 16
            l = 15 & c
            h = 2 ** l
            u = 2 + h
            s = self.i(t[o + 2:o + 2 + h])
        print(s)
        p = []
        for d in range(s):
            m = self.i(t[o + u + d * E:o + u + (d + 1) * self.E])
            p[d] = self.export(t, m)
        # }
        return p

    def i(self, t, e=None):
        e = e or 0
        r = 0
        for n in range(e, len(t)):
            r <<= 8
            r |= 255 & t[n]
        return r

    def s(self, text, t, e):
        w = text[t: t + 8]
        return int.from_bytes(w, "big")

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
    encrypt = Encrypt()


    r = "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"

    encrypt.o_encrypt(r)
    # import plistlib
    # plistlib.loads(r)
    # a = base64.b64decode(r)
    # with open("test.plist", "r") as f:
    #     plistlib.load(f)
