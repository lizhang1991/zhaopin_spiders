# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LpItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
	tag_title = scrapy.Field()
	tag_url = scrapy.Field()  # 标识
	tag_area = scrapy.Field()
	tag_edu = scrapy.Field()
	tag_experice = scrapy.Field()
	tag_money = scrapy.Field()
	tag_pub = scrapy.Field()
	tag_pubcon = scrapy.Field()
	tag_content = scrapy.Field()
	tag_company=scrapy.Field()
	tag_cate=scrapy.Field()
	tag_temptation=scrapy.Field()
	
	def get_sql(self):
		sql='insert into liepin(tag_title,tag_url,tag_area,tag_edu,tag_experice,tag_money,tag_pub,tag_pubcon,tag_content,tag_company,tag_cate,tag_temptation)'\
		'values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
		data=(self['tag_title'],self['tag_url'],self['tag_area'],self['tag_edu'],self['tag_experice'],self['tag_money'],self['tag_pub'],self['tag_pubcon'],self['tag_content'],self['tag_company'],self['tag_cate'],self['tag_temptation'])

		return sql,data


class JobItem(scrapy.Item):
	
	tag_title=scrapy.Field()
	tag_area=scrapy.Field()
	tag_edu=scrapy.Field()
	tag_experice=scrapy.Field()
	tag_money=scrapy.Field()
	tag_pub=scrapy.Field()
	tag_url=scrapy.Field()
	tag_content=scrapy.Field()
	tag_company=scrapy.Field()
	tag_cate=scrapy.Field()
	tag_temptation=scrapy.Field()
	spider=scrapy.Field()

	def get_sql_qc(self):

		sql='insert into qcwy(tag_title,tag_area,tag_edu,tag_experice,tag_money,tag_pub,tag_url,tag_content,tag_company,tag_cate,tag_temptation,spider)'\
		'values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
		data=(self['tag_title'],self['tag_area'],self['tag_edu'],self['tag_experice'],self['tag_money'],self['tag_pub'],self['tag_url'],self['tag_content'],self['tag_company'],self['tag_cate'],self['tag_temptation'],self['spider'])


		return sql,data