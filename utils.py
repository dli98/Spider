import hashlib
import time
import base64

# https://zh.wikipedia.org/wiki/RC4

def rc4(string, sec_key):
    string_length = len(string)
    result = ''
    box = list(range(256))
    randkey = []

    key_length = len(sec_key)

    if isinstance(sec_key, bytes):
        sec_key = sec_key.decode("utf-8")

    if isinstance(string, bytes):
        string = string.decode("utf-8")

    sec_key = list(map(ord, sec_key))

    # Init sbox
    for i in range(256):
        randkey.append(sec_key[i % key_length])

    # Key setup
    for i in range(256):
        j = 0
        j = (j + box[i] + randkey[i]) % 256
        box[i], box[j] = box[j], box[i] # swap

    S = range(256)
    # Pseudo-random generation algorithm
    # 此算法保证每256次循环中S盒的每个元素至少被交换过一次。
    for i in range(string_length):
        a = j = 0
        a = (a + 1) % 256
        j = (j + box[a]) % 256

        box[a], box[j] = box[j], box[a]  # swap
        # 以上再次进行了打乱
        # 真正的明文string逐字节与box中的随机值异或生成加密的result
        # 不管怎么随机打乱，由于cryptkey以及string_length总是一样的，因此box最终也一样
        # 解密时，密文在与box异或则返回明文

        result += chr(ord(string[i]) ^ (box[(box[a] + box[j]) % 256]))
    return result

if __name__ == '__main__':
    resutlt = rc4(b"abcdefg", b'9538347986e59ae0')
    print(resutlt)

    resutlt = rc4(resutlt, '9538347986e59ae0')
    print(resutlt)

