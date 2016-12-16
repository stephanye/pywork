import scrapy
from sitesbot.items import DmozItem

class DmozSpider(scrapy.Spider):
    name = "dmoz"
    allowed_domains = ["dmoz.org"]
    start_urls = [
        "http://www.dmoz.org/Computers/Programming/Languages/Python/Books/",
        "http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/"
    ]

    def parse(self, response):
        sites = response.css('#site-list-content > div.site-item')
        items = []
        for site in sites:
            item = DmozItem()
            item['title'] = site.css('a > div.site-title::text').extract_first().strip()
            item['link'] = site.xpath('div/a/@href').extract()
            item['desc'] = site.css('div.site-descr::text').extract_first().strip()
            items.append(item)

        return items
