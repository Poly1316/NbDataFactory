# -*- coding: utf-8 -*-
"""
@author wangxiaotao
Created on 2017-12-02
"FK业务库数据读取公共方法"
"""
import logging
from src.commonDao.oracledb import OracleDB
from src.commonDao.commonFunc import CommonUtil


class OracleDataRead(object):
    def __init__(self):
        self.cul = CommonUtil
        user_name = self.cul.get_config('hero_Oracle', 'Hero_username', '../Config/config.conf')
        pass_word = self.cul.get_config('hero_Oracle', 'Hero_password', '../Config/config.conf')
        url = self.cul.get_config('hero_Oracle', 'Hero_URL', '../Config/config.conf')
        self.db_link = self.cul.get_config('hero_Oracle', 'nbpf_dblink', '../Config/config.conf')
        self.ODB = OracleDB(user_name, pass_word, url)

    def get_rule_people(self):
        """
        获取attribute_info中所有符合规则人员的身份证号和object_id
        :return:返回列表类型，例:[('653223870703321', 420925, '30258', 2), ('650103520826402', 426464, '39228', 2)]
        """
        rule_sql = "select b.attribute_value,a.rule_id,a.rel_value, c.status from alarm_rule_rel a,attribute_info b," \
                   "alarm_rule_info c where b.object_id=a.rel_value and b.attribute_type='111' and c.id=a.rule_id"
        self.ODB.select_ora(rule_sql)
        attribute_object = self.ODB.out_all_ora()
        return attribute_object

    def get_attribute_people(self, num=None):
        """
        获取attribute_info中所有人员的身份证号和object_id
        :return:返回字典类型，例:{'652524740423151': 39846, '513401001101300': 44464}
        """
        if num is None:
            __sql = "select attribute_value,object_id from attribute_info where attribute_type='111'"
        else:
            __sql = "select T.attribute_value,T.object_id from attribute_info T where T.Attribute_Type='111' " \
                    "and T.attribute_value is not null and rownum<={0} order by T.object_id desc".format(num)
        self.ODB.select_ora(__sql)
        attribute_object = self.ODB.out_all_ora_dict()
        return attribute_object

    def get_other_attribute_people(self):
        """
        获取除身份证外的其他所有属性
        :return: 返回列表类型
        """
        __sql = "select attribute_value,object_id from attribute_info where attribute_type in " \
                "('FH11078','CO30002','335','414','116','B030303','513')"
        self.ODB.select_ora(__sql)
        attribute_object = self.ODB.out_all_ora_dict()
        return attribute_object

    def get_alarm_trans(self):
        """
        获取业务库alarm_trans表中身份证号和object_id
        :return:返回身份证号和object_id的字典
        """
        __sql = "select DISTINCT T.attribute_value,T.object_id from alarm_trans T"
        self.ODB.select_ora(__sql)
        attribute_trans = self.ODB.out_all_ora_dict()
        # __result = []
        # for line in attribute_trans:
        #     __result.append(line[0])
        return attribute_trans

    def get_alarm_action(self):
        """
        获取业务库alarm_action表中身份证号和object_id
        :return:返回身份证号和object_id的字典
        """
        __sql = "select DISTINCT T.attribute_value,T.object_id from alarm_action T"
        self.ODB.select_ora(__sql)
        __attribute_action = self.ODB.out_all_ora_dict()
        return __attribute_action

    def get_alarm_trans_time(self, attribute_value):
        """
        获取业务库alarm_trans身份证号对应的轨迹开始时间
        :param attribute_value: 身份证号
        :return:返回轨迹开始时间的列表
        """
        __sql = "select T.source_time from alarm_trans T where T.attribute_value='{0}'".format(attribute_value)
        self.ODB.select_ora(__sql)
        attribute_trans = self.ODB.out_all_ora()[1]
        __result = []
        for line in attribute_trans:
            __result.append(line[0])
        return __result

    def get_alarm_action_time(self, attribute_value, res_code):
        """
        获取业务库alarm_action表中身份证号对应的活动开始时间
        :param attribute_value: 身份证号
        :param res_code: 表对应的res_code
        :return: 返回活动开始时间列表
        """
        if len(attribute_value) != 15:
            return False, 'error attribute_value:{0}'.format(attribute_value)
        __sql = "select T.start_time from alarm_action T where T.attribute_value='{0}' and T.res_code='{1}'"\
            .format(attribute_value, res_code)
        self.ODB.select_ora(__sql)
        __attribute_action = self.ODB.out_all_ora()[1]
        __result = []
        for __line in __attribute_action:
            __result.append(__line[0])
        return __result

    def get_trans_create_time(self, attribute_value, source_time):
        """
        通过证件号码和轨迹开始时间获取数据创建时间
        :param attribute_value: 证件号码
        :param source_time: 轨迹开始时间
        :return: 返回创建时间，int型
        """
        __sql = "select T.create_time from alarm_trans T where T.attribute_value='{0}' " \
                "and T.source_time='{1}' order by T.create_time desc"\
            .format(attribute_value, source_time)
        self.ODB.select_ora(__sql)
        __attribute_create_time = self.ODB.out_one_ora()[1]
        if __attribute_create_time[0]:
            return int(__attribute_create_time[0])

    def get_all_car_no(self):
        """
        获取业务库所有车牌号码
        :return:返回车牌号码list
        """
        __sql = "select attribute_value from attribute_info T where T.ATTRIBUTE_TYPE='C030002'"
        self.ODB.select_ora(__sql)
        __car_no = self.ODB.out_all_ora()[1]
        __result = []
        for __car in __car_no:
            __result.append(__car[0])
        return str(__result).decode('string-escape')

    def get_action_car(self):
        """
        获取业务库alarm_action表车牌号码，返回list类型
        :return:
        """
        __sql = "select DISTINCT T.Attribute_Value from alarm_action T where T.Attribute_Type='C030002' " \
                "and T.Attribute_Value not like '%无%'"
        self.ODB.select_ora(__sql)
        __car_no = self.ODB.out_all_ora()[1]
        __result = []
        for __car in __car_no:
            __result.append(__car[0])
        return str(__result).decode('string-escape')

    def get_action_car_time(self, attribute_value):
        """
        通过车牌号码查询数据活动开始时间，返回活动开始时间列表
        :param attribute_value:
        :return:
        """
        __sql = "select T.start_time from alarm_action T where T.attribute_value='{0}' and attribute_type='C030002'"\
            .format(attribute_value)
        self.ODB.select_ora(__sql)
        __time = self.ODB.out_all_ora()[1]
        __result = []
        for __item in __time:
            __result.append(__item[0])
        return __result

    def get_action_create_time(self, attribute_value, source_time):
        """
        通过证件号码和活动开始时间获取数据创建时间
        :param attribute_value: 证件号码
        :param source_time: 轨迹开始时间
        :return: 返回创建时间，int型
        """
        __sql = "select T.create_time from alarm_action T where T.attribute_value='{0}' " \
                "and T.start_time='{1}' order by T.create_time desc"\
            .format(attribute_value, source_time)
        self.ODB.select_ora(__sql)
        __attribute_create_time = self.ODB.out_one_ora()[1]
        if __attribute_create_time[0]:
            return int(__attribute_create_time[0])

    def get_alarm_trans_city(self, attribute_value, time_stamp):
        """
        根据身份证号查询trans表中轨迹数据的出发城市和到达城市
        :param time_stamp: GP库时间戳字段
        :param attribute_value: 身份证号
        :return: 返回出发城市和到达城市的列表，如：[source_city, target_city]
        """
        __sql = "select T.Source_City,T.Target_City from alarm_trans T where T.ATTRIBUTE_VALUE='{0}' " \
                "and (source_time>{1} and source_time<{2})"\
            .format(attribute_value, time_stamp-86400, time_stamp+86400)
        self.ODB.select_ora(__sql)
        __trans_city = self.ODB.out_all_ora()[1]
        __result = []
        if len(__trans_city) == 1:
            return list(__trans_city[0])
        elif len(__trans_city) > 1:
            for __line in __trans_city:
                __result.append(__line[0])
                __result.append(__line[1])
            return __result
        else:
            return []

    def get_trans_rk(self, res_code, create_time, end_time):
        """
        通过res_code获取创建时间和省厅标准库入库时间字典
        :param end_time: 区间结束时间
        :param res_code:表对应的编码
        :param create_time:创建时间区间，取该时间之后的数据
        :return:
        """
        __sql = "select T.create_time,T.insert_time from alarm_trans T where T.res_code='{0}' " \
                "and (T.create_time>{1} and T.create_time<{2})"\
            .format(res_code, create_time, end_time)
        self.ODB.select_ora(__sql)
        __create_insert = self.ODB.out_all_ora_dict()
        if __create_insert:
            return __create_insert

    def get_action_rk(self, res_code, create_time, end_time):
        """
        通过res_code获取创建时间和省厅标准库入库时间字典
        :param end_time: 区间结束时间
        :param res_code:表对应的编码
        :param create_time:创建时间区间，取该时间之后的数据
        :return:
        """
        __sql = "select T.create_time,T.insert_time from alarm_action T where T.res_code='{0}' " \
                "and (T.create_time>{1} and T.create_time<{2})"\
            .format(res_code, create_time, end_time)
        self.ODB.select_ora(__sql)
        __create_insert = self.ODB.out_all_ora_dict()
        if __create_insert:
            return __create_insert

    def get_alarm_action_area(self, attribute_value, time_stamp):
        """
        根据身份证号查询action表中活动数据的活动城市
        :param attribute_value: 证件号码
        :param time_stamp: GP库活动开始时间时间戳
        :return: 返回出发城市和到达城市的列表，如：[area_id1, area_id2]
        """
        __sql = "select T.area_id from alarm_action T where T.ATTRIBUTE_VALUE='{0}' " \
                "and (start_time>{1} and start_time<{2})"\
            .format(attribute_value, time_stamp-86400, time_stamp+86400)
        self.ODB.select_ora(__sql)
        __action_area = self.ODB.out_all_ora()[1]
        __result = []
        if len(__action_area) == 1:
            return list(__action_area[0])
        elif len(__action_area) > 1:
            for __line in __action_area:
                __result.append(__line[0])
                # __result.append(__line[1])
            return __result
        else:
            return []

    def get_attribute_object(self, attribute_value):
        """
        通过attribute_value去属性表查询object_id
        :param attribute_value: 身份证号
        :return: object_id, <type 'int'>
        """
        __sql = "select T.object_id from attribute_info T where attribute_value='{0}' and attribute_type='111'"\
            .format(attribute_value)
        self.ODB.select_ora(__sql)
        attribute_object = self.ODB.out_one_ora()[1]
        if attribute_object:
            return attribute_object[0]
        else:
            return -1

    def get_rule(self, attribute_value):
        """
        通过身份证检验该人员在规则表中是否布控
        :param attribute_value: 身份证号
        :return: 返回规则内容
        """
        __sql = "select * from alarm_rule_info T1 where T1.ID in (select T2.rule_id from alarm_rule_rel T2 where " \
                "T2.rel_value=(select T3.object_id from attribute_info T3 where T3.attribute_value='{0}'))"\
            .format(attribute_value)
        self.ODB.select_ora(__sql)
        __result = self.ODB.out_one_ora()[1]
        if __result:
            return __result

    def get_all_rule(self):
        """
        查询业务库规则信息，返回业务库规则身份证号列表
        :return: 身份证号列表
        """
        __sql = "select T1.attribute_value from attribute_info T1 where object_id in (select T2.rel_value " \
                "from alarm_rule_rel T2 where T2.Rule_Id in (select T3.id from alarm_rule_info T3 where T3.status=2))" \
                " and T1.attribute_type='111'"
        self.ODB.select_ora(__sql)
        __result = self.ODB.out_all_ora()[1]
        if __result:
            __last_result = []
            for __line in __result:
                __last_result.append(__line[0])
            return __last_result

    def attribute_value_create_msg(self, attribute_value_tuple):
        """
        根据身份证号查询创建信息
        :param attribute_value_tuple: 身份证号元组或者list
        :return:[(15522, '654101770629241', '-1', 1464751014, 2004)]
        """
        if isinstance(attribute_value_tuple, list):
            attribute_value_tuple = tuple(attribute_value_tuple)
        else:
            pass

        if attribute_value_tuple is None:
            return False
        elif len(attribute_value_tuple) == 1:
            attribute_value_tuple = "('{0}')".format(attribute_value_tuple[0])
        else:
            pass

        __sql = "select T1.Object_Id,T1.ATTRIBUTE_VALUE,T2.Create_Userid,T2.CREATE_TIME,T2.SOURCE_ID " \
                "from attribute_info T1,object_info T2 where T1.attribute_type='111' and T1.attribute_value " \
                "in {0} and T1.Object_Id=T2.Object_Id".format(attribute_value_tuple)
        logging.debug(u'身份证创建用户信息查询SQL为：{0}'.format(__sql))
        self.ODB.select_ora(__sql)
        create_msg = self.ODB.out_all_ora()
        if create_msg[1] and create_msg[0]:
            return create_msg[1]

    def query_user(self, user_id):
        """
        根据用户id查询用户信息
        :param user_id: 用户id
        :return: 返回用户信息列表
        """
        user_sql = "select T.USERNAME,T.REALNAME from nb_user@{1} T where id ='{0}'".format(user_id, self.db_link)
        self.ODB.select_ora(user_sql)
        user_result = self.ODB.out_all_ora()[1]
        if user_result:
            return list(user_result[0])
        else:
            return [user_id, user_id]

    def query_attribute_by_num(self, num=100):
        """
        获取指定数目的attribute_type为111的人员属性信息
        :param num: 需要获取的数目
        :return:
        """
        __sql = "select * from attribute_info T where T.Attribute_Type='111' and T.attribute_value is not null " \
                "and rownum<={0} order by T.object_id desc".format(num)
        self.ODB.select_ora(__sql)
        __result = self.ODB.out_all_ora()[1]
        return __result

    def do_sql(self, sql):
        """
        执行sql语句
        :param sql:str或者list类型
        :return:
        """
        if isinstance(sql, str):
            sql = [sql]
        if isinstance(sql, list):
            pass
        else:
            return

        for __sql in sql:
            self.ODB.select_ora(__sql)
            self.ODB.commit()

    def close(self):
        self.ODB.close_ora()


def test():
    """
    测试函数
    :return:
    """
    ODR = OracleDataRead()
    try:
        # all = ODR.get_rule_people()
        # other_attribute = ODR.get_other_attribute_people()
        # print all
        # print other_attribute
        __result = ODR.get_attribute_people(num=100)
        # __result_1 = ODR.get_rule('654101770629241')
        print __result.keys()
        # print type(__result)
        # print __result.has_key('654101770629241')
        # print __result_1
        # a = ['654101770629241']
        # print ODR.attribute_value_create_msg(a)
        # print ODR.get_all_rule()
        # a = random.sample(all, 10)
        # print ODR.get_alarm_trans_city('652829960105079', 1515498000)
        # print a, type(a)
        # print ODR.get_alarm_action().keys()
        # print a[1], type(a[1])
        # print ODR.get_alarm_action_area('653101660601097', 1513163220)
        # print ODR.get_trans_create_time('650121001213371', '1501033971')
        # print ODR.get_all_car_no()
        # print ODR.query_attribute_by_num(10)
    finally:
        ODR.close()

if __name__ == '__main__':
    test()
