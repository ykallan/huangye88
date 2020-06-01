# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import csv
import pymysql
pymysql.install_as_MySQLdb()


class HuangyePipeline(object):

    def __init__(self):

        # # 打开文件，指定方式为写，利用第3个参数把csv写数据时产生的空行消除
        # self.f = open("huangyexinxi.csv", "a", newline="", encoding='utf-8')
        # # 设置文件第一行的字段名，注意要跟spider传过来的字典key名称相同
        # self.fieldnames = ['person_name', 'phone', 'com_name', 'address']
        # # 名称 场馆 日期 主办方 地址 城市 详情
        # # 指定文件的写入方式为csv字典写入，参数1为指定具体文件，参数2为指定字段名
        # self.writer = csv.DictWriter(self.f, fieldnames=self.fieldnames)
        # # 写入第一行字段名，因为只要写入一次，所以文件放在__init__里面
        # self.writer.writeheader()
        self.conn = pymysql.Connect(
            host='localhost',
            port=3306,
            database='scrapy',
            user='root',
            passwd='root',
            charset='utf8',
            # use_unicode=True
        )

        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        # 写入spider传过来的具体数值
        # self.writer.writerow(item)
        # 写入完返回

        self.cursor.execute('''INSERT INTO huangye(person_name, phone, com_name, address) VALUES(%s, %s, %s, %s)''',
                            (item['person_name'], item['phone'], item['com_name'], item['address']))
        self.conn.commit()

        # item['com_name'] = com_name
        # item['person_name'] = person_name
        # item['phone'] = phone[0]
        # item['address'] = address

    def close(self, spider):
        # self.f.close()
        pass


