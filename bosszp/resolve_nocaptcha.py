import asyncio

from retrying import retry
from pyppeteer.launcher import launch

js1 = '''() =>{
           Object.defineProperties(navigator,{
             webdriver:{
               get: () => false
             }
           })
        }'''
js2 = '''() => {
        alert (
            window.navigator.webdriver
        )
    }'''
js3 = '''() => {
        window.navigator.chrome = {
    runtime: {},
    // etc.
  };
    }'''
js4 = '''() =>{
Object.defineProperty(navigator, 'languages', {
      get: () => ['en-US', 'en']
    });
        }'''
js5 = '''() =>{
Object.defineProperty(navigator, 'plugins', {
    get: () => [1, 2, 3, 4, 5,6],
  });
        }'''


def retry_if_result_none(result):
    return result is None


@retry(retry_on_result=retry_if_result_none, )
async def mouse_slide(page=None, slider=None):
    await asyncio.sleep(3)
    try:
        box = await slider.boundingBox()
        await page.mouse.move(box['x'] + box['width'] / 2, box['y'] + box['height'] / 2)
        await page.mouse.down()
        await page.mouse.move(box['x'] + 335, box['y'])  # moveto(100, 200)coordinates
        await page.mouse.up()
        await asyncio.sleep(5)
    except Exception as e:
        print(e, ' : slide failed')
        return None
    else:
        slider_text = await page.xpath('//span[@data-nc-lang="_yesTEXT"]//text()')
        slider_text = await (await slider_text[0].getProperty('textContent')).jsonValue()
        if slider_text != '验证通过':
            return None
        else:
            print('验证通过')
            return True


async def page_close(browser):
    for _page in await browser.pages():
        await _page.close()
    await browser.close()


async def get_encrypt_params(page, path="register"):
    try:
        form = {}
        params = await page.xpath(f'//div[@class="sign-form sign-{path}"]//input[@type="hidden"]')
        if params:
            for param in params:
                name = await (await param.getProperty('name')).jsonValue()
                value = await (await param.getProperty('value')).jsonValue()
                form[name] = value
        return form
    except Exception as e:
        print('获取参数失败', e)
        return


async def pyppeteer_solve_captcha(url, path="register"):
    browser = await launch({'headless': False, 'dumpio': True, 'args': ['--no-sandbox', '--window-size=1366,768']},
                           userDataDir='./userdata')
    page = await browser.newPage()
    await page.setViewport(viewport={"width": 1366, "height": 768})
    await page.setUserAgent(
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko)'
        ' Chrome/73.0.3683.103 Safari/537.36'
    )
    await page.goto(url)
    await page.evaluate(js1)
    await page.evaluate(js3)
    await page.evaluate(js4)
    await page.evaluate(js5)

    await asyncio.sleep(3)
    # 判断是否有滑块
    form = ''
    slider = await page.xpath(f'//div[@class="sign-form sign-{path}"]//span[contains(@id, "n1z")]')
    if slider:
        flag = await mouse_slide(page=page, slider=slider[0])
        if flag:
            form = await get_encrypt_params(page=page, path=path)
        else:
            print("滑块模拟失败")
        await page_close(browser)
        return form
    else:
        print("未发现滑块")
    await page_close(browser)


if __name__ == '__main__':
    url = "https://signup.zhipin.com/?ka=header-register"
    loop = asyncio.get_event_loop()
    loop.run_until_complete(pyppeteer_solve_captcha(url))
