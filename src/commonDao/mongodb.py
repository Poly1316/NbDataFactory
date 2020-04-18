#!/usr/bin/env python
# -*- coding: utf8 -*-
"""此模块封装了mongodb数据库的相关操作功能"""


# import pymongo


class MongoDB(object):
    def __init__(self):
        """
        #构造函数
        :return:暂无
        """
        pass

    def mongo_connect(self, host, port, dbname, uname=None, password=None):
        """
        #用于mongod库的连接
        :param host:mongod库ip
        :param port:mongod库port
        :param dbname:数据库名字
        :param uname:用户名  一般很少使用
        :param password:用户密码  一般很少使用
        :return:有异常则返回否则没返回信息
        """
        # import pymongo
        # self.conn = pymongo.Connection(host=host,port=port)
        # if uname is not None and password is not None:
        #     self.auth = self.conn.admin
        #     assert self.auth.authenticate(uname,password)
        #     self.db = self.conn[dbname]
        # else:
        #     self.db = self.conn[dbname]

        from pymongo import MongoClient
        if uname is None and password is None:
            self.client = MongoClient(host=host, port=port)
        else:
            connect_str = 'mongodb' + '://' + uname + ':' + password + '@' + host + ':' + str(port) + '/'
            self.client = MongoClient(connect_str)
        self.db = self.client[dbname]

    def show_collections(self):
        """
        #查看全部表名称，返回列表
        :return:返回列表
        """
        return self.db.collection_names()

    def mongo_select_all(self, tablename, *args, **kwargs):
        """
        #用于查询某表，后面参数支持字符串比对或者某key value的查找（“123”，“123”）（id=“123”，id=“123”）
        （“123”）:查出所有结果中含123 字符串的结果 支持多个，不能和下面的参数方式组合
        （id=“123”）：查出所有结果中id=123的结果  支持多个，不能和上面的参数方式组合
        返回所有结果，返回的是cursor对象，使用遍历取值 每个值是字典类型
        :param tablename:表名
        :param args:筛选串
        :param kwargs:查某个key value的结果 支持多个
        :return:返回的是cursor对象，使用遍历取值 每个值是字典类型
        """
        return self.db[tablename].find(*args, **kwargs)

    def mongo_select_one(self, tablename, *args, **kwargs):
        """
        #用于查询某表，后面参数支持字符串比对或者某key value的查找（“123”，“123”）（id=“123”，id=“123”）
        （“123”）:查出所有结果中含123 字符串的结果 支持多个，不能和下面的参数方式组合
        （id=“123”）：查出所有结果中id=123的结果  支持多个，不能和上面的参数方式组合
        返回一条结果,类型字典
        :param tablename:表名
        :param args:筛选串
        :param kwargs:查某个key value的结果 支持多个
        :return:类型字典
        """
        return self.db[tablename].find_one(*args, **kwargs)

    def mongo_insert(self, tablename, *args, **kwargs):
        """
        #用于插入结果
        :param tablename:表名
        :param args:按顺序的数据值，不建议
        :param kwargs:key value 值队
        :return:无
        """
        return self.db[tablename].insert(*args, **kwargs)

    def mongo_save(self, tablename, *args, **kwargs):
        """
        #用于保存结果
        :param tablename:表名
        :param args:删保存的values
        :param kwargs:带删除的值对 key value 建议使用此种
        :return:无
        """
        return self.db[tablename].save(*args, **kwargs)

    def mongo_distinct(self, tablename, key):
        """
        #获取表的字段的所有值，结果去重，类型list
        :param tablename:表名
        :param key:待查key
        :return:结果去重，类型list
        """
        return self.db[tablename].distinct(key)

    def mongo_update(self, tablename, *args, **kwargs):
        """
        #更新表数据({‘name’:'foobar’},{‘$set’:{‘age’:36}})，将记录name=foobar中的age更新36
        :param tablename:表名
        :param args:
        :param kwargs:
        :return:
        """
        return self.db[tablename].update(upsert=False, multi=True, *args, **kwargs)

    def mongo_deleted(self, tablename, *args, **kwargs):
        """
        #按筛选条件，删除记录
        :param tablename:表名
        :param args:待删除筛选串
        :param kwargs:待删除筛选key v 对
        :return:无
        """
        return self.db[tablename].remove(*args, **kwargs)

    def mongo_dropTable(self, tablename):
        """
        #删除表
        :param tablename:删除表名
        :return:无
        """
        return self.db.drop_collection(tablename)

    def mongo_count(self, tablename, *args, **kwargs):
        """
        #查询符合某条件的记录数，类型int
        :param tablename:待查询表名
        :param args:待查询筛选串
        :param kwargs:待查询筛选key v 对
        :return:记录数字，类型int
        """
        return self.db[tablename].find(*args, **kwargs).count()

    def mongo_creat_table(self, tablename, **kwargs):
        """
        #在此用户下创建表
        :param tablename:表名
        :param kwargs:表字段属性
        :return:无
        """
        self.db.create_collection(tablename, **kwargs)

    def close(self):
        """
        #关闭芒果链接
        :return:无
        """
        return self.client.close()


if __name__ == '__main__':
    a = MongoDB()
    a.mongo_connect(host='172.16.114.237', port=27017, dbname='admin', uname='fhmgdb', password='wzmgdb')
    print a.show_collections()
