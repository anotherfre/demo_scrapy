from selenium import webdriver
from lxml import etree
import pandas as pd


class JiKe:
    def __init__(self, url):
        self.browser = webdriver.Chrome()
        self.url = url

    def get_page(self):
        self.browser.get(self.url)
        page = self.browser.page_source
        return page

    def get_items(self, page):
        page_etree = etree.HTML(page)
        content_list = page_etree.xpath('//div[@class="flex flex-col flex-auto pt-2 w-full animate-show min-w-0"]')
        items = []
        for index, content in enumerate(content_list):
            user = content.xpath('.//a[@class="sc-bdnxRM fEvjQr"]/text()')[0]
            create_time = content.xpath('.//time/@datetime')[0]
            text = content.xpath(
                './/div[contains(@class,"break-words content_truncate__1z0HR")]/text()')
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

            item = {'user': user, 'create_time': create_time, 'text': text, 'image_urls': image_url_list}
            items.append(item)
        return items

    def save_items(self, items):
        try:

            data_Frame = pd.DataFrame(items)
            data_Frame.to_csv('./jike_user.csv', index=False, sep=';')
            return True
        except Exception as e:
            print(e)
            return False


if __name__ == '__main__':
    jike = JiKe('https://web.okjike.com/u/5f88ffbd-9595-4de0-9cf5-b3402bf43a0e')
    page = jike.get_page()
    items = jike.get_items(page)
    jike.save_items(items)
    # for item in items:
    #     for key, value in item.items():
    #         print(key, value)
    #     print("\n")
