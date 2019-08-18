import hashlib
import time
import base64


# https://zh.wikipedia.org/wiki/RC4

def rc4(string, sec_key):

    assert isinstance(sec_key, str), "sec_key 为字符串"

    string_length = len(string)
    result = ''
    box = list(range(256))
    randkey = []

    key_length = len(sec_key)

    sec_key = list(map(ord, sec_key))

    # Init sbox
    for i in range(256):
        randkey.append(sec_key[i % key_length])

    # Key setup
    j = 0
    for i in range(256):
        j = (j + box[i] + randkey[i]) % 256
        box[i], box[j] = box[j], box[i]  # swap

    S = range(256)
    # Pseudo-random generation algorithm
    # 此算法保证每256次循环中S盒的每个元素至少被交换过一次。
    result = []
    a = j = 0
    for i in range(string_length):
        a = (a + 1) % 256
        j = (j + box[a]) % 256

        box[a], box[j] = box[j], box[a]  # swap
        # 以上再次进行了打乱
        # 真正的明文string逐字节与box中的随机值异或生成加密的result
        # 不管怎么随机打乱，由于cryptkey以及string_length总是一样的，因此box最终也一样
        # 解密时，密文在与box异或则返回明文

        result.append(string[i] ^ (box[(box[a] + box[j]) % 256]))
    return bytearray(result)


if __name__ == '__main__':
    result = rc4(b"abcdefg", '9538347986e59ae0')
    print(result)

    result = rc4(result, '9538347986e59ae0')
    print(result)



