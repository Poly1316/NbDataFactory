# -*- coding: utf-8 -*-
"""
@author wangxiaotao
@version 0.0.3
Created on 2017-8-8
"常用的公共方法"
"""
import os.path
import re
import socket
import sys
import time
import random
import hashlib
import logging
import paramiko
import pypinyin
import ConfigParser
import pandas as pd
from mysqldb import MySql
from time import localtime
from datetime import datetime
from pypinyin import lazy_pinyin
from src.dataDao import addr

reload(sys)
sys.setdefaultencoding('utf-8')


class CommonUtil(object):
    def __init__(self):
        self.area_dict = addr.area_dict

    @staticmethod
    def incolorprint(content, color=None):
        """
        :param content: 打印内容
        :param color: 打印字体颜色，默认黑色
        :return:
        """
        if color is not None:
            color = color.upper()
            if color == 'RED':
                print "{0}[31;2m{1}{2}[0m".format(chr(27), content, chr(27))
            elif color == 'GREEN':
                print "{0}[32;2m{1}{2}[0m".format(chr(27), content, chr(27))
            elif color == 'YELLOW':
                print "{0}[33;2m{1}{2}[0m".format(chr(27), content, chr(27))
        else:
            print content

    @staticmethod
    def abs_path(py_file, conf_dir=None):
        """
        返回文件的绝对路径
        :param py_file:文件对象__file__,或者是文件名  str
        :param conf_dir：默认直接去当前路径，如果此有值，在路径上加上此路径，str
        abs_path(__file__) 返回文件的目录路径
        abs_path(__file__，"data") 返回文件的目录路径/data
        """
        if conf_dir is None:
            conf_dir = ""
        return os.path.normpath(
            os.path.join(os.path.normpath(
                os.path.dirname(os.path.realpath(py_file))), conf_dir))

    @staticmethod
    def get_config(type, para, file_path='../Config/config.conf'):
        """
        获取配置文件中，对应配置
        """
        config = ConfigParser.ConfigParser()
        config_path = CommonUtil.abs_path(__file__, file_path)
        with open(config_path, 'r') as cfgfile:
            config.readfp(cfgfile)
            agreement = config.get(type, para)
        return agreement

    @staticmethod
    def stamp2time(stamp_time, pattern='%Y-%m-%d %H:%M:%S'):
        """
        时间戳转换为标准时间
        :param pattern: 时间格式化字符串，默认为'%Y-%m-%d %H:%M:%S'
        :param stamp_time:1505126123
        :return:2017-09-11 18:35:23
        """
        try:
            __result = time.strftime(pattern, localtime(float(stamp_time)))
        except Exception as ex:
            logging.debug(u'时间转换失败，输入时间为【{0}】，{1}'.format(stamp_time, ex))
            __result = 0
        return __result

    @staticmethod
    def time2stamp(time_str, pattern='%Y-%m-%d %H:%M:%S'):
        """
        将时间转换为时间戳
        :param time_str:时间字符串
        :param pattern: 时间格式化字符串
        :return: 返回绝对时间，int格式
        """
        if isinstance(time_str, str):
            pass
        else:
            return

        __time_array = time.strptime(time_str, pattern)  # 时间转换为时间数组
        return int(time.mktime(__time_array))

    @staticmethod
    def current_time(pattern='%Y%m%d'):
        """
        获取当前年月日，格式为20171113
        :param pattern:返回当前时间的格式化字符串，默认为 '%Y%m%d'
        :return:按照格式化字符串返回当前时间格式
        """
        return datetime.now().strftime(pattern)

    @staticmethod
    def current_stamp():
        """
        获取当前时间戳
        :return:
        """
        return int(time.time())

    @staticmethod
    def md5_sth(string):
        """
        生成字符串MD5值
        :param string:
        :return:
        """
        if isinstance(string, str):
            pass
        else:
            return

        __md5 = hashlib.md5()
        __md5.update(string)
        return __md5.hexdigest()

    @staticmethod
    def excel_read(file_path, col=0, start_rowx=0, end_rowx=None, sheet=0):
        """
        读取excel的方法
        :param file_path:excel文件的路径，或者excel文件
        :param col: 读取的列数
        :param sheet: 读取的表格
        :param start_rowx: 读取列开始的行数，默认为0
        :param end_rowx: 读取结束的行数，默认为0
        :return: 返回列数据
        """
        if os.path.exists(file_path):
            pass
        else:
            return

        import xlrd
        try:
            data = xlrd.open_workbook(file_path)
            table = data.sheets()[sheet]
            col_value = table.col_values(col, start_rowx, end_rowx)
            return col_value
        except Exception as ex:
            logging.error(u'Excel file not found,{0}'.format(ex))
            return None

    @staticmethod
    def get_row_by_str(xls_file, string, sheet=0, row=0):
        """
        通过查找指定列的数据，返回该数据所在的列序号
        :param row: 查找的行数
        :param sheet: excel所在的sheet，第一个为0
        :param xls_file:读取的excel文件路径
        :param string:查找的数据
        :return:返回数据列数最大值和最小值 ，如：(2342, 2370)
        """
        l = []
        import xlrd
        wb = xlrd.open_workbook(xls_file)
        sheet = wb.sheet_by_index(sheet)
        i = 1
        for __row in range(sheet.nrows):
            c_row = sheet.row(__row)
            if str(c_row[row].value) == str(string):
                l.append(i)
            i += 1
        return min(l), max(l)

    @staticmethod
    def old2new(old_id):
        """
        "15位号码转18位号码"
        :param old_id: 待转换身份证
        :return:类型str，18位
        """
        __verify = ('1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2')
        __iw = (7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2)
        _current_y = int(str(localtime()[0])[2:4])
        if len(old_id) is 15:
            if int(old_id[6:8]) > abs(int(_current_y - 80)):
                old_card = '%s19%s' % (old_id[:6], old_id[6:])
            else:
                old_card = '%s20%s' % (old_id[:6], old_id[6:])
            _verifyid = __verify[sum(map(lambda x: int(x[0]) * x[1], zip(old_card[0:17], __iw))) % 11]
            return '%s%s' % (old_card, _verifyid)

    @staticmethod
    def new2old(new_id):
        """
        #18位号码转15位号码
        :param new_id: 待转换身份证
        :return:类型str，15位
        """
        if isinstance(new_id, str):
            pass
        else:
            return 'input type is not str'

        if len(new_id) is 18:
            new_card = new_id[:6] + new_id[8:][:9]
            return new_card

    @staticmethod
    def word2pinyin(string_word):
        """
        汉字转拼音
        :param string_word: 汉字，如：‘中国’
        :return:返回'ZHONGGUO'
        """
        string_word = unicode(string_word)
        return ''.join(lazy_pinyin(string_word, style=pypinyin.NORMAL)).upper()

    @staticmethod
    def check_mobile(mobile):
        """
        手机号长度及合法性校验
        :param mobile: list类型，例：['13888888888', '13666666666']
        :return:
        """
        if isinstance(mobile, list) is False:
            logging.error(u'请输入列表型手机号')
            return False
        for every_mobile in mobile:
            length_mobile = len(every_mobile)
            if length_mobile == 11:
                if re.match("^(13[0-9]|15[012356789]|17[013678]|18[0-9]|14[57])[0-9]{8}$", every_mobile):
                    return True
                else:
                    logging.error(u'手机号【{0}】验证不通过，不合法的手机号'.format(every_mobile))
            else:
                logging.error(u'手机号【{0}】长度不合法，长度为【{1}】'.format(every_mobile, length_mobile))

    @staticmethod
    def check_mobile_every(mobile):
        """
        手机号长度及合法性校验
        :param mobile: str类型，例：'13888888888'
        :return:
        """
        length_mobile = len(mobile)
        if length_mobile == 11:
            if re.match("^(13[0-9]|15[012356789]|17[013678]|18[0-9]|14[57])[0-9]{8}$", mobile):
                return True
            else:
                logging.error(u'手机号【{0}】验证不通过，不合法的手机号'.format(mobile))
                return False
        else:
            logging.error(u'手机号【{0}】长度不合法，长度为【{1}】'.format(mobile, length_mobile))
            return False

    @staticmethod
    def check_wz(id_list):
        """
        查找字典表，确认人员是否属于维族人员
        :param id_list:人员身份证号列表，list类型，如果不是list类型，也可以进行转换
        :return:返回维族人员列表
        """
        if isinstance(id_list, list):
            pass
        elif isinstance(id_list, list):
            id_list = [id_list]
        else:
            return

        __path = CommonUtil.get_config('wz_dict', 'dict_path', '../Config/config.conf')  # 字典配置所在路径
        __wz_people = []
        for line in id_list:
            if line[0:2] != '65':
                continue
            __file_name = '{0}.txt'.format(line[0:6])
            file_path = '{0}\\{1}'.format(__path, __file_name)
            if not os.path.exists(file_path):
                logging.warning(u'身份证【{0}】对应的字典文件不存在'.format(line))
                continue

            with open(file_path, 'rb') as __all_reader:
                for __reader in __all_reader:
                    if line in __reader:
                        logging.info(u'人员【{0}】是维族人员'.format(line))
                        __wz_people.append(line)
                        id_list.remove(line)
                        break
                __all_reader.close()
        return __wz_people, id_list

    @staticmethod
    def check_wz_one(id_str):
        """
        检查单个身份证号是否属于新疆维族人员，如果属于维族人员，则返回True，如果不属于则返回False
        :param id_str: 身份证号，str类型
        :return: True或者False
        """
        if id_str[0:2] != '65':
            return False
        __path = CommonUtil.get_config('wz_dict', 'dict_path', '../Config/config.conf')  # 字典配置所在路径
        __file_name = '{0}.txt'.format(id_str[0:6])
        file_path = '{0}\\{1}'.format(__path, __file_name)
        if not os.path.exists(file_path):
            logging.warning(u'身份证【{0}】对应的字典文件不存在'.format(id_str))
            return False

        with open(file_path, 'rb') as __all_reader:
            for __reader in __all_reader:
                if id_str in __reader:
                    logging.info(u'人员【{0}】是维族人员'.format(id_str))
                    return True
        return False

    @staticmethod
    def get_local_name():
        """
        获取本机电脑名，返回类型str
        例子1：
        print get_local_name()
        SKY-20160601PMP
        :return:
        """
        return socket.getfqdn(socket.gethostname())

    def get_local_ip(self):
        """
        #获取本机ip，返回类型str
            例子1：
            print get_local_ip()
            10.0.24.60
        """
        return socket.gethostbyname(self.get_local_name())

    @staticmethod
    def is_id_card(id_number):
        """
        身份证号校验
        :param id_number:输入为str类型，18位身份证号
        :return:
        """
        import datetime
        if isinstance(id_number, int):
            logging.error(u'不合法的身份证类型，{0}'.format(id_number))
            return False
        area_dict = {11: "北京", 12: "天津", 13: "河北", 14: "山西", 15: "内蒙古", 21: "辽宁", 22: "吉林", 23: "黑龙江", 31: "上海",
                     32: "江苏",
                     33: "浙江", 34: "安徽", 35: "福建", 36: "江西", 37: "山东", 41: "河南", 42: "湖北", 43: "湖南", 44: "广东", 45: "广西",
                     46: "海南", 50: "重庆", 51: "四川", 52: "贵州", 53: "云南", 54: "西藏", 61: "陕西", 62: "甘肃", 63: "青海", 64: "新疆",
                     71: "台湾", 81: "香港", 82: "澳门", 91: "外国"}
        id_code_list = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
        check_code_list = [1, 0, 'X', 9, 8, 7, 6, 5, 4, 3, 2]
        if len(id_number) != 18:
            return False, "Length error"
        if not re.match(r"^\d{17}(\d|X|x)$", id_number):
            return False, "Format error"
        if int(id_number[0:2]) not in area_dict:
            return False, "Area code error"
        try:
            datetime.date(int(id_number[6:10]), int(id_number[10:12]), int(id_number[12:14]))
        except ValueError as ve:
            return False, "Datetime error: {0}".format(ve)
        if check_code_list[sum([a * b for a, b in zip(id_code_list, [int(a) for a in id_number[0:-1]])]) % 11] != \
                id_number.upper()[-1]:
            return False, "Check code error"
        return True

    @staticmethod
    def format_time(origin_time='2017/12/29', origin_pattern='%Y/%m/%d', pattern='%Y-%m-%d'):
        """
        时间格式化方法，输入任意一个时间以及该时间的格式，返回指定格式的时间
        :param origin_time: 原始时间
        :param origin_pattern: 原始时间格式
        :param pattern: 需要返回的时间格式
        :return: 返回指定格式的时间
        """
        return datetime.strptime(origin_time, origin_pattern).strftime(pattern)

    @staticmethod
    def query_source(source_id):
        """
        通过source_id查询对象来源，source字典存在Oracle_Data_Analys.conf配置文件
        :param source_id:
        :return:
        """
        try:
            source_dict = CommonUtil.get_config('ATTRIBUTE_SOURCE', 'source', '../Config/CountryTaskLog.conf')
            return eval(source_dict)[source_id]
        except Exception as ex:
            logging.warning(u'该source_id没有对应的来源字典，{0}'.format(ex))
            return source_id

    @staticmethod
    def upload(local_dir, remote_dir, hostname, username, password, port=22):
        """
        从Windows本地上传文件到linux系统
        :param local_dir: 本地文件所在目录
        :param remote_dir: Linux文件需要存放的目录
        :param hostname: Linux系统IP地址
        :param username: Linux系统登录名，一般为root
        :param password: Linux系统登录密码
        :param port: Linux系统登录端口，默认为22
        :return:
        """
        try:
            t = paramiko.Transport(hostname, port)
            t.connect(username=username, password=password)
            sftp = paramiko.SFTPClient.from_transport(t)
            logging.debug('upload file start %s ' % datetime.now())
            for root, dirs, files in os.walk(local_dir):
                logging.debug('[%s][%s][%s]' % (root, dirs, files))
                for filespath in files:
                    local_file = os.path.join(root, filespath)
                    logging.debug('[%s][%s][%s][%s]' % (root, filespath, local_file, local_dir))
                    a = local_file.replace(local_dir, '').replace('\\', '/').lstrip('/')
                    remote_file = os.path.join(remote_dir, a)
                    try:
                        sftp.put(local_file, remote_file)
                    except Exception as e:
                        sftp.mkdir(os.path.split(remote_file)[0])
                        sftp.put(local_file, remote_file)
                        logging.debug("upload {0} to remote {1}, {2}".format(local_file, remote_file, e))
                for name in dirs:
                    local_path = os.path.join(root, name)
                    a = local_path.replace(local_dir, '').replace('\\', '')
                    remote_path = os.path.join(remote_dir, a)
                    logging.debug('remote_path[{0}]'.format(remote_path))
                    try:
                        sftp.mkdir(remote_path)
                    except Exception as e:
                        logging.debug(e)
            logging.info('upload file success %s ' % datetime.now())
            t.close()
        except Exception as e:
            logging.debug(e)

    @staticmethod
    def get_file_list(folder, mode=0):
        """
        获取某路径下文件路径的方法，返回list
        :param mode: 根据mode字段确定返回全部路径列表还是文件名列表
        :param folder: 如：''G:\\python-project\\fk\\fileDao\\yuqing_nb'
        :return: 如：['G:\\python-project\\fk\\fileDao\\yuqing_nb\\nb_app_sentiment_info-1504290692-20171129-12.nb']
        """
        file_list = []
        for root, dirs, files in os.walk(folder):
            for f in files:
                if mode == 0:
                    path = root + os.path.sep + f
                else:
                    path = f
                file_list.append(path)
        return file_list

    def get_birth_date(self, credit_id, split_sign='-'):
        """
        根据身份证号返回人员出生日期
        :param credit_id: 身份证号，支持18位或者15位
        :param split_sign: 出身日期分隔符
        :return: 返回出身日期，如：'1961-05-30'
        """
        if isinstance(credit_id, int):
            credit_id = str(credit_id)
        if len(credit_id) == 18:
            pass
        elif len(credit_id) == 15:
            credit_id = self.new2old(credit_id)
        else:
            return 'not valid credit_id'
        return '{0}'.format(split_sign).join([credit_id[6:10], credit_id[10:12], credit_id[12:14]])

    def get_sex(self, credit_id):
        """
        根据身份证号获取人员性别
        :param credit_id: 身份证号，支持18位或者15位
        :return: 返回性别，如：'男'
        """
        credit_id = str(credit_id)
        if len(credit_id) == 15:
            credit_id = self.new2old(credit_id)
        elif len(credit_id) == 18:
            pass
        else:
            return 'not valid credit_id'
        if int(credit_id[16]) % 2:
            sex = '男'
        else:
            sex = '女'
        return sex

    def get_area_by_credit(self, credit_id):
        """
        通过身份证号返回籍贯区域编码
        :param credit_id:身份证号码，支持18位和15位
        :return:返回区域编码和区域名称元组
        """
        if len(credit_id) == 15:
            credit_id = self.new2old(credit_id)
        elif len(credit_id) == 18:
            pass
        else:
            return 'not valid credit_id'
        __area = credit_id[0:6]
        return __area, self.area_dict[int(__area)]

    def prettyXml(self, element, indent, newline, level=0):  # element为传进来的Elment类，参数indent用于缩进，newline用于换行
        if element is not None:  # 判断element是否有子元素
            if element.text == None or element.text.isspace():  # 如果element的text没有内容
                element.text = newline + indent * (level + 1)
            else:
                element.text = newline + indent * (level + 1) + element.text.strip() + newline + indent * (level + 1)
                # else:  # 此处两行如果把注释去掉，Element的text也会另起一行
                # element.text = newline + indent * (level + 1) + element.text.strip() + newline + indent * level
        temp = list(element)  # 将elemnt转成list
        for subelement in temp:
            if temp.index(subelement) < (len(temp) - 1):  # 如果不是list的最后一个元素，说明下一个行是同级别元素的起始，缩进应一致
                subelement.tail = newline + indent * (level + 1)
            else:  # 如果是list的最后一个元素， 说明下一行是母元素的结束，缩进应该少一个
                subelement.tail = newline + indent * level
            self.prettyXml(subelement, indent, newline, level=level + 1)  # 对子元素进行递归操作

    @staticmethod
    def date_list(beginDate, endDate):
        # beginDate, endDate是形如‘20160601’的字符串或datetime格式
        __date = [datetime.strftime(x, '%Y-%m-%d') for x in list(pd.date_range(start=beginDate, end=endDate))]
        return __date


