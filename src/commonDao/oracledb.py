#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
此模块封装了oracledb数据库的相关操作功能，以及打开关闭数据库操作等功能
2017-11-10 汪啸涛新增out_all_ora_dict用于返回两个查询结果的字典值
"""

import cx_Oracle
import sys


class OracleDB(object):
    def __init__(self, *args, **kwargs):
        """
        #用于链接oracle数据库，支持两种参数，一般使用Conn_ora('noahpf','noahpf','10.0.126.45:1521/ora11g')即可
        :param args:list型参数
        :param kwargs:字典型参数
        """
        from os import environ
        environ['NLS_LANG'] = 'american_america.AL32UTF8'

        self.Conn = cx_Oracle.connect(*args, **kwargs)
        self.Cursor = self.Conn.cursor()

    def close_ora(self):
        """
        #用于关闭数据库链接
        :return:返回状态和有异常则返回异常信息
        """
        try:
            self.Conn.close()
            return True, ""
        except StandardError as e:
            return False, e

    def select_ora(self, strSQL):
        """
        #用于执行select查询式语句
        :param strSQL: 查询语句
        :return:返回状态和有异常则返回异常信息
        """
        try:
            self.Cursor.execute(strSQL)
            return True, ""
        except StandardError as e:
            return False, e

    def commit(self):
        self.Conn.commit()

    def cmd_ora(self, strSQL):
        """
        #用于执行cmd执行式语句，并且默认都会commit
        :param strSQL: cmd执行式语句,类型str或者list
        :return:返回状态和有异常则返回异常信息
        """
        try:
            if isinstance(strSQL, str):
                self.Cursor.execute(strSQL)
            if isinstance(strSQL, list):
                for eachstr in strSQL:
                    self.Cursor.execute(eachstr)
            self.Conn.commit()
            return True, ""
        except StandardError as e:
            return False, e

    def run_callproc(self, name, parameters=None, keywordParameters=None):
        """
        #暂时不使用
        :param name:
        :param parameters:   []
        :param keywordParameters: {}
        :return:返回状态和有异常则返回异常信息
        """
        if parameters is None:
            parameters = []

        if keywordParameters is None:
            keywordParameters = {}

        self.Cursor = self.Conn.cursor()
        try:
            self.Cursor.callproc(name, parameters, keywordParameters)
            self.Conn.commit()
            return True, ""
        except StandardError as e:
            return False, e

    def run_callfunc(self, name, returnType, parameters=None, keywordParameters=None):
        """
        #暂时不使用
        :param name:
        :param returnType:
        :param parameters: []
        :param keywordParameters: {}
        :return:返回状态和有异常则返回异常信息
        """
        if parameters is None:
            parameters = []

        if keywordParameters is None:
            keywordParameters = {}

        self.Cursor = self.Conn.cursor(name, returnType, parameters, keywordParameters)
        try:
            self.Cursor.callfunc()
            self.Conn.commit()
            return True, ""
        except StandardError as e:
            return False, e

    def out_all_ora(self):
        """
        #查询完毕用于返回查询结果，这是一次性返回所有结果，返回类型list，每个元素是元组
        :return:（状态，（返回类型list，每个元素是元组）或者（异常信息））
        """
        try:
            __Row = self.Cursor.fetchall()
            return True, __Row
        except StandardError as ee:
            return False, e

    def out_one_ora(self):
        """
        #查询完毕用于返回查询结果，这是一次性返回一条记录结果，再次运行返回下一条结果.返回类型元组
        :return:（状态，（返回类型元组）或者（异常信息））
        """
        try:
            __Row = self.Cursor.fetchone()
            return True, __Row
        except StandardError as e:
            return False, e

    def out_all_ora_dict(self):
        """
        #查询完毕用于返回查询结果，这是一次性返回所有结果，返回类型dict
        :return:（状态，（返回类型dict）或者（异常信息））,如：{'230305820620126': 3}
        """
        try:
            __Row = self.Cursor.fetchall()
            result = {}
            for line in __Row:
                result[list(line)[0]] = list(line)[1]
            return result
        except StandardError as e:
            return False, e


class DealOra():
    def __init__(self, ipup):
        """
        #此类主要用于oracle数据库的关闭和打开，以及关于监听的操作
        :param ipup: oracle所在机器的ip user pwd
        :return: 无
        """
        self.oo = SSH()
        self.oo.connect(ipup)

    def startup_ora(self):
        """
        打开数据库
        :return:assert
        """
        su_status, su_out, su_err = self.oo.exec_command(
            'echo "startup"|sqlplus  sys/sys as sysdba')
        print (su_status, su_out, su_err)
        assert su_status == 0, (su_out, su_err)

    def shutdown_ora(self):
        """
        关闭数据库
        :return:assert
        """
        sd_status, sd_out, sd_err = self.oo.exec_command(
            'echo "shutdown immediate"|sqlplus  sys/sys as sysdba')
        assert sd_status == 0, (sd_out, sd_err)

    def lsnrctl_ora(self, status=None, justdo=True):
        """
        关于监听的操作
        :param status: 一般为start restart status
        :return:
        """
        l_status, l_out, l_err = self.oo.exec_command('lsnrctl {}'.format(status))
        if justdo:
            return l_status, l_out, l_err
        else:
            assert l_status == 0, (l_out, l_err)

if __name__ == '__main__':
    ord = OracleDB('nbpf', 'nbpf', '172.16.40.85:1521/ora11g')
    ord.select_ora('select * from nb_logs')
    _result = ord.out_one_ora()
    print _result


