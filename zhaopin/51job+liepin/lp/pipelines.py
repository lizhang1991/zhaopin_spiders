# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from scrapy.conf import settings

class LpPipeline(object):
    def process_item(self, item, spider):
        return item


class LpPipeline(object):
	def open_spider(self,spider):
		my=settings['MYSQL']
		self.coon=pymysql.connect(my['host'],my['user'],my['pwd'],my['db'],charset='utf8')
		self.cursor=self.coon.cursor()


	def process_item(self,item,spider):
		try:
			sql,data=item.get_sql()
			self.cursor.execute(sql,data)
			self.coon.commit()
			print('写入成功%s'%item['tag_title'])
		except Exception as e:
			print(e,'写入失败')
			self.coon.rollback()

	def close_spider(self,spider):

		self.cursor.close()
		self.coon.close()

class JobPipeline(object):
	
	def open_spider(self,spider):
		my=settings['MYSQL']
		self.coon=pymysql.connect(my['host'],my['user'],my['pwd'],my['db'],charset='utf8')
		self.cursor=self.coon.cursor()
		

	def process_item(self,item,spider):
		try:
			item['spider']=spider.name
			sql,data=item.get_sql_qc()
			self.cursor.execute(sql,data)
			self.coon.commit()
			print('写入成功%s'%item['tag_title'])
		except Exception as e:
			print(e,'写入失败')
			self.coon.rollback()

	def close_spider(self,spider):

		self.cursor.close()
		self.coon.close()
