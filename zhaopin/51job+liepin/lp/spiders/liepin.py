import scrapy
from fake_useragent import UserAgent
from scrapy.conf import settings
from w3lib.html import remove_tags
from lp.items import LpItem


class LiepinSpider(scrapy.Spider):
    name = 'liepin'
    allowed_domains = ['liepin.com']
    start_urls = ['http://www.liepin.com/']
    base_url = 'https://www.liepin.com/zhaopin/?ckid=57c301626d9866c5&fromSearchBtn=2&degradeFlag=0&init=-1&sfrom=click-pc_homepage-centre_searchbox-search_new&key=&headckid=57c301626d9866c5&d_pageSize=40&siTag=1B2M2Y8AsgTpgAmY7PhCfg~fA9rXquZc5IkJpXC-Ycixw&d_headId=5545314aaca5e6240782a1ae440268a7&d_ckId=5545314aaca5e6240782a1ae440268a7&d_sfrom=search_fp&d_curPage=0&curPage=%d'
    ua = UserAgent()
    headers = {
        'User-Agent': ua.random,
    }
    custom_settings={
        'ITEM_PIPELINES' : {
            # 'lp.pipelines.LpPipeline':1,
        },

    }

    def parse(self, response):
        for i in range(0,100+1):
            fullurl = self.base_url % i

            yield scrapy.Request(fullurl, callback=self.parse_url, headers=self.headers, cookies=settings['COOKIES'])

    def parse_url(self, response):

        tag_list = response.xpath('//ul[@class="sojob-list"]//li')
        for tag in tag_list:
            item = LpItem()
            try:
                tag_title = tag.css('div.job-info h3 a::text')[0].extract().strip()
                tag_url = tag.css('div.job-info h3 a::attr(href)')[0].extract()  # 唯一标识
                tag_info = tag.css('p.condition.clearfix ::text').extract()
                tag_area = tag_info[3]
                tag_edu = tag_info[5]
                tag_experice = tag_info[7]  # 经验
                tag_money = tag_info[1].strip('万')
                tag_timeinfo = tag.css('p.time-info.clearfix ::text').extract()
                tag_pub = tag_timeinfo[1]  # 发布时间
                tag_pubcon = tag_timeinfo[3]
                tag_company=tag.css('p.company-name a::text')[0].extract().strip()
                tag_cate=tag.css('p.field-financing span a::text')[0].extract().strip()
                tag_temp=tag.css('p.temptation.clearfix span ::text').extract()
                tag_temptation='----'.join(tag_temp)
                item['tag_cate']=tag_cate
                item['tag_pubcon'] = tag_pubcon
                item['tag_title'] = tag_title
                item['tag_url'] = tag_url
                item['tag_area'] = tag_area
                item['tag_edu'] = tag_edu
                item['tag_experice'] = tag_experice
                item['tag_money'] = tag_money
                item['tag_pub'] = tag_pub
                item['tag_company']=tag_company
                item['tag_cate']=tag_cate
                item['tag_temptation']=tag_temptation

                yield scrapy.Request(tag_url, callback=self.parse_info, headers=self.headers, cookies=settings['COOKIES'],meta={'item': item})
            except Exception as e:
                print(e)

    def parse_info(self, response):
        item = response.meta['item']

        tag_content = response.xpath('//div[@class="job-item main-message job-description"]/div[@class="content content-word"]')[0].extract()
        tag_content = remove_tags(tag_content, keep=('br',))

        item['tag_content'] = tag_content
        yield item

        