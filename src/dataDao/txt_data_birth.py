# -*- coding: utf-8 -*-
"""
@author wangxiaotao
@version 0.0.3
created on 2018-02-28
"txt文件类型数据自动生成脚本，通过配置文件驱动"
"""
import logging.config

import gc

from src.commonDao.commonFunc import CommonUtil
from src.commonDao.readxml import ReadXml
from src.dataDao.Oracle_Data_Read import OracleDataRead

from src.dataDao.Randconstants import RandomConst


class TxtBirth(object):
    def __init__(self, xml_path='../Config/data_task.xml'):
        """
        初始化函数
        :param xml_path:xml配置文件路径，默认为../Config/data_task.xml
        """
        self.cul = CommonUtil()
        self.rc = RandomConst()
        try:
            self.odr = OracleDataRead()
        except Exception as ex:
            logging.warning('no oracle connect,{0}'.format(ex))
        self.file = xml_path
        self.credit_list = []
        self.area_code = []

    def mapping_func(self, seq_list, line):
        """
        函数与配置文件参数一一对应，通过传特定参数，调用不同的造数据方法返回不同类型数据
        :param seq: 与数据类型对应的序列
        :return: 返回数据
        """
        # global credit
        map_list = []
        for seq in seq_list:
            if int(seq[1]) == 1:    # 随机生成身份证号码，自定义位数
                credit = self.rc.random_credit_id(digit=seq[2], num=line,area=seq[3], start=seq[4], end=seq[5])
                # __birth_date = self.cul.get_birth_date(self.credit)
                # __sex = self.cul.get_sex(self.credit)
                # self.credit_list.append(__birth_date)
                # self.credit_list.append(__sex)
                self.credit_list = [__credit for __credit in credit]
                # self.credit_list = [__credit for __credit in range(10000)]
                map_list.append(self.credit_list)
            elif int(seq[1]) == 0:  # 0对应空值
                map_list.append([''] * int(line))
            elif int(seq[1]) == 2:  # 生成随机用户姓名
                map_list.append(self.rc.random_username(path=seq[2], num=line))
            elif int(seq[1]) == 3:  # 生成整形随机数，自定义范围
                map_list.append(self.rc.random_num(start=int(seq[2]), end=int(seq[3]), num=line))
            elif int(seq[1]) == 4:  # 4对应随机生成航班号函数
                map_list.append(self.rc.random_airplane_num(num=line))
            elif int(seq[1]) == 5:  # 5对应随机生成日期-时间函数，random_date_time
                map_list.append(self.rc.random_date_time(pattern=seq[2], time_second=int(seq[3]),
                                                         time_pro=int(seq[4]), num=line))
            elif int(seq[1]) == 6:  # 6对应机场三字码函数，random_airplane_port
                map_list.append(self.rc.random_airplane_port(num=line))
            elif int(seq[1]) == 7:  # 7对应随机生成字符串函数，random_string
                map_list.append(self.rc.random_string(low_case=seq[2], digits_num=seq[3], all_num=int(seq[4]), num=line))
            elif int(seq[1]) == 8:  # 8对应性别，random_sex
                if self.credit_list:
                    map_list.append([self.cul.get_sex(__credit) for __credit in self.credit_list])
                else:
                    map_list.append([self.rc.random_sex() for __i in range(0, line)])
            elif int(seq[1]) == 9:  # 9对应手机号码，random_phone
                map_list.append(self.rc.random_phone(num=line))
            elif int(seq[1]) == 10: # 10对应指定值
                map_list.append([seq[2]] * int(line))
            elif int(seq[1]) == 11: # 11对应民族
                map_list.append(self.rc.random_nation(num=line))
            elif int(seq[1]) == 12: # 12对应邮箱
                map_list.append(self.rc.random_email(num=line))
            elif int(seq[1]) == 13: # 13对应IMSI
                map_list.append(self.rc.random_imsi(num=line))
            elif int(seq[1]) == 14: # 14对应MAC地址
                map_list.append(self.rc.random_mac(number=line))
            elif int(seq[1]) == 15: # 15对应IMEI
                map_list.append(self.rc.random_imei(num=line))
            elif int(seq[1]) == 16: # 16对应address
                map_list.append(self.rc.random_address(num=line))
            elif int(seq[1]) == 17: # 17对应IP地址
                map_list.append(self.rc.random_ip(num=line))
            elif int(seq[1]) == 18: # 18对应网站域名
                map_list.append(self.rc.random_website(num=line))
            elif int(seq[1]) == 19: # 19对应业务库身份证号码
                if int(seq[2]) == 18:
                    map_list.append(self.odr.get_attribute_people(num=line))
                else:
                    map_list.append([self.cul.new2old(__credit_hero) for __credit_hero
                                     in self.odr.get_attribute_people(num=line)])
            elif int(seq[1]) == 20: # 20对应火车车次
                map_list.append(self.rc.random_train_num(num=line))
            elif int(seq[1]) == 21: # 21对应区域名称
                __area = self.rc.random_area_code(return_type=1, num=line)
                # self.area_code_1 = [__area_code[0] for __area_code in __area]
                # print self.area_code_1, 'line 112'
                # self.area_code_2 = [__area_code[1] for __area_code in __area]
                # print self.area_code_2, 'line 114'
                # self.area_code.append(self.area_code_1)
                # self.area_code.append(self.area_code_2)
                self.area_code = zip(*[__area_code for __area_code in __area])
                map_list.append(self.area_code[0])
            elif int(seq[1]) == 22: # 22对应区域编码
                if self.area_code:
                    map_list.append(self.area_code[1])
                else:
                    area_list = [__area[1] for __area in self.rc.random_area_code(return_type=1, num=line)]
                    map_list.append(area_list)
        return map_list

    def update_data_xml(self, table_name=None, file_path ='../Config/table_fields.xls', start=None, end=None):
        """
        根据表结构文档中数据类型，生成xml配置文件
        :param table_name:表名，如果表名为None，则默认读取配置文件中table_name字段
        :param file_path:表结构文档所在路径，默认为../Config/table_fields.xls
        :param start:
        :param end:
        :return:
        """
        __col = self.cul.get_config('data_platform', 'config_col', '../Config/config.conf')
        if start is None:
            start = self.cul.get_config('data_platform', 'start_row', '../Config/config.conf')
        if end is None:
            end = self.cul.get_config('data_platform', 'end_row', '../Config/config.conf')
        if table_name is None:
            table_name = self.cul.get_config('data_platform', 'table_name', '../Config/config.conf')
        __field_col = self.cul.get_config('data_platform', 'field_col', '../Config/config.conf')
        field_list = self.cul.excel_read(file_path, col=int(__col) - 1,
                                         start_rowx=int(start) - 1, end_rowx=int(end))
        # __table_name_list = self.cul.excel_read(file_path, col=int(table_name) - 1,
        #                                         start_rowx=int(start) - 1, end_rowx=int(end))
        __field_name_list = self.cul.excel_read(file_path, col=int(__field_col) - 1,
                                                start_rowx=int(start) - 1, end_rowx=int(end))

        # 随机整数,航班号,日期时间,机场三字码,姓名,字符串,身份证号码,空值,随机性别,手机号码
        rx = ReadXml(self.file)
        root = rx.get_root()

        # 2. 属性修改
        # A. 找到父节点
        nodes = rx.find_nodes("tables")[0]

        __i = 0
        for __field in field_list:
            # table_name = __table_name_list[__i]
            field_name = __field_name_list[__i]
            __i += 1
            __nodes = rx.find_nodes("field", fa=nodes)
            # 判断当前表在xml配置文件中是否存在
            if rx.get_node_by_keyvalue(__nodes, {"name": table_name, "field": field_name}):
                logging.warning('table_field [{0}] already exists!!!'.format(__field))
                continue
            if __field == u'随机整数':
                # A.新建节点
                __field = rx.create_node("field", {"name": table_name, "field": field_name, "type": u"随机整数", "id": str(__i)}, "")
                # B.插入到父节点之下
                rx.add_child_node(root, __field)
                __nodes = rx.find_nodes("field", fa=nodes)
                __tab = rx.get_node_by_keyvalue(__nodes, {"id": str(__i), "name": table_name})
                __child1 = rx.create_node("seq", {}, "3")
                rx.add_child_node(__tab, __child1)
                __child2 = rx.create_node("start", {}, "1000000")
                rx.add_child_node(__tab, __child2)
                __child3 = rx.create_node("end", {}, "99999999")
                rx.add_child_node(__tab, __child3)
            elif __field == u'航班号':
                __field = rx.create_node('field', {"name": table_name, "field": field_name, "type": u"航班号", "id": str(__i)}, '')
                rx.add_child_node(root, __field)
                __nodes = rx.find_nodes("field", fa=nodes)
                __tab = rx.get_node_by_keyvalue(__nodes, {"id": str(__i), "name": table_name})
                __child1 = rx.create_node("seq", {}, '4')
                rx.add_child_node(__tab, __child1)
            elif __field == u'日期时间':
                __field = rx.create_node('field', {"name": table_name, "field": field_name, "type": u"日期时间", "id": str(__i)}, '')
                rx.add_child_node(root, __field)
                __nodes = rx.find_nodes("field", fa=nodes)
                __tab = rx.get_node_by_keyvalue(__nodes, {"id": str(__i), "name": table_name})
                __child1 = rx.create_node("seq", {}, '5')
                rx.add_child_node(__tab, __child1)
                __child2 = rx.create_node("pattern", {}, '%Y-%m-%d %H:%M:%S')
                rx.add_child_node(__tab, __child2)
                __child3 = rx.create_node("time_second", {}, '1800')
                rx.add_child_node(__tab, __child3)
                __child3 = rx.create_node("time_pro", {}, '0')
                rx.add_child_node(__tab, __child3)
            elif __field == u'机场三字码':
                __field = rx.create_node('field', {"name": table_name, "field": field_name, "type": u"机场三字码", "id": str(__i)}, '')
                rx.add_child_node(root, __field)
                __nodes = rx.find_nodes("field", fa=nodes)
                __tab = rx.get_node_by_keyvalue(__nodes, {"id": str(__i), "name": table_name})
                __child1 = rx.create_node("seq", {}, '6')
                rx.add_child_node(__tab, __child1)
            elif __field == u'姓名':
                __field = rx.create_node('field', {"name": table_name, "field": field_name, "type": u"姓名", "id": str(__i)}, '')
                rx.add_child_node(root, __field)
                __nodes = rx.find_nodes("field", fa=nodes)
                __tab = rx.get_node_by_keyvalue(__nodes, {"id": str(__i), "name": table_name})
                __child1 = rx.create_node("seq", {}, '2')
                rx.add_child_node(__tab, __child1)
                __child2 = rx.create_node("path", {}, '../Config/Const.conf')
                rx.add_child_node(__tab, __child2)
            elif __field == u'字符串':
                __field = rx.create_node('field', {"name": table_name, "field": field_name, "type": u"字符串", "id": str(__i)}, '')
                rx.add_child_node(root, __field)
                __nodes = rx.find_nodes("field", fa=nodes)
                __tab = rx.get_node_by_keyvalue(__nodes, {"id": str(__i), "name": table_name})
                __child1 = rx.create_node("seq", {}, '7')
                rx.add_child_node(__tab, __child1)
                __child2 = rx.create_node("lower_case", {}, '0')
                rx.add_child_node(__tab, __child2)
                __child3 = rx.create_node("digits_num", {}, '0')
                rx.add_child_node(__tab, __child3)
                __child4 = rx.create_node("case_num", {}, '6')
                rx.add_child_node(__tab, __child4)
            elif __field == u'身份证号码':
                __field = rx.create_node('field', {"name": table_name, "field": field_name, "type": u"身份证号码", "id": str(__i)}, '')
                rx.add_child_node(root, __field)
                __nodes = rx.find_nodes("field", fa=nodes)
                __tab = rx.get_node_by_keyvalue(__nodes, {"id": str(__i), "name": table_name})
                __child1 = rx.create_node("seq", {}, '1')
                rx.add_child_node(__tab, __child1)
                __child2 = rx.create_node("digit", {}, '18')
                rx.add_child_node(__tab, __child2)
                __child3 = rx.create_node("front-2", {}, 'None')
                rx.add_child_node(__tab, __child3)
                __child4 = rx.create_node("year-start", {}, '1960-01-01')
                rx.add_child_node(__tab, __child4)
                __child5 = rx.create_node("year-end", {}, '2016-12-30')
                rx.add_child_node(__tab, __child5)
            elif __field == u'空值':
                __field = rx.create_node('field', {"name": table_name, "field": field_name, "type": u"空值", "id": str(__i)}, '')
                rx.add_child_node(root, __field)
                __nodes = rx.find_nodes("field", fa=nodes)
                __tab = rx.get_node_by_keyvalue(__nodes, {"id": str(__i), "name": table_name})
                __child1 = rx.create_node("seq", {}, '0')
                rx.add_child_node(__tab, __child1)
            elif __field == u'随机性别':
                __field = rx.create_node('field', {"name": table_name, "field": field_name, "type": u"随机性别", "id": str(__i)}, '')
                rx.add_child_node(root, __field)
                __nodes = rx.find_nodes("field", fa=nodes)
                __tab = rx.get_node_by_keyvalue(__nodes, {"id": str(__i), "name": table_name})
                __child1 = rx.create_node("seq", {}, '8')
                rx.add_child_node(__tab, __child1)
            elif __field == u'手机号码':
                __field = rx.create_node('field', {"name": table_name, "field": field_name, "type": u"手机号码", "id": str(__i)}, '')
                rx.add_child_node(root, __field)
                __nodes = rx.find_nodes("field", fa=nodes)
                __tab = rx.get_node_by_keyvalue(__nodes, {"id": str(__i), "name": table_name})
                __child1 = rx.create_node("seq", {}, '9')
                rx.add_child_node(__tab, __child1)
            elif __field == u'指定值':
                __field = rx.create_node('field', {"name": table_name, "field": field_name, "type": u"指定值", "id": str(__i)}, '')
                rx.add_child_node(root, __field)
                __nodes = rx.find_nodes("field", fa=nodes)
                __tab = rx.get_node_by_keyvalue(__nodes, {"id": str(__i), "name": table_name})
                __child1 = rx.create_node("seq", {}, '10')
                rx.add_child_node(__tab, __child1)
                __child2 = rx.create_node("value", {}, '0')
                rx.add_child_node(__tab, __child2)
            elif __field == u'民族':
                __field = rx.create_node('field', {"name": table_name, "field": field_name, "type": u"民族", "id": str(__i)}, '')
                rx.add_child_node(root, __field)
                __nodes = rx.find_nodes("field", fa=nodes)
                __tab = rx.get_node_by_keyvalue(__nodes, {"id": str(__i), "name": table_name})
                __child1 = rx.create_node("seq", {}, '11')
                rx.add_child_node(__tab, __child1)
            elif __field == u'邮箱':
                __field = rx.create_node('field', {"name": table_name, "field": field_name, "type": u"邮箱", "id": str(__i)}, '')
                rx.add_child_node(root, __field)
                __nodes = rx.find_nodes("field", fa=nodes)
                __tab = rx.get_node_by_keyvalue(__nodes, {"id": str(__i), "name": table_name})
                __child1 = rx.create_node("seq", {}, '12')
                rx.add_child_node(__tab, __child1)
            elif __field == u'IMSI':
                __field = rx.create_node('field', {"name": table_name, "field": field_name, "type": u"IMSI", "id": str(__i)}, '')
                rx.add_child_node(root, __field)
                __nodes = rx.find_nodes("field", fa=nodes)
                __tab = rx.get_node_by_keyvalue(__nodes, {"id": str(__i), "name": table_name})
                __child1 = rx.create_node("seq", {}, '13')
                rx.add_child_node(__tab, __child1)
            elif __field == u'MAC地址':
                __field = rx.create_node('field', {"name": table_name, "field": field_name, "type": u"MAC地址", "id": str(__i)}, '')
                rx.add_child_node(root, __field)
                __nodes = rx.find_nodes("field", fa=nodes)
                __tab = rx.get_node_by_keyvalue(__nodes, {"id": str(__i), "name": table_name})
                __child1 = rx.create_node("seq", {}, '14')
                rx.add_child_node(__tab, __child1)
            elif __field == u'IMEI':
                __field = rx.create_node('field', {"name": table_name, "field": field_name, "type": u"IMEI", "id": str(__i)}, '')
                rx.add_child_node(root, __field)
                __nodes = rx.find_nodes("field", fa=nodes)
                __tab = rx.get_node_by_keyvalue(__nodes, {"id": str(__i), "name": table_name})
                __child1 = rx.create_node("seq", {}, '15')
                rx.add_child_node(__tab, __child1)
            elif __field == u'随机地址':
                __field = rx.create_node('field', {"name": table_name, "field": field_name, "type": u"随机地址", "id": str(__i)}, '')
                rx.add_child_node(root, __field)
                __nodes = rx.find_nodes("field", fa=nodes)
                __tab = rx.get_node_by_keyvalue(__nodes, {"id": str(__i), "name": table_name})
                __child1 = rx.create_node("seq", {}, '16')
                rx.add_child_node(__tab, __child1)
            elif __field == u'IP地址':
                __field = rx.create_node('field', {"name": table_name, "field": field_name, "type": u"IP地址", "id": str(__i)}, '')
                rx.add_child_node(root, __field)
                __nodes = rx.find_nodes("field", fa=nodes)
                __tab = rx.get_node_by_keyvalue(__nodes, {"id": str(__i), "name": table_name})
                __child1 = rx.create_node("seq", {}, '17')
                rx.add_child_node(__tab, __child1)
            elif __field == u'网站域名':
                __field = rx.create_node('field', {"name": table_name, "field": field_name, "type": u"IP地址", "id": str(__i)}, '')
                rx.add_child_node(root, __field)
                __nodes = rx.find_nodes("field", fa=nodes)
                __tab = rx.get_node_by_keyvalue(__nodes, {"id": str(__i), "name": table_name})
                __child1 = rx.create_node("seq", {}, '18')
                rx.add_child_node(__tab, __child1)
            elif __field == u'业务库身份证':
                __field = rx.create_node('field', {"name": table_name, "field": field_name, "type": u"业务库身份证", "id": str(__i)}, '')
                rx.add_child_node(root, __field)
                __nodes = rx.find_nodes("field", fa=nodes)
                __tab = rx.get_node_by_keyvalue(__nodes, {"id": str(__i), "name": table_name})
                __child1 = rx.create_node("seq", {}, '19')
                rx.add_child_node(__tab, __child1)
                __child2 = rx.create_node("digit", {}, '18')
                rx.add_child_node(__tab, __child2)
            elif __field == u'火车车次':
                __field = rx.create_node('field', {"name": table_name, "field": field_name, "type": u"火车车次", "id": str(__i)}, '')
                rx.add_child_node(root, __field)
                __nodes = rx.find_nodes("field", fa=nodes)
                __tab = rx.get_node_by_keyvalue(__nodes, {"id": str(__i), "name": table_name})
                __child1 = rx.create_node("seq", {}, '20')
                rx.add_child_node(__tab, __child1)
            elif __field == u'区域编码':
                __field = rx.create_node('field', {"name": table_name, "field": field_name, "type": u"区域编码", "id": str(__i)}, '')
                rx.add_child_node(root, __field)
                __nodes = rx.find_nodes("field", fa=nodes)
                __tab = rx.get_node_by_keyvalue(__nodes, {"id": str(__i), "name": table_name})
                __child1 = rx.create_node("seq", {}, '21')
                rx.add_child_node(__tab, __child1)
            elif __field == u'区域编码-地名':
                __field = rx.create_node('field', {"name": table_name, "field": field_name, "type": u"区域编码-地名", "id": str(__i)}, '')
                rx.add_child_node(root, __field)
                __nodes = rx.find_nodes("field", fa=nodes)
                __tab = rx.get_node_by_keyvalue(__nodes, {"id": str(__i), "name": table_name})
                __child1 = rx.create_node("seq", {}, '22')
                rx.add_child_node(__tab, __child1)

            rx.write_xml(self.file)

        self.cul.prettyXml(root, '\t', '\n')    # 美化生成的xml文件
        rx.write_xml(self.file)

    def txt_birth(self, table_name, path='../fileDao/test_file/', format='.nb', line=10, field_num=0,
                  xml_path="../Config/data_task.xml", file_path='../Config/table_fields.xls', field_split='\t',
                  line_split='\n'):
        """
        写表文本文件方法，通过xml控制表结构
        :param line_split: 文件字段分隔符，默认为\t
        :param field_split: 文件行分隔符，默认为\n‘
        :param file_path:表字段excel路径，支持相对路径
        :param xml_path:xml配置文件路径，支持相对路径
        :param table_name: 要添加的表名， list类型或者str类型均可，如：'sh_mh_passenger_in_dz'或者['sh_mh_passenger_in_dz']
        :param format:要生成的文件格式，如'.txt','.nb'等
        :param path:文件存储路径，默认为'../fileDao/test_file/'
        :param line:文件行数
        :param field_num:xml中表结构对应的fields序列号
        :return:None
        """
        rx = ReadXml(xml_path)
        table_list = []
        if isinstance(table_name, str):
            table_list.append(table_name)
        elif isinstance(table_name, list):
            table_list = table_name
        else:
            pass
        gc.disable()
        for _table_name in table_list:
            seq_list = []
            # 通过表名判断该表结构信息是否在xml中已配置，如果没有配置，会先执行update_data_xml ；
            _nodes = rx.find_nodes("tables")[field_num]
            if rx.get_node_by_keyvalue(_nodes, {"name": _table_name}):
                logging.warning('table [{}] already exists!!!'.format(_table_name))
            else:
                try:
                    _row = self.cul.get_row_by_str(file_path, string=_table_name, row=1)
                except Exception as ex:
                    logging.error(u'表关键词所在列号获取失败，请注意检查表名配置是否正确，{0}'.format(ex))
                    break
                logging.info(u'【{0}】在xml中的配置不存在，查找到excel表中对应的该表起始位置和结束为止分别为：{1}'
                             .format(_table_name, _row))
                self.update_data_xml(table_name=_table_name, file_path=file_path, start=_row[0], end=_row[1])
                rx = ReadXml(xml_path)
                __nodes = rx.find_nodes("tables")[field_num]

            # 拼接文件名称和路径，目前使用表名加后缀的方式
            _all_path = '{0}{1}_{2}{3}'.format(path, _table_name, self.cul.current_time(pattern='%Y%m%d%H%M%S'), format)
            _fields = rx.get_node_by_keyvalue(_nodes, {"name": _table_name})
            _i = 1
            with open(_all_path, 'wb') as txt_reader:
                if format == '.nb' or format=='.txt':
                    for _field in _fields:
                        _seq = []
                        for _element in _field.iter():
                            _seq.append(_element.text.strip())
                        seq_list.append(_seq)
                    for _list in zip(*self.mapping_func(seq_list=seq_list, line=line)):
                        _list = [str(_txt) for _txt in _list]
                        _content = '{0}'.format(field_split).join(_list) + '{0}'.format(line_split)
                        txt_reader.write(_content)
                        logging.info(u'第{0}行{1}写入完成!'.format(_i, _content))
                        _i += 1
                elif format == '.sql':
                    for _field in _fields:
                        _seq = []
                        for _element in _field.iter():
                            _seq.append(_element.text.strip())
                        seq_list.append(_seq)
                    for _list in zip(*self.mapping_func(seq_list=seq_list, line=line)):
                        _list = ['"{0}"'.format(str(_txt)) for _txt in _list]
                        _content = 'insert into {0} values'.format(_table_name) + '(' + "{0}".format(field_split).join(_list) + ');' + '{0}'.format(line_split)
                        txt_reader.write(_content)
                        logging.info(u'第{0}行{1}写入完成!'.format(_i, _content))
                        _i += 1
            del seq_list[:]
        gc.enable()

    def run(self ):
        """
        运行主函数
        :return:None
        """
        line = self.cul.get_config('data_platform', 'txt_line', file_path='../Config/config.conf')
        table_name = self.cul.get_config('data_platform', 'table_name', file_path='../Config/config.conf')
        __format = self.cul.get_config('data_platform', 'format', file_path='../Config/config.conf')
        __field_split = self.cul.get_config('data_platform', 'field_split', file_path='../Config/config.conf')
        if __field_split == '' or __field_split == '\t':
            __field_split_n = '\t'
        else:
            __field_split_n = __field_split
        __excel_path = self.cul.get_config('data_platform', 'excel_path', file_path='../Config/config.conf')
        # 读取配置文件，判断是否存在逗号，若存在，则table_name转为列表类型
        if ',' in table_name:
            table_name = table_name.split(',')
        self.txt_birth(line=int(line), table_name=table_name, format=__format, field_split=__field_split_n,
                       file_path=__excel_path)

if __name__ == '__main__':
    tb = TxtBirth(xml_path='../Config/data_task.xml')
    tb.run()