class SshLinux(object):
    def __init__(self, host, username, password, port=22):
        """
        'linux远程实现,利用paramiko'
        :param command:需要执行的命令
        :return:返回命令执行结果
        """
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(host, int(port), username, password)

    def linux_cmd(self, command):
        """
        Linux命令执行
        :param command: 需要执行的命令
        :return:
        """
        stdin, stdout, stderr = self.ssh.exec_command(command)
        err = stderr.readlines()
        out = stdout.readlines()
        if (err):
            logging.error(u'查询出错{0}'.format(err))
        else:
            return str(out).decode('string_escape')

    def ssh_close(self):
        self.ssh.close()


class TestDb(object):
    def __init__(self):
        cul = CommonUtil()
        host = cul.get_config('test_mysql', 'mysql_host', '../Config/config.conf')
        user = cul.get_config('test_mysql', 'mysql_user', '../Config/config.conf')
        passwd = cul.get_config('test_mysql', 'mysql_password', '../Config/config.conf')
        db = cul.get_config('test_mysql', 'mysql_db', '../Config/config.conf')
        self.my_db = MySql(host, user, passwd, db)

    def insert_test_attribute(self, values):
        """
        mysql插入SQL封装
        :param values: 插入的字段值，接受元组类型，与字段一一对应
        :return: 无
        """
        insert_sql = "insert into test_attribute_info (ID, ATTRIBUTE_VALUE, OBJECT_ID, TEST_TYPE, CREATE_TIME, " \
                     "CREATE_USER, INSERT_REASON, INSERT_PLACE) values {0}".format(values)
        logging.debug(insert_sql)
        self.my_db.execute(insert_sql)
        self.my_db.commit()

    def insert_test_action(self, values):
        """
        mysql插入SQL封装
        :param values: 插入的字段值，接受元组类型，与字段一一对应
        :return: 无
        """
        insert_sql = "insert into test_action (ACTION_ID, ATTRIBUTE_TYPE, ATTRIBUTE_VALUE, OBJECT_ID, " \
                     "START_TIME, END_TIME, AREA_ID, ADDRESS, NAME, LON, LAT, DESCRIBE_ACTION, INSERT_TIME, " \
                     "CREATE_TIME, DETAIL, RES_CODE, DATA_MD5, RULE_ID) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s," \
                     "%s,%s,%s,%s,%s,%s,%s,%s)"
        logging.debug('{0}{1}'.format(insert_sql, values))
        self.my_db.execute(insert_sql, values)
        self.my_db.commit()

    def insert_test_trans(self, values):
        """
        mysql插入SQL封装
        :param field:插入的字段名，接受元组类型
        :param values: 插入的字段值，接受元组类型，与字段一一对应
        :param table_name: 插入的表名字
        :return: 无
        """
        insert_sql = "insert into test_trans (TRANS_ID,ATTRIBUTE_TYPE,ATTRIBUTE_VALUE,OBJECT_ID,RESOURCES_TYPE," \
                     "PLACE_NAME,SOURCE_CITY,TARGET_CITY,SOURCE_TIME,TARGET_TIME,ALARM_TIME,CREATE_TIME,STATUS," \
                     "RESOURCES_TABLE_NAME,RESOURCES_TABLE_PK,RESOURCES_TABLE_PK_VALUE,REMARK,SOURCE_LON,SOURCE_LAT," \
                     "TARGET_LON,TARGET_LAT,RES_CODE,INSERT_TIME,DATA_FLAG,RULE_ID) values (%s,%s,%s,%s,%s,%s,%s," \
                     "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        logging.debug('{0}{1}'.format(insert_sql, values))
        self.my_db.execute(insert_sql, values)
        self.my_db.commit()

    def query_id(self, id_field='id', table_name='test_attribute_info'):
        """
        查询表中最大ID
        :param id_field:
        :param table_name:
        :return:
        """
        __sql = "select max({0}) from {1}".format(id_field, table_name)
        self.my_db.execute(__sql)
        __result = self.my_db.fetchone()
        if __result[0]:
            return __result[0] + 1
        else:
            return 1

    def query_action_id(self, attribute_value, id_field='action_id', table_name='test_action'):
        """
        查询表中最大ID
        :param attribute_value: 身份证号
        :param id_field:id对应的字段，默认为action_id
        :param table_name:查询的表名，默认为test_action
        :return:例：1
        """
        __sql = "select max({0}) from {1} where attribute_value={2}".format(id_field, table_name, attribute_value)
        self.my_db.execute(__sql)
        __result = self.my_db.fetchone()
        if __result[0]:
            return __result[0] + 1
        else:
            return 1

    def query_trans_id(self, attribute_value, id_field='trans_id', table_name='test_trans'):
        """
        查询表中最大ID
        :param attribute_value: 身份证号
        :param id_field:id对应的字段，默认为trans_id
        :param table_name:查询的表名，默认为test_trans
        :return:例：1
        """
        __sql = "select max({0}) from {1} where attribute_value={2}".format(id_field, table_name, attribute_value)
        self.my_db.execute(__sql)
        __result = self.my_db.fetchone()
        if __result[0]:
            return __result[0] + 1
        else:
            return 1

    def query_exist(self, field_value_1, field_value_2, table_name='test_attribute_info'):
        __sql = "select * from {0} where attribute_value='{1}' and type='{2}'" \
            .format(table_name, field_value_1, field_value_2)
        self.my_db.execute(__sql)
        __result = self.my_db.fetchall()
        return __result

    def close(self):
        self.my_db.close()


