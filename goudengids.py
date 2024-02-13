from scrapy.spiders import SitemapSpider
from comapines.items import GoudengidsItem


class GoudengidsSpider(SitemapSpider):
    name = "goudengids"
    allowed_domains = ["goudengids.be"]
    sitemap_urls = ['https://www.goudengids.be/sitemap_nl_be_company_0.xml.gz',
                    'https://www.goudengids.be/sitemap_nl_be_company_1.xml.gz',
                    'https://www.goudengids.be/sitemap_nl_be_company_2.xml.gz',
                    'https://www.goudengids.be/sitemap_nl_be_company_3.xml.gz',
                    ]
    sitemap_rules = [('.*bedrijf.*', 'parse')]

    def parse(self, response):
        item = GoudengidsItem()
        name = response.xpath('//h1/span/text()').get(default='').strip()
        categories = response.xpath('//section[@id="GO__categories"]/ul[@class="flex flex-wrap"]/li//text()').getall()
        website = response.xpath('//a[@itemprop="url"]/@href').get(default='').strip()
        website = website.split('?utm_source=')[0]
        facebook = response.xpath('//div[@id="social-section"]//a[contains(@href, "facebook")]/@href').get(
            default='').strip()
        postal = response.xpath("//span[@data-yext='postal-code']/text()").get(default='').strip()
        city = response.xpath("//span[@data-yext='city']/text()").get(default='').strip()
        street = response.xpath("//span[@data-yext='street']/text()").get(default='').strip()
        number = response.xpath('//a[@id="phoneNumber"]/@data-phone-number').get(default='').strip()
        email = response.xpath('//a[@data-ta="EmailBtnClick"]/href').get(default='').strip()
        if 'mailto:' in email:
            email = email.split('mailto:')[1].split('?subject')[0].strip()
        item['name'] = name
        item['categories'] = categories
        item['website'] = website
        item['facebook'] = facebook
        item['postal'] = postal
        item['city'] = city
        item['street'] = street
        item['number'] = number
        item['email'] = email
        yield item
