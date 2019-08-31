from requests.utils import dict_from_cookiejar

from bosszp.resolve_nocaptcha import pyppeteer_solve_nocaptcha
import asyncio
import requests


def success(data):
    login_url = 'https://login.zhipin.com/wapi/zppassport/login/account'
    response = requests.post(login_url, data=data)
    if response.json()['message'] == 'Success':
        print('用户登录成功')
        cookies = dict_from_cookiejar(response.cookies)
        print(f'成功获取到Cookies: {cookies}')
        return cookies
    print(f'用户登录失败：{response.json()}')

if __name__ == '__main__':
    username = "1312513****"
    password = "****"
    url = "https://login.zhipin.com/?ka=header-login"
    loop = asyncio.get_event_loop()
    data = loop.run_until_complete(pyppeteer_solve_nocaptcha(url, path='pwd'))
    data['account'] = username
    data['password'] = password
    result = success(data)
