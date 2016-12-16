import scrapy
from scrapy.selector import Selector
from sitesbot.items import WxsgItem
from scrapy.http import Request

class WxsgSpider(scrapy.Spider):
    name = "wxsg"
    allowed_domains =["sogou.com","xizi.com","weixin.sogou.com"]
    headers={
        "Accept":"*/*",
        "Accept-Encoding":"gzip, deflate, sdch",
        "Accept-Language":"zh-CN,zh;q=0.8",
        "Cache-Control":"no-cache",
        "Connection":"keep-alive",
        "Referer":"http://weixin.sogou.com/",
        "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
        "X-Requested-With":"XMLHttpRequest"
    }
    start_urls=[
        "http://weixin.sogou.com/pcindex/pc/pc_0/1.html",
    ]
    print '---------------------2-dd-d--------------------------'

    def start_requests(self):
        return [Request("http://weixin.sogou.com/pcindex/pc/pc_0/1.html",headers=self.headers)]

    def parse(self,response):
        sites = response.css('li')
        print '---------------------3-dd-d--------------------------'
        items=[]
        for site in sites:
            item =WxsgItem()
            item['title'] = site.css('div.txt-box > h3 > a::text').extract_first().strip()
            item['link'] = site.xpath('div/a/@href').extract()
            print item['title']

        return items