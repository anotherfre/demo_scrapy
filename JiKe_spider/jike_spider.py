from selenium import webdriver
from lxml import etree
import pandas as pd
import json
import time
import openpyxl


class JiKe:
    def __init__(self, url):

        # chrome_opt = webdriver.ChromeOptions()
        # chrome_opt.add_argument("--proxy-server=http://171.92.21.43:9000")
        # self.browser = webdriver.Chrome(chrome_options=chrome_opt)
        self.browser = webdriver.Chrome()
        self.url = url

    def get_page(self, save_login_cookies=True, load_login_cookies=True, scroll=True):
        """
        save_login_cookies: 保存登录cookies
        load_login_cookies: 加载登录cookies
        scroll:控制页面滚动
        """
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
            create_time = content.xpath('.//time/@datetime')[0]
            text = content.xpath(
                './/div[contains(@class,"break-words content_truncate__1z0HR")]/text()')
            href = content.xpath('.//a[@class="text-primary no-underline"]/@href')
            # video_src = content.xpath('.//video/@src')
            img_pattern = './/div[@class="sc-bdnxRM fzUdiI"]'
            image_url_list = []
            if content.xpath(img_pattern):
                img_src = content.xpath(img_pattern + '//img/@src')
                if img_src:
                    image_url_list.append(img_src)
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
            text_str = " ".join(text)
            item = {'user': user, 'create_time': create_time, 'text': text_str}
            items.append(item)
            for t in items:
                print(t)
        return items

    def save_items(self, items):
        """
        保存为csv or excel文件
        """
        try:

            unsorted_data_Frame = pd.DataFrame(items)
            sorted_data_Frame = unsorted_data_Frame.sort_values(by='create_time', ascending=True)
            # data_Frame.to_csv('./jike_user.csv', index=False, sep=';')
            sorted_data_Frame.to_excel('./jike_user4.xlsx', sheet_name='Sheet1')
            sorted_data_Frame.to_csv('./jike_xiaoxiami2.txt', sep='\t', index=False, line_terminator='\n\n')
            return True
        except Exception as e:
            print(e)
            return False

    def analyse_items(self, items):
        pass


if __name__ == '__main__':
    jike = JiKe('https://web.okjike.com/u/2FF63D38-82E0-49FB-B773-3872C9FD40CC')

    page = jike.get_page(load_login_cookies=True, save_login_cookies=False, scroll=True)
    # jike.get_login_cookies()
    items = jike.get_items(page)
    jike.save_login_cookies()
    jike.save_items(items)
    # items = pd.read_csv('./jike_user.csv', sep=';')
    # jike.analyse_items(items)
    # for item in items:
    #     for key, value in item.items():
    #         print(key, value)
    #     print("\n")
