var window = {};
!function() {
    function a(a) {
    //  a方法是产生16位随机string
        var d, e, b = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", c = "";
        for (d = 0; a > d; d += 1)
            e = Math.random() * b.length, //返回 0 ~ 1 之间的随机数。

            e = Math.floor(e), //对数进行下舍入。
            c += b.charAt(e);
//            注释：字符串中第一个字符的下标是 0。如果参数 index 不在 0 与 string.length 之间，该方法将返回一个空字符串。
        return c
    }
    function b(a, b) {
        var c = CryptoJS.enc.Utf8.parse(b) // 加密秘钥
          , d = CryptoJS.enc.Utf8.parse("0102030405060708")  //  矢量
          , e = CryptoJS.enc.Utf8.parse(a) //需要加密的数据
          , f = CryptoJS.AES.encrypt(e, c, { //  AES加密
            iv: d,
            mode: CryptoJS.mode.CBC
            //mode开头的是模式，pad开头的是补码方式。
        });
        return f.toString()
    }
    function c(a, b, c) {
        // c方法是进行 RSA加
        var d, e;
        return setMaxDigits(131),  //130 1024  n的十六进制位数/2+3   268 266
        //第一个参数为加密指数、第二个参数为解密参数、第三个参数为加密系数模数
        d = new RSAKeyPair(b,"",c),
        e = encryptedString(d, a)
    }
    function d(d, e, f, g) {
        var h = {}
          , i = a(16);
        return h.encText = b(d, g),
        h.encText = b(h.encText, i),
        h.encSecKey = c(i, e, f),
        h
    }
    function e(a, b, d, e) {
        var f = {};
        return f.encText = c(a + e, b, d),
        f
    }
    window.asrsea = d,
}();

//JSON.stringify() 方法是将一个JavaScript值(对象或者数组)转换为一个 JSON字符串，
//如果指定了replacer是一个函数，则可以替换值，或者如果指定了replacer是一个数组，可选的仅包括指定的属性。

//function get_params(){
//    var modulus = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7';
////    var i7b = {ids: "[557581476]", br: 128000, csrf_token: ""};
////    var bUS9J = window.asrsea(JSON.stringify(i7b), '010001', modulus, "0CoJUm6Qyw8W8jud");
//
//    return {params: bUS9J.encText,
//    ncSecKey: bUS9J.encSecKey}
//};
