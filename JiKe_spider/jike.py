from selenium import webdriver
from lxml import etree
import pandas as pd
import json
import time
import os
import random
import string
import requests
import matplotlib.pyplot as plt


class JiKe:
    def __init__(self, url):

        # chrome_opt = webdriver.ChromeOptions()
        # chrome_opt.add_argument("--proxy-server=http://171.92.21.43:9000")
        # self.browser = webdriver.Chrome(chrome_options=chrome_opt)
        self.browser = None
        self.url = url
        self.image_list = []

    def get_page(self, save_login_cookies=False, load_login_cookies=False, scroll=False):
        """
        save_login_cookies: 保存登录cookies
        load_login_cookies: 加载登录cookies
        scroll:控制页面滚动
        """
        self.browser = webdriver.Chrome()
        self.browser.get(self.url)
        if save_login_cookies:
            self.save_login_cookies()
        if load_login_cookies:
            self.load_login_cookies()
        if scroll:
            # 滑动至底部
            client_hg = scroll_top = 0
            scroll_hg = 1
            while round(scroll_top) + round(client_hg) < round(int(scroll_hg)):
                self.browser.execute_script("window.scrollTo(0,document.body.scrollHeight);")
                # 根据网络状态适当修改滑动加载时间
                time.sleep(6)
                js = 'let scroll_top = document.documentElement.scrollTop; return scroll_top;'
                scroll_top = self.browser.execute_script(js)
                js = 'let client_hg = document.documentElement.clientHeight; return client_hg;'
                client_hg = self.browser.execute_script(js)
                js = 'let scroll_hg = document.body.scrollHeight; return scroll_hg;'
                scroll_hg = self.browser.execute_script(js)
        page = self.browser.page_source
        return page

    def save_login_cookies(self):
        """
        保存登录cookies
        """
        cookies = self.browser.get_cookies()
        with open('./cookies.json', 'w') as f:
            f.write(json.dumps(cookies))
        return True

    def load_login_cookies(self):
        """
        读取本地cookies文件加载cookies模拟登录
        """
        with open('./cookies.json', 'r')as f:
            cookies = json.loads(f.read())

        for cookie in cookies:
            self.browser.add_cookie({
                'domain': cookie['domain'],
                'name': cookie['name'],
                'value': cookie['value'],
                'path': cookie['path']
            })
        self.browser.get(self.url)
        return True

    def get_items(self, page):
        """
        xpath 和 JavaScript获取数据，清洗返回item
        """
        page_etree = etree.HTML(page)
        content_list = page_etree.xpath('//div[@class="flex flex-col flex-auto pt-2 w-full animate-show min-w-0"]')
        items = []
        for index, content in enumerate(content_list):
            user = content.xpath('.//a[@class="sc-bdnxRM fEvjQr"]/text()')[0]
            create_time = content.xpath('.//time/@datetime')
            text = content.xpath(
                './/div[contains(@class,"break-words content_truncate__1z0HR")]/text()')
            href = content.xpath('.//a[@class="text-primary no-underline"]/@href')
            like = content.xpath('.//span[@class="Like___StyledSpan-sc-8xi69i-1 gURQoB"]/text()')
            area = content.xpath(
                './/a[@class="sc-bdnxRM cYiXfS MessageFooter__TopicContainer-sc-3lstkp-0 dYbgtz"]/text()')
            # video_src = content.xpath('.//video/@src')
            img_pattern = './/div[@class="sc-bdnxRM fzUdiI"]'
            image_url_list = []
            if content.xpath(img_pattern):
                img_src = content.xpath(img_pattern + '//img/@src')
                if img_src:
                    image_url_list.append(img_src[0])
                    self.image_list.append(img_src[0])
                else:
                    """
                    JavaScript 
                    """
                    js = """
                        let src_list = [];
                        let temp_div = document.querySelectorAll("div.flex.flex-col.flex-auto.pt-2.w-full.animate-show.min-w-0")[(%s)];
                        let image_list = temp_div.getElementsByClassName("sc-bdnxRM MessagePictureGrid__Cell-sc-pal5rf-3");
                        for(let image of image_list){
                            let bg_image = window.getComputedStyle(image).backgroundImage;
                            src_list.push(bg_image);
                        }
                        return src_list;
                    """ % (index,)
                    images = self.browser.execute_script(js)
                    for image in images:
                        img_src = image.lstrip('url("').rstrip('")')
                        image_url_list.append(img_src)
                        self.image_list.append(img_src)

            item = {'user': user,
                    'create_time': create_time[0] if create_time else '',
                    'text': text[0] if text else '',
                    'image_urls': image_url_list if image_url_list else '',
                    'href': href if href else '',
                    'like': int(like[0]) if like else 0,
                    'area': area[0] if area else ''}
            items.append(item)
        return items

    def save_items(self, items):
        """
        保存为csv or excel文件
        """
        try:

            data_Frame = pd.DataFrame(items)
            # data_Frame.to_csv('./jike_user.csv', index=False, sep=';')
            data_Frame.to_excel('./hhpt.xlsx')
            return True
        except Exception as e:
            print(e)
            return False

    def analyse_items(self, data_path, compare_data_path=None):
        """
        分析item
        """
        data = pd.read_excel(data_path)
        # print(data.head())
        create_time_arr = data['create_time'].to_numpy()
        like_arr = data['like'].to_numpy()
        if compare_data_path:
            compare_data = pd.read_excel(compare_data_path)
            c_create_time_arr = compare_data['create_time'].to_numpy()
            c_like_arr = compare_data['like'].to_numpy()
            plt.plot(c_create_time_arr, c_like_arr, color='green', linestyle='-.', label=compare_data.iloc[0]['user'])
        plt.plot(create_time_arr, like_arr, color='red', linestyle='--', label=data.iloc[0]['user'])
        plt.xticks(rotation=270)
        plt.title('date_like')
        plt.xlabel('date')
        plt.ylabel('like')
        plt.legend(loc='upper left')
        # plt.rcParams['figure.figsize'] = (4, 3)
        # 设置中文字体显示
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False
        plt.show()
        pass

    def download_images(self, path='./images'):
        if not os.path.exists(path):
            os.mkdir(path)
        for image in self.image_list:
            resp = requests.get(image)
            if resp.status_code == 200:
                file = ''.join(random.sample(string.ascii_letters + string.digits, 8))
                path = '{path}/{file}.jpg'.format(file=file, path=path)

                with open(path, 'wb') as f:
                    f.write(resp.content)


if __name__ == '__main__':
    # jike = JiKe('https://web.okjike.com/topic/5b7d2e3aaa31960017c5a206/hot')
    jike = JiKe('https://web.okjike.com/u/051A9E99-6CB8-4283-AD24-79EE8265D17B')
    # page = jike.get_page(load_login_cookies=False, save_login_cookies=False, scroll=True)
    # jike.get_login_cookies()
    # items = jike.get_items(page)
    # jike.save_items(items)
    # jike.download_images()
    path = './hhpt.xlsx'
    compare_path = './xxj.xlsx'
    jike.analyse_items(path, compare_path)
