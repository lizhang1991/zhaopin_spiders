import scrapy
from fake_useragent import UserAgent
from w3lib.html import remove_tags
from lp.items import JobItem
class Job(scrapy.Spider):
	name = '51job'
	allowed_domains = ['51job.com']
	start_urls = ['https://www.51job.com/']
	
	ua = UserAgent()

	custom_settings={
		'DEFAULT_REQUEST_HEADERS' : {
	   		'User-Agent':ua.random,
	   		'Cookie': 'adv=adsnew%3D1%26%7C%26adsresume%3D1%26%7C%26adsfrom%3Dhttps%253A%252F%252Fwww.baidu.com%252Fbaidu.php%253Fsc.060000jZYuibWkd0M9Wtyy1kaztG-4ULOni6fcQwrtQoZQRPf9VSI1BpeuJGcK5aqFPj4oS4ULCC72GWEeZ8csqfwuJSeTj7wrsyU6u1XVwLSiJ4TRJk3S2e7u62TmPnzmJhS1Ztf0pkpx4ISbWY5oiDMXodHjeaFWrWCIXwB2XA4fr1Kf.7D_NR2Ar5Od66CHnsGtVdXNdlc2D1n2xx81IZ76Y_NvTIOu_zIyT8P9MqOOgujSOODlxdlPqKMWSxKSgqjlSzOFqtZOmzUlZlS5S8QqxZtVAOtItISiel5SKkOeZwSEHNuxSLsfxzcEqolQOY2LOqWq8WvLxVOgVlqoAzAVPBxZub88zuQCUS1FIEtR_4n-LiMGePOBGyAp7Wx_Led0.U1Yk0ZDqkea11jRk0ZKGm1Yk0Zfqkea11jRk0A-V5HczPfKM5yF-TZns0ZNG5yF9pywd0ZKGujYY0APGujY4nsKVIjYknjD1g1DsnH-xnH0kPdtknjfYg1nvnjD0pvbqn0KzIjYkn1R0uy-b5HDYPHNxnWDsrjf0mhbqnW0Y0AdW5HDkrHb4nWmdP7tknj0kg1TdrjRsP164rNtknjFxn0KkTA-b5H00TyPGujYs0ZFMIA7M5H00mycqn7ts0ANzu1Ys0ZKs5Hn4nHmsnjTvn6K8IM0qna3snj0snj0sn0KVIZ0qn0KbuAqs5H00ThCqn0KbugmqTAn0uMfqn0KspjYs0Aq15H00mMTqnH00UMfqn0K1XWY0IZN15HDzrHTvrjbvrjDLnjnLrHcYrj6z0ZF-TgfqnHR1njRkn1DsnWn4r0K1pyfqrj6LnWw-nW6snj0zPjFhufKWTvYqPYnvPWbLP17Afbm4rDmLfsK9m1Yk0ZK85H00TydY5H00Tyd15H00XMfqn0KVmdqhThqV5HKxn7tsg1DsPjuxn0Kbmy4dmhNxTAk9Uh-bT1Ysg1Kxn7t1nHT3Pj7xn0Ksmgwxuhk9u1Ys0AwWpyfqn0K-IA-b5iYk0A71TAPW5H00IgKGUhPW5H00Tydh5HD30AuWIgfqn0KhXh6qn0Khmgfqn0KlTAkdT1Ys0A7buhk9u1Yk0Akhm1Ys0APzm1Y1PHR4ns%2526ck%253D4880.8.120.334.150.260.143.1004%2526shh%253Dwww.baidu.com%2526us%253D1.0.1.0.0.0.0%2526ie%253DUTF-8%2526f%253D8%2526tn%253Dbaidu%2526wd%253D%2525E5%252589%25258D%2525E7%2525A8%25258B51%2526oq%253D%2525E5%252589%25258D%2525E7%2525A8%25258B51%2526rqlang%253Dcn%2526bc%253D110101%26%7C%26adsnum%3D1039482; guid=15305131105469930045; nsearch=jobarea%3D%26%7C%26ord_field%3D%26%7C%26recentSearch0%3D%26%7C%26recentSearch1%3D%26%7C%26recentSearch2%3D%26%7C%26recentSearch3%3D%26%7C%26recentSearch4%3D%26%7C%26collapse_expansion%3D; search=jobarea%7E%60070000%7C%21ord_field%7E%600%7C%21recentSearch0%7E%601%A1%FB%A1%FA070000%2C00%A1%FB%A1%FA000000%A1%FB%A1%FA0000%A1%FB%A1%FA00%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA2%A1%FB%A1%FA%A1%FB%A1%FA-1%A1%FB%A1%FA1530513150%A1%FB%A1%FA0%A1%FB%A1%FA%A1%FB%A1%FA%7C%21; 51job=cenglish%3D0%26%7C%26',
			'Host': 'search.51job.com',
		},
		'ITEM_PIPELINES' : {
   			# 'lp.pipelines.JobPipeline': 2,
		},
	}

	base_url='https://search.51job.com/list/070000,000000,0000,00,9,99,%2520,2,{}.html'

	def parse(self,response):

		for i in range(2000,0,-1):

			fullurl = self.base_url.format(i)

			yield scrapy.Request(fullurl,callback=self.parse_url)

	def parse_url(self,response):

		tag_list = response.xpath('//div[@class="el"]')
		for each_tag in tag_list[4:]:
			try:
				item=JobItem()
				
				tag_title=each_tag.css('p.t1 span a::text')[0].extract().strip('\r\n').strip()
				tag_url=each_tag.css('p.t1 span a::attr(href)')[0].extract()
				tag_company=each_tag.css('span.t2 a::text')[0].extract()
				tag_area=each_tag.css('span.t3 ::text')[0].extract()
				tag_money=each_tag.css('span.t4 ::text')[0].extract()
				tag_pub=each_tag.css('span.t5 ::text')[0].extract()
				
				item['tag_title']=tag_title
				item['tag_url']=tag_url
				item['tag_company']=tag_company
				item['tag_area']=tag_area
				item['tag_money']=tag_money
				item['tag_pub']=tag_pub

				yield scrapy.Request(tag_url,callback=self.parse_info,meta={'item':item})
			except Exception as e:
				pass
	def parse_info(self,response):
		
		item = response.meta['item']

		tag_cate=response.css('p.msg.ltype ::text')[0].extract().replace('\t','').replace('\n','').replace(' ','').replace('\xa0','')
		tag_len=response.css('div.t1 span.sp4 ::text').extract()
		tag_experice=response.css('div.t1 span.sp4 ::text')[0].extract()
		if len(tag_len)==4:
			tag_edu=response.css('div.t1 span.sp4 ::text')[1].extract()
			
		else:
			tag_edu=''
		tag_temptation=response.css('div.jtag.inbox p.t2 span::text').extract()
		tag_temptation='----'.join(tag_temptation)
		tag_content=response.css('div.tBorderTop_box')[1].extract().replace('微信分享邮件','').replace('\n','').replace('\t','')
		tag_content=remove_tags(tag_content,keep=('p',))
		
		item['tag_edu']=tag_edu
		item['tag_cate']=tag_cate
		item['tag_experice']=tag_experice
		item['tag_temptation']=tag_temptation
		item['tag_content']=tag_content
		
		yield item