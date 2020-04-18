# -*- coding: utf-8 -*-
"""
@author wangxiaotao
@version 0.0.3
created on 2017-7-5
"随机生成用户姓名、手机号码、用户邮箱等数据"
"""
import os
import random
import socket
import string
import struct
import time
from random import choice

from src.commonDao.commonFunc import CommonUtil

import Random_CreditID
from addr import addr


class RandomConst(object):
    def __init__(self):
        self.cul = CommonUtil()

    @staticmethod
    def __random_name(size=1, chars=string.ascii_letters + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    def __first_name(self, size=2, ln=None, fn=None):
        _lst = []
        for i in range(size):
            _item = self.__random_name(1, fn)
            if ln:
                while _item in ln:
                    _item = self.__random_name(1, fn)
                _lst.append(_item)
            else:
                _lst.append(_item)
        return "".join(_lst)

    def random_username(self, num=1, path='../Config/Const.conf'):
        """
        随机生成用户姓名
        调用方法
        例1：
        for i in random_username(num=1000):
            print i
        :param num: 迭代的次数
        :param path: 配置文件地址
        :return:
        """
        if os.path.exists(path):
            pass
        else:
            yield
        lns = list(eval(self.cul.get_config('attribute_conf', 'hundred_Family_name', path)))
        fns = list(eval(self.cul.get_config('attribute_conf', 'commonUse_Chinese', path)))
        __i = 1
        while __i <= num:
            _last = self.__random_name(1, lns)
            __i += 1
            yield "{}{}".format(_last, self.__first_name(random.randint(1, 2), _last, fns))

    def random_phone(self, num=1, path='../Config/Const.conf'):
        """
        随机生成手机号码
        :param num: 迭代的次数
        :param path: 配置文件地址，默认为'../Config/Const.conf'
        :return:
        """
        __i = 1
        area_num = list(eval(self.cul.get_config('attribute_conf', 'area_Phone_num', path)))
        # area_number = choice(area_num)
        seed = "1234567890"

        # last_eight_number = ''.join(sa)
        while __i <= num:
            __i += 1
            # sa = []
            # for i in range(8):
            #     sa.append(choice(seed))
            sa = [choice(seed) for __a in range(8)]
            yield '{0}{1}'.format(choice(area_num), ''.join(sa))

    @staticmethod
    def random_user_code():
        """
        随机生成用户编号
        :return:
        """
        user_code = random.randint(99999, 100000000)
        return user_code

    def random_email(self, num=1, path='../Config/Const.conf'):
        """
        随机生成邮箱
        :param path: 配置文件地址，默认为'../Config/Const.conf'
        :return:
        """
        __str_email = self.random_string(num=num, low_case=True, all_num=random.randint(6, 20))
        __common_email = list(eval(self.cul.get_config('attribute_conf', 'commonUse_email', path)))
        # i_email = random.randint(8, 20)
        # __email_1 = random.sample(__str_email, i_email)
        # __email_2 = random.sample(__common_email, 1)
        __i = 1
        while __i <= num:
            yield '{0}{1}'.format(__str_email.next(), choice(__common_email))
            __i += 1

    def random_chinese(self, chinese_num=2, path='../Config/Const.conf'):
        """
        随机生成中文汉字，数目自定义
        :param path:
        :param chinese_num: 中文汉字数目，默认为2
        :param path: 配置文件地址，默认为'../Config/Const.conf'
        :return: 如：'史选怎灯顺'
        """
        # AllChinese = "".join(map(unichr, xrange(0x4e00, 0x9fa6)))
        # __useful_chinese = Constants.Const.commonUse_Chinese
        __useful_chinese = list(eval(self.cul.get_config('attribute_conf', 'commonUse_Chinese', path)))
        # # return random.sample(AllChinese, chinese_num)
        # __random_chinese = "".join(random.sample(AllChinese, chinese_num_1))
        __random_chinese = random.sample(__useful_chinese, chinese_num)
        yield "".join(__random_chinese)

    @staticmethod
    def random_chinese_complex(num):
        """
        生成指定个数汉字，负责类型
        :param num: 需要生成的汉字个数，int类型
        :return:
        """
        __all_chinese = "".join(map(unichr, xrange(0x4e00, 0x9fa6)))
        yield "".join(random.sample(__all_chinese, num))

    # @staticmethod
    # def random_chinese_complex(chinese_num=2):
    #     """
    #     随机生成中文汉字，数目自定义，此方法为全部2万汉字字库，使用请慎重！因为大部分汉字你都不认识
    #     :param chinese_num:中文汉字数目，默认为2
    #     :return:
    #     """
    #     # AllChinese = "".join(map(unichr, xrange(0x4e00, 0x9fa6)))
    #     UsefulChinese = Constants.Const.commonUse_Chinese
    #     AllCase = '%s%s%s' % (Constants.Const.commonUse_english, UsefulChinese, Constants.Const.commonUse_mark)
    #     # return random.sample(AllChinese, chinese_num)
    #     RandomNotice_html = "".join(random.sample(AllCase, chinese_num))
    #     yield RandomNotice_html

    @staticmethod
    def random_qq():
        """随机生成QQ号码"""
        return random.randint(100000, 9999999999)

    @staticmethod
    def random_passport(num=1):
        first = ['G', 'P', 'S', 'D']
        __seed = '12345678'
        __i = 1
        while __i <= num:
            __i += 1
            __sa = [choice(__seed) for __a in range(8)]
            yield '{0}{1}'.format(choice(first), ''.join(__sa))

    @staticmethod
    def random_GA_passport(num=1):
        """
        港澳通行证
        :return:
        """
        first = 'GA'
        __i = 1
        __seed = '12345678'
        while __i <= num:
            __i += 1
            __sa = [choice(__seed) for __a in range(8)]
            yield '{0}{1}'.format(first, ''.join(__sa))

    @staticmethod
    def random_TW_passport(num=1):
        """
        台湾通行证
        :return:
        """
        first = 'TW'
        __i = 1
        __seed = '12345678'
        while __i <= num:
            __i += 1
            __sa = [choice(__seed) for __a in range(8)]
            yield '{0}{1}'.format(first, ''.join(__sa))

    @staticmethod
    def credit_id(num=1):
        """
        随机生成18为身份证号码
        :param num: 迭代次数，即生成的身份证号码的个数
        :return: 返回18为身份证迭代对象，调用方法为credit_id().next()
        """
        __i = 1
        while __i <= num:
            __i += 1
            yield Random_CreditID.getRandomIdNumber()

    @staticmethod
    def random_date_time(num=1, pattern='%Y/%m/%d', time_second=0, time_pro=0):
        """
        根据格式化字符串'%Y/%m/%d'生成随机日期或者时间
        :param time_pro: 不同模式供选择，0：当前时间加上一个随机秒数后再加上time_second；1：当前时间加上time_second;
                        2:减去随机秒数后再加上time_second
        :param num: 迭代次数，即需要生成的数据的个数
        :param pattern: 格式化字符串，如:'%Y/%m/%d'或者'%H%M'
        :param time_second:可选择增加秒数, 必须为int类型，可以为负数
        :return:
        """
        __i = 1
        while __i <= num:
            __i += 1
            if time_pro == 0:
                yield time.strftime(pattern,
                                    time.localtime(float(int(time.time()) + random.randint(3600, 360000) + time_second)))
            elif time_pro == 1:
                yield time.strftime(pattern, time.localtime(float(int(time.time()) + time_second)))
            elif time_pro == 2:
                yield time.strftime(pattern,
                                    time.localtime(float(int(time.time()) - random.randint(3600, 360000) + time_second)))
            elif time_pro == 3:
                yield int(time.time())

    @staticmethod
    def random_date_time_pro(num=1, pattern='%Y/%m/%d', time_second=0):
        """
        根据格式化字符串'%Y/%m/%d'生成随机日期或者时间
        :param num: 迭代次数
        :param pattern: 格式化字符串，如:'%Y/%m/%d'或者'%H%M'
        :param time_second:可选择增加秒数, 必须为int类型
        :return:
        """
        __i = 1
        while __i <= num:
            __i += 1
            yield time.strftime(pattern, time.localtime(float(int(time.time()) + time_second)))

    @staticmethod
    def random_area_code(return_type=0, num=1):
        """
        随机生成区域编码，依赖addr.py
        :return:type为0返回：440000，为1返回：(110229, u'\u5efa\u59cb\u53bf')
        """
        __i = 1
        while __i <= num:
            __i += 1
            if return_type == 0:
                yield addr[random.randint(0, len(addr) - 1)][0]
            elif return_type == 1:
                yield addr[random.randint(0, len(addr) - 1)]
            else:
                pass

    def random_nation(self, num=1, path='../Config/Const.conf'):
        """
        随机生成民族
        :param num:迭代次数
        :param path: 配置文件路径
        :return: 返回民族
        """
        __i = 1
        while __i <= num:
            __all_nation = list(eval(self.cul.get_config('attribute_conf', 'nation', path)))
            yield choice(__all_nation)
            __i += 1

    @staticmethod
    def random_train_num(num=1):
        """
        随机生成火车班次
        :return:
        """
        en = ['K', 'Z', 'D', 'G', 'T']
        __i = 1
        while __i <= num:
            __i += 1
            yield '{0}{1}'.format(en[random.randint(0, 4)], random.randint(1, 9999))

    @staticmethod
    def random_airplane_num(num=1):
        """
        随机生成航班号
        :return:
        """
        src_uppercase = string.ascii_uppercase  # string_大写字母
        # src_lowercase = string.ascii_lowercase  # string_小写字母
        # __all_cae = src_uppercase + src_lowercase
        __i = 1
        while __i <= num:
            __i += 1
            yield ''.join(random.sample(src_uppercase, 2)) + str(random.randint(100, 9999))

    @staticmethod
    def random_airplane_port(num=1):
        """
        读取全国机场的excel，然后随机选取一个三字码
        :return:
        """
        all_port = CommonUtil.excel_read('../Config/airplane.xlsx')
        __i = 1
        while __i <= num:
            __i += 1
            yield str(choice(all_port))

    @staticmethod
    def random_string(num=1, low_case=0, digits_num=0, all_num=6):
        """
        随机返回一组字母和数字组成的字符串
        :param all_num: 字符总数
        :param num: 生成个数
        :param low_case: 是否包含小写字母
        :return: 例：'CMJN0S'
        """
        src_digits = string.digits  # string_数字
        src_uppercase = string.ascii_uppercase  # string_大写字母
        src_lowercase = string.ascii_lowercase  # string_小写字母
        __i = 1
        while __i <= num:
            # 随机生成数字、大写字母、小写字母的组成个数（可根据实际需要进行更改）
            # if digits_num == 1:
            #     digits_num = random.randint(1, 3)
            # else:
            #     digits_num = 0
            # __i += 1
            # if low_case == 1:
            #     uppercase_num = random.randint(1, all_num - digits_num - 1)
            #     lowercase_num = all_num - (digits_num + uppercase_num)
            # else:
            uppercase_num = all_num - int(digits_num) - int(low_case)
                # lowercase_num = 0
            # 生成字符串
            password = random.sample(src_digits, int(digits_num)) + random.sample(src_uppercase,
                                                                             uppercase_num) + random.sample(
                src_lowercase, int(low_case))
            # 打乱字符串
            random.shuffle(password)
            # 列表转字符串
            new_password = ''.join(password)
            yield new_password

    def random_website(self, num=1, path='../Config/Const.conf'):
        """
        随机生成网站域名
        :return: 如：'www.baidu.com'
        """
        __domain = list(eval(self.cul.get_config('attribute_conf', 'commonUse_domain', path)))
        __i = 1
        while __i <= num:
            __i += 1
            yield 'www.{0}{1}'.format(self.random_string(low_case=True).next(), choice(__domain))

    @staticmethod
    def airplane_seat(num=1):
        """
        返回航班座位号
        :return: 14F
        """
        __i = 1
        src_uppercase = string.ascii_uppercase
        while __i <= num:
            __i += 1
            yield str(random.randint(1, 90)) + choice(src_uppercase[0:13])

    def old_credit_id(self, num=1):
        """
        15位随机身份证号生成器
        :return: 15位身份证号
        """
        __i = 1
        while __i <= num:
            __i += 1
            yield self.cul.new2old(self.credit_id().next())

    def random_credit_id(self, num=1, digit=18, start="1960-01-01", end="2016-12-30", area=None):
        """
        随机生成身份证号码，可根据传参确定生成的身份证号码位数
        :param num: 生成的身份证号迭代对象个数
        :param digit: 生成的身份证号码的位数
        :return:
        """
        if area == "None":
            area = None
        __i = 1
        while __i <= num:
            __i += 1
            if int(digit) == 18:
                yield Random_CreditID.getRandomIdNumber(start=start, end=end, area=area)
            elif int(digit) == 15:
                yield self.cul.new2old(Random_CreditID.getRandomIdNumber(start=start, end=end, area=area))
            else:
                pass

    @staticmethod
    def random_ip(num=1):
        """
        随机生成ipv4地址
        :return: 如：'238.34.12.228'
        """
        __i = 1
        while __i <= num:
            __i += 1
            yield socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff)))

    @staticmethod
    def random_ipv6(num=1):
        """
        随机生成ipv6地址
        :return: 如：'1f7d:9240:5049:8517:1'
        """
        __i = 1
        while __i <= num:
            __i += 1
            yield ':'.join('{:x}'.format(random.randint(0, 2 ** 16 - 1)) for i in range(4)) + ':1'

    def random_address(self, num=1):
        """
        随机生成地址
        :return: 例：'醒介忽路8040号'
        """
        __i = 1
        while __i <= num:
            __i += 1
            yield '{0}路{1}号'.format(self.random_chinese(random.randint(2, 3)).next(), random.randint(1, 9999))

    @staticmethod
    def random_mac(number=1):
        """
        #随机生成MAC：X0:XX:XX:XX:XX:XX。返回类型是generator，具体使用返回的时候请见例子1、2,例子1、2的返回都是str
           生成Mac  X0:XX:XX:XX:XX:XX
            例子1：
            #批量生成
            for i in make_mac(number=10):
                print i
            例子2：
            #生成一条mac
            print make_mac().next()
        """
        num = 1
        while num <= number:
            yield '%02x:%02x:%02x:%02x' % (
                random.randint(0x00, 0xff), random.randint(0x00, 0xff), random.randint(0x00, 0xff),
                random.randint(0x00, 0xff))
            num += 1

    def random_cdlx(self, num=1):
        """
        随机获取车道类型
        00-直行机动车车道
        01-直左混行机动车车道
        02-直右混行机动车车道
        03-左右混行机动车车道
        04-直左右混行机动车车道
        05-左转机动车车道
        06-右转机动车车道
        07-非机动车车道
        08-机动车掉头机动车车道
        11-小客车道
        12-客车道
        13-客货车道
        19-应急车道
        :param num:迭代次数
        :return:返回车道编号
        """
        __i = 1
        while __i <= num:
            yield choice(list(eval(self.cul.get_config('attribute_conf', 'cdlx', '../Config/Const.conf'))))
            __i += 1

    def random_hpzl(self, num=1):
        """
        随机获取号牌种类
        01  大型汽车
        02  小型汽车
        03  使馆汽车
        04  领馆汽车
        05  境外汽车
        06  外籍汽车
        07  普通摩托车
        08  轻便摩托车
        09  使馆摩托车
        10  领馆摩托车
        11  境外摩托车
        12  外籍摩托车
        13  低速车
        14  拖拉机
        15  挂车
        16  教练汽车
        17  教练摩托车
        18  试验汽车
        19  试验摩托车
        20  临时入境汽车
        21  临时入境摩托车
        22  临时行驶车
        23  警用汽车
        24  警用摩托
        25  原农机号牌
        26  香港入出境车
        27  澳门入出境车
        31  武警号牌
        32  军队号牌
        41  无号牌
        42  假号牌
        43  挪用号牌
        44  无法识别
        99  其他号牌
        :param num: 迭代次数
        :return: 返回号牌迭代对象
        """
        __i = 1
        while __i <= num:
            yield choice(list(eval(self.cul.get_config('attribute_conf', 'hpzl', '../Config/Const.conf'))))
            __i += 1

    def random_car_num(self, num=1):
        """
        随机生成车牌号码
        :param num: 迭代次数
        :return: 返回迭代对象
        """
        __i = 1
        _all_first = self.cul.excel_read('..\\Config\\car_num.xls', sheet=0, col=0)
        while __i <= num:
            yield '{0}{1}'.format(choice(_all_first), str(random.randint(0, 99999)).zfill(5))
            __i += 1

    def random_imsi(self, num=1):
        """
        随机生成IMSI号
        :param num: 迭代次数，即生成的个数
        :return: 返回imsi迭代对象
        """
        mcc = '460'
        mnc_list = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '11', '20']
        __i = 1
        while __i <= num:
            yield '{0}{1}{2}'.format(mcc, choice(mnc_list), str(random.randint(0, 9999999999)).zfill(10))
            __i += 1

    def random_num(self, num=1, start=1000000, end=99999999):
        """
        随机生成int型随机数
        :param start: 开始数字
        :param end: 结束数字
        :return: 返回整形随机数
        """
        __i = 1
        while __i <= num:
            yield random.randint(int(start), int(end))

    def random_sex(self):
        """
        随机生成性别
        :return:
        """
        __sex = random.randint(0, 1)
        if __sex == 1:
            return '男'
        elif __sex == 0:
            return '女'
        else:
            return '未知'

    @staticmethod
    def __get_imei_l(digits14):
        digit15 = 0
        for num in range(14):
            if num % 2 == 0:
                digit15 = digit15 + int(digits14[num])
            else:
                digit15 = digit15 + (int(digits14[num]) * 2) % 10 + (int(digits14[num]) * 2) / 10
        digit15 = int(digit15) % 10
        if digit15 == 0:
            digits14 = digits14 + str(digit15)
        else:
            digits14 = digits14 + str(10 - digit15)
        return digits14

    def random_imei(self, num=1):
        """
        随机生成IMEI
        :param num:迭代次数
        :return: 返回IMEI迭代对象
        """
        __i = 1
        while __i <= num:
            yield self.__get_imei_l(str(random.randint(12345678901234, 99999999991234)))
            __i += 1


