# -*- coding: UTF-8 -*-
"""
author = wangxiaotao
time = 2017/7/1
"随机生成身份证号码"
"""

import random
import datetime


# 随机生成身份证号
def getValidateCheckout(id17):
    """获得校验码算法"""
    weight = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]  # 十七位数字本体码权重   
    validate = ['1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2']  # mod11,对应校验码字符值   

    sum = 0
    for i in range(0, len(id17)):
        sum = sum + int(id17[i]) * weight[i]
    mode = sum % 11
    return validate[mode]


def getRandomIdNumber(start="1960-01-01", end="2016-12-30", area=None):
    """产生随机可用身份证号，sex = 1表示男性，sex = 0表示女性"""
    # 地址码产生
    from addr import addr  # 地址码
    if area is None:
        addrInfo = random.randint(0, len(addr)-1)  # 随机选择一个值
    elif area == '65':
        addrInfo = random.randint(3387, 3500)
    addrId = addr[addrInfo][0]
    addrName = addr[addrInfo][1]
    idNumber = str(addrId)
    # 出生日期码
    days = (datetime.datetime.strptime(end, "%Y-%m-%d") - datetime.datetime.strptime(start, "%Y-%m-%d")).days + 1
    birthDays = datetime.datetime.strftime(
        datetime.datetime.strptime(start, "%Y-%m-%d") + datetime.timedelta(random.randint(0, days)), "%Y%m%d")
    idNumber = idNumber + str(birthDays)
    # 顺序码
    for i in range(2):  # 产生前面的随机值
        n = random.randint(0, 9)  # 最后一个值可以包括
        idNumber = idNumber + str(n)
    # 性别数字码
    sex = random.randint(0, 1)
    sexId = random.randrange(sex, 10, step=2)  # 性别码
    idNumber = idNumber + str(sexId)
    # 校验码
    checkOut = getValidateCheckout(idNumber)
    idNumber = idNumber + str(checkOut)
    return idNumber


if __name__ == '__main__':
    for i in range(100):
        print getRandomIdNumber(start='1983-01-01', end='2002-12-31', area='65')
