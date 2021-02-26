import requests
import re
from bs4 import BeautifulSoup
from fontTools.ttLib import TTFont


class crawl():
    def __init__(self):
        self.sess = requests.session()

    def get_html(self, url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36'
        }
        try:
            r = self.sess.get(url, headers=headers)
            if r.status_code == 200:
                return r.content
        except Exception as e:
            print('抓取失败', e)
            return None

    # 解析字体，
    def decode_font(self, font_parse_name):
        # 设置编码和文字的关系
        font_dict = [u'五', u'四', u'短', u'十',
                     u'坏', u'近', u'大', u'九', u'小',
                     u'矮', u'上', u'一', u'六', u'的',
                     u'呢', u'长', u'少', u'下', u'地',
                     u'右', u'好', u'更', u'远', u'二',
                     u'和', u'低', u'七', u'很', u'着',
                     u'高', u'了', u'是', u'得', u'不',
                     u'左', u'八', u'三', u'多']

        font_base = TTFont('font_base.ttf')
        # font_base.saveXML('font_base.xml')
        font_base_order = font_base.getGlyphOrder()[1:]  # 原始font_base 编码

        font_parse = TTFont(font_parse_name)
        font_parse.saveXML('font_parse_2.xml')  # 调试用
        font_parse_order = font_parse.getGlyphOrder()[1:]  #

        f_base_flag = []
        for i in font_base_order:
            flags = font_base['glyf'][i].flags  # 获取0、1值
            f_base_flag.append(list(flags))

        f_flag = []
        for i in font_parse_order:
            flags = font_parse['glyf'][i].flags
            f_flag.append(list(flags))

        result_dict = {}
        for a, i in enumerate(f_base_flag):
            for b, j in enumerate(f_flag):
                if self.comp(i, j):
                    key = font_parse_order[b].replace('uni', '')
                    print(key)
                    key = eval(r'u"\u' + str(key) + '"').lower()
                    result_dict[key] = font_dict[a]
        return result_dict

    def comp(self, L1, L2):

        if len(L1) != len(L2):
            return 0
        for i in range(len(L2)):
            if L1[i] == L2[i]:
                pass
            else:
                return 0
        return 1

    # 解析网页
    def parse_html(self, html):
        soup = BeautifulSoup(html, 'lxml')

        font_url = soup.find('style', attrs={'type': 'text/css'}).text
        # font_url = 'https:' + re.search('format\("woff"\),url\("(.*?)"\)', font_url, re.S).group(1)
        font_url = 'https:' + re.search(",url\('(//.*.ttf)'\) format\('woff'\)", font_url, re.S).group(1)

        new_font_name = "font_new.ttf"

        font_data = self.get_html(font_url)
        with open(new_font_name, 'wb') as f:  # 获得字体文件
            f.write(font_data)

        map_data = self.decode_font(new_font_name)  # 得到字体映射
        print(map_data)
        conttxt = soup.find(class_='conttxt').text
        # 去掉html标签
        text_data = re.sub(r'<.*?>', '', conttxt).strip()

        if text_data:
            for j in map_data.keys():
                text_data = text_data.replace(j, map_data[j])
            print('name actual', text_data)


if __name__ == "__main__":
    url = 'https://club.autohome.com.cn/bbs/thread/5825c062dc84c6da/18454758-1.html'
    spider = crawl()
    html = spider.get_html(url)
    spider.parse_html(html)
