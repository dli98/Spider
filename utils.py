import hashlib
import time
import base64


# http://ju.outofmemory.cn/entry/46753
# https://www.cnblogs.com/darkpig/p/5849161.html
# https://zh.wikipedia.org/wiki/RC4

class RC4:
    def __init__(self, public_key=None, ckey_lenth=16):
        self.ckey_lenth = ckey_lenth
        self.public_key = public_key or 'none_public_key'
        key = hashlib.md5(self.public_key).hexdigest().encode("utf-8")  # 将密码public_key进行md5，返回32字节的key
        self.keya = hashlib.md5(key[0:16]).hexdigest()  # 将Key的前16字节md5，返回32字节的keya
        self.keyb = hashlib.md5(key[16:32]).hexdigest()  # 将key的后16字节md5，返回32字节的keyb
        self.keyc = ''

    def encode(self, string):
        # 当加密时，keyc取time.time()的md5前4字节，用作IV
        self.keyc = hashlib.md5(str(time.time()).encode("utf-8")).hexdigest()[32 - self.ckey_lenth:32]
        string = '0000000000' + hashlib.md5((string + self.keyb).encode("utf-8")).hexdigest()[0:16] + string
        self.result = b''
        self.docrypt(string)
        return self.keyc + base64.b64encode(self.result)

    def decode(self, string):
        # 当解密时，从密文的前4字节取出IV
        self.keyc = string[0:self.ckey_lenth]
        string = base64.b64decode(string[self.ckey_lenth:])
        self.result = ''
        self.docrypt(string)
        result = self.result
        if (result[0:10] == '0000000000'
            # 前十字节是0，再16字节是明文string与keyb的md5前16字节，最后的则是string
            or int(result[0:10]) - int(time.time()) > 0) \
                and result[10:26] == hashlib.md5(
                            result[26:] + self.keyb).hexdigest()[0:16]:
            return result[26:]
        else:
            return None

    def docrypt(self, string):
        string_lenth = len(string)
        result = ''
        box = list(range(256))
        randkey = []

        cryptkey = self.keya + hashlib.md5(self.keya + self.keyc).hexdigest()
        key_lenth = len(cryptkey)

        # Init sbox
        for i in range(255):
            randkey.append(ord(cryptkey[i % key_lenth]))

        # Key setup
        for i in range(255):
            j = 0
            j = (j + box[i] + randkey[i]) % 256
            tmp = box[i]
            box[i] = box[j]
            box[j] = tmp

        # Pseudo-random generation algorithm
        # 此算法保证每256次循环中S盒的每个元素至少被交换过一次。
        for i in range(string_lenth):
            a = j = 0
            a = (a + 1) % 256
            j = (j + box[a]) % 256
            tmp = box[a]
            box[a] = box[j]
            box[j] = tmp
            # 以上再次进行了打乱
            # 真正的明文string逐字节与box中的随机值异或生成加密的result
            # 不管怎么随机打乱，由于cryptkey以及string_length总是一样的，因此box最终也一样
            # 解密时，密文在与box异或则返回明文

            self.result += chr(ord(string[i]) ^ (box[(box[a] + box[j]) % 256]))


if __name__ == '__main__':
    rc = RC4('9538347986e59ae0'.encode("utf-8"))
    string = '我在这里呢，你在那里呢'
    print(string)
    str = rc.encode(string)
    print(str)
    str = rc.decode(str)
    print(str)
