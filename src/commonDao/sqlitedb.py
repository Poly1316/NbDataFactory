#!/usr/bin/env python
# -*- coding: utf8 -*-
"""此模块封装了sqlite数据库的相关操作功能"""
import sqlite3


class SqliteDb(object):
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()

    def execute(self, sql, param=None):
        """
        用于执行sql语句
        :param param:
        :param sql:sql语句
        :return:异常或者为执行语句行数
        """
        self.cursor.execute(sql, param)

    def fetchone(self):
        """
        返回一条结果
        :return:元组
        """
        return self.cursor.fetchone()

    def fetchall(self):
        """
        #返回所有结果
        :return:（（），（），，，）
        """
        return self.cursor.fetchall()

    def commit(self):
        """
        用于提交事务
        :return:无
        """
        self.conn.commit()

    def close(self):
        """
        用于关闭链接
        :return:无
        """
        self.conn.close()

# if __name__ == '__main__':
#     mysqldb = MySql(host='localhost', user='root', passwd='abc@123', db='mysql')
#     mysqldb.execute('select * from user')
#     result = mysqldb.fetchall()
#     print result