if __name__ == '__main__':
    cul = CommonUtil()
    # print oracle_connect(sql, 0)
    # print random_train_num()
    # print cul.md5_sth('fkpt@2017')
    # a = cul.stamp2time('-1', pattern='%Y-%m-%d')
    # print a
    # b = '2016/1/3'
    # b = cul.format_time(b)
    # print b
    # print a == b
    # print cul.excel_read('../Config/airplane.xlsx', 0)
    # print cul.word2pinyin('中国')
    # print cul.check_mobile_every('13866666666.')
    # path = 'D:\\wxt\\python-project\\fk\\Config\\wwe_dict'
    # a = cul.get_file_list(path, mode=1)
    # print a
    # file_name = a[0].split('\\')[-1].split('-')[0]
    # print file_name, type(file_name)
    # file_name_new = '{0}-{1}-{2}.nb'.format(file_name, cul.current_stamp(),cul.current_time(pattern='%Y%m%d-%H'))
    # file_path_new = '{0}\\{1}'.format(path, file_name_new)
    # print file_path_new
    # print cul.md5_sth('653226810815142,230109,513401')
    # os.rename(a[0], )
    # tdb = TestDb()
    # print tdb.query_id()
    # print tdb.query_action_id('650102731226301')
    # print cul.check_wz_one('650104198903070754')
    # print cul.query_source('2008')
    #
    # print cul.time2stamp('2018-01-17 00:00:00')
    # print cul.check_mobile_every('15389999974')
    # print cul.excel_read('..\\Config\\car_num.xls', sheet=0, col=0)
    # print cul.word2pinyin('臧秋秋')
    # print cul.get_birth_date('350504196105303658')
    # print cul.get_local_name()
    # print cul.get_local_ip()
    # a = cul.excel_read(file_path='../Config/table_fields.xls', col=7, start_rowx=2341, end_rowx=2370)
    # for __a in a:
    #     print __a
    # a = cul.get_row_by_str(xls_file='../Config/table_fields.xls', string='sh_mh_passenger_in_dz')
    # print a
    # print cul.get_area_by_credit('14103019370705607X')
    # print cul.md5_sth('513723198112035411\t01')
    print cul.date_list(beginDate='2018-03-01', endDate='2018-05-19')