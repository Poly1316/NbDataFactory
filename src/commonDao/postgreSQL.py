#!/usr/bin/env python
# -*- coding: utf8 -*-
"""此模块封装了GP数据库的相关操作功能"""
import psycopg2


class PostGreSql(object):
    def __init__(self, host=None, user=None, passwd=None, db=None, charset="utf8", port=3306):
        """
        用于连接mysqldb
        :param host:数据库机器ip
        :param user:用户名
        :param passwd:密码
        :param db:被操作数据库名字
        :param charset:编码
        :param port:端口 默认为3306
        :return:异常或者无
        """
        self.conn = psycopg2.connect(host=host, user=user, passwd=passwd, db=db, charset=charset, port=port)
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

    def callproc(self, procname, args):
        """
        用于执行存储过程
        :param procname:存储过程名字
        :param args:参数
        :return:异常或者无
        """
        self.cursor.callproc(procname, args)

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
        self.cursor.close()
        self.conn.close()


# if __name__ == '__main__':
#     mysqldb = MySql(host='localhost', user='root', passwd='abc@123', db='mysql')
#     mysqldb.execute('select * from user')
#     result = mysqldb.fetchall()
#     print result


