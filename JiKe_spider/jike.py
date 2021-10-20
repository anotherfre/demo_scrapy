from selenium import webdriver
from lxml import etree


class JiKe:
    def __init__(self, url):
        self.browser = webdriver.Edge()
        self.url = url

    def get_page(self):
        self.browser.get(self.url)
        page = self.browser.page_source
        return page

    def get_items(self, page):
        page_etree = etree.HTML(page)
        content_list = page_etree.xpath('//div[@class="flex flex-col flex-auto pt-2 w-full animate-show min-w-0"]')
        items = []
        for content in content_list:
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
                        let image_list = document.getElementsByClassName("sc-bdnxRM MessagePictureGrid__Cell-sc-pal5rf-3");
                        for(let image of image_list){
                            let bg_image = window.getComputedStyle(image).backgroundImage;
                            src_list.push(bg_image);
                        }
                        return src_list;
                    """
                    images = self.browser.execute_script(js)
                    for image in images:
                        img_src = image.lstrip('url("').rstrip('")')
                        image_url_list.append(img_src)

            item = {'user': user, 'create_time': create_time, 'text': text, 'image_urls': image_url_list}
            items.append(item)
        return items


if __name__ == '__main__':
    jike = JiKe('https://web.okjike.com/u/5f88ffbd-9595-4de0-9cf5-b3402bf43a0e')
    page = jike.get_page()
    items = jike.get_items(page)

    for item in items:
        print(item)
