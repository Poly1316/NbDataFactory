#!/usr/bin/env python
# -*- coding: utf8 -*-
from __future__ import unicode_literals

from time import sleep

from atbase.attributeoperation import *
from atbase.fileoperation import readfile_towhole
from atbase.oracledb import OracleDB
from pyse import Pyse
# from FkLibrary.libraries.util import util
from src.commonDao import CommonUtil


class FkBase(Pyse):
    def __init__(self,path=None,title=None):
        super(FkBase,self).__init__()
        self.cul = CommonUtil()
        if path == None:
            path_common = self.cul.get_config('base_conf', '', '../../config/common.ini')
            path_person = util.abspath(__file__, '../../config/person_details.ini')
            path = util.abspath(__file__,'../../config/person_center.ini')
            path_person_relation_analyze = util.abspath(__file__, '../../config/person_relation_analyze.ini')
        if title == None:
            title_common = 'common'
            title_person = 'person_details'
            title = 'person_center'
            title_person_relation_analyze = 'person_relation_analyze'
        self.common = util.ConfigIni(path_common, title_common)
        self.person = util.ConfigIni(path_person, title_person)
        self.details = util.ConfigIni(path,title)
        self.relation_analyze = util.ConfigIni(path_person_relation_analyze, title_person_relation_analyze)

    def get_IDcard(self,IDcard):#根据身份证号，返回生日和性别
        if len(IDcard) == 18:
            y,m,d = int(IDcard[6:10]),int(IDcard[11:12]),int(IDcard[13:14])
            bir = '%04d-%02d-%02d' % (y,m,d)
            if int(IDcard[-2])%2 == 1:#取余
                sex = "男性"#0为女性
            else:
                sex = "女性"#1为男性
        else:
            bir = sex = ""
        return bir,sex

    def fk_open_browser(self, browserurl, browser='u2'):
        '''
        打开浏览器
        browser：浏览器类型| browserurl：浏览器安装位置
        '''
        self.open_browser(browser, browserurl)
        self.max_window()

    def fk_login(self, url, username, password):
        '''
        登录
        url：打开地址| username：用户名| password：密码
        '''
        if url != None:
            self.open(url)
        # print self.driver.page_source 页面源代码
        self.input_text(self.common.get_ini("login_username"), username, 15)
        self.input_text(self.common.get_ini("login_password"), password)
        self.click(self.common.get_ini("login_click"))
        sleep(5)
        if self.element_present('xpath=>//div[@class="desktop-guide-wrap" and @style="display: block;"]'):
            self.js("$('.desktop-guide-wrap').attr('style','display: none;')")#关掉教学步骤

    def fk_logout(self):
        '''
        退出登录
        '''
        self.click(self.common.get_ini("username_a"))
        sleep(1)
        self.click(self.common.get_ini("logout_a"))
        sleep(1)
        self.click(self.common.get_ini("sure_a"))

    def fk_menu_click(self):
        self.click(self.common.get_ini("login_check"))

    def select_input_value(self,locator,text,secs=3):#输入型下拉框
        self.click(locator, secs=secs)
        sleep(0.5)
        self.input_text(locator, text, secs=secs)
        self.click("xpath=>//span[text()='%s']" % text)

    def select_value(self,locator,text,secs=3):#下拉框
        self.click(locator, secs=secs)
        sleep(0.5)
        self.click("xpath=>//span[text()='%s']" % text)

    def close_browser(self):
        '''
        关闭浏览器事件
        无参数
        '''
        self.quit()

    def del_IdCard(self,IdCard,user="hero",pwd="hero",conn='172.16.114.236:1521/ora11g'):
        """
        #执行sql文件中的语句，删除身份证号
        :param IdCard: 18位身份证号，str
        :param user: 数据库用户名，str
        :param pwd: 数据库密码，str
        :param conn: 数据库连接串，str
        :return:正确返回True和"",错误返回False和错误信息
        example:del_IdCard(IdCard="610114199009040825")
        """
        path = util.abspath(__file__,'../../config/del_ID_number.sql')
        card = IdentityCard()
        newcard = card.new2old(IdCard)
        db = OracleDB()
        db.conn_ora(user,pwd,conn)
        sql = readfile_towhole(path)
        oldcard = sql.split("('")[1].split("')")[0]
        sql = sql.replace(oldcard,newcard)
        status,rs = db.select_ora(sql)
        return status,rs

    def _open_person_center_details(self, new_idcard):
        '''
        打开人员中心某人详情页面
        :param new_idcard:人员身份证号码
        :return:返回状态和异常:若有异常,则返回异常信息
        '''
        try:
            if self.element_not_present(self.details.get_ini('serach_input'), 5):
                self.switch_to_frame(self.details.get_ini('add_in_iframe'))
            self.click(self.details.get_ini('serach_input'))
            self.input_text(self.details.get_ini('idcard_input'), new_idcard)
            self.click(self.details.get_ini('serach_sure_btn'))
            self.click(self.details.get_ini('serach_btn'))
            sleep(2)
            self.click(self.details.get_ini('details_a') % new_idcard)
            self.switch_to_frame_out()
            self.switch_to_frame(self.details.get_ini("bi_in_iframe"))
            sleep(1)
            return True, ""
        except Exception, e:
            print e
            import traceback
            print traceback.format_exc()
            return False, e

    def _save_value_dict(self, infolist):
        '''
        保存页面获取的数据
        :param infolist:分割页面数据后的list
        :return :返回保存结果（字典）
        '''
        info = {}
        for i in range(len(infolist)):
            if infolist[i][-1] == "：":
                if i + 1 < len(infolist):
                    if infolist[i + 1][-1] == "：":
                        info[infolist[i][:-1]] = ""
                    else:
                        info[infolist[i][:-1]] = infolist[i + 1]
                else:
                    info[infolist[i][:-1]] = ""
        return info

    def _compare_info(self, info, infobase):
        '''
        对比实际结果和预期结果：比较是以预期结果为准，当实际结果有，预期结果没有的情况，直接忽略实际结果
        :param info: 预期结果字典
        :param infobase: 实际结果字典
        '''
        errorinfobase = {}
        for key in info: # 循环预期结果
            exp_value = info.get(key)
            if key in infobase:
                act_value = infobase.get(key)
                if exp_value != act_value:
                    errorinfobase[key] = "预期结果:{},实际结果:{}".format(exp_value, act_value)
            else:
                errorinfobase[key] = "预期结果:{},实际结果:{}".format(exp_value, "页面没有该字段")
        return errorinfobase
        

if __name__ == "__main__":
    # pass
    fb = FkBase()
    fb.fk_open_browser("C:/Users/Administrator/AppData/Local/U2/Application/u2.exe")