import asyncio
import requests
from bosszp.resolve_nocaptcha import pyppeteer_solve_nocaptcha

def send_sms(data):
    # 从打码平台获取电话号码，验证码
    url = 'https://signup.zhipin.com/wapi/zppassport/send/smsCode'
    res = requests.post(url=url, headers= headers, data=data)
    if res.json()['message'] == 'Success':
        print("Boss发送短信成功", res.json())
        phone_code = "打码平台获取或自己手动输入"
        # phone_code = input("输入验证码")
        if phone_code:
            print(f'Boss短信验证码接收成功: {phone_code}')
            data['phoneCode'] = phone_code
            return True
    # 验证码发送失败，需重新拖动滑块
    print("发送短信失败", res.json())
    return False


if __name__ == '__main__':
    headers = {
        'origin': 'https://www.zhipin.com',
        'pragma': 'no-cache',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10'
                      '_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
    }
    url = "https://signup.zhipin.com/?ka=header-register"

    data = dict()
    data['phone'] = "1810809****"  # 打码平台获取
    loop = asyncio.get_event_loop()
    form = loop.run_until_complete(pyppeteer_solve_nocaptcha(url))

    data.update(form)

    if send_sms(data):
        url = 'https://signup.zhipin.com/wapi/zppassport/user/registered'
        data['policy'] = 'on'
        data['rescode'] = '1'
        response = requests.post(url=url, headers=headers, data=data)
        print(f'Boss注册成功： {response.json()}')