def main():
    """
    测试代码
    """
    rdc = RandomConst()
    # for i in range(10):
    #     print rdc.random_username().next()
    # print rdc.random_email().next()
    # print RandomComment()
    for i in  rdc.random_credit_id(num=1000, digit=18, start='1953-01-01', end='2002-12-31'):
        print i
    # for i in rdc.random_cdlx(num=100):
    #     print i
    # for i in rdc.random_hpzl(num=100):
    #     print i
    # for i in rdc.random_car_num(num=10):
    #     print i
    # for i in rdc.random_imsi(num=10):
    #     print i
    # for i in rdc.random_email(num=10):
    #     print i
    # print RandomCourse_name()
    # for i in rdc.random_phone(10000):
    #     print i
    # a = rdc.random_passport(1000)
    # for i in range(1000):
    #     print a.next()
    # for i in rdc.random_TW_passport(1000):
    #     print i
    # for i in rdc.random_GA_passport(1000):
    #     print i
    # print rdc.random_train_num().next()
    # for i in rdc.random_airplane_num(num=100):
    #     print i
    # print rdc.date_time().next()
    # print rdc.airplane_port().next()
    # print rdc.date_time(pattern='%H%M').next()
    # print rdc.random_string().next()
    # print rdc.airplane_seat().next()
    # print rdc.random_website().next()
    # print rdc.random_ip().next()
    # print rdc.random_ipv6().next()
    # print rdc.random_chinese(5).next()
    # for i in rdc.random_area_code(return_type=1, num=10):
    #     print i
    # print rdc.random_address().next()
    # print rdc.random_username().next()

    # num = 1000
    # a = rdc.random_username(num)
    # for i in range(num):
    #     print a.next()
    # for i in rdc.random_mac(1000):
    #     print i
    # for i in rdc.random_nation(num=10):
    #     print i
    # for i in rdc.random_imei(num=10):
    #     print i


def test(n):
    rdc = RandomConst()
    # for i in range(1, n):
    #     print rdc.random_username().next()
    # for i in rdc.random_username(n):
    #     print i


if __name__ == '__main__':
    # import timeit
    # test_round = 1000
    # time_cost = timeit.timeit("test(1000)", setup="from __main__ import test", number=test_round)
    # print time_cost
    main()
