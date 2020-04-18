#!/usr/bin/env python
# -*- coding: utf8 -*-
from __future__ import unicode_literals

import os
import time
# from robot.libraries.Screenshot import Screenshot
import traceback
from time import sleep

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait


# from FkLibrary.env.common import *


class CustomWebDriverWait(WebDriverWait):
    def until(self, method, message=''):
        """Calls the method provided with the driver as an argument until the \
        return value is not False."""
        screen = None
        stacktrace = None
        end_time = time.time() + self._timeout
        while True:
            try:
                value = method(self._driver)
                if value:
                    return value
            except self._ignored_exceptions as exc:
                screen = getattr(exc, 'screen', None)
                stacktrace = getattr(exc, 'stacktrace', None)
                if message == "":
                    message = exc
            time.sleep(self._poll)
            if time.time() > end_time:
                break
        self.__write_text()
        raise TimeoutException(message, screen, stacktrace)

    def until_not(self, method, message=''):
        """Calls the method provided with the driver as an argument until the \
        return value is False."""
        end_time = time.time() + self._timeout
        while True:
            try:
                value = method(self._driver)
                if not value:
                    return value
            except self._ignored_exceptions:
                return True
            time.sleep(self._poll)
            if time.time() > end_time:
                break
        self.__write_text()
        raise TimeoutException(message)

    def __write_text(self):
        '''
        写入报错页面的pagesource
        :param path: 写入文件所在路径
        '''
        path = os.getcwd()
        list = path.split("\\")
        base = list[0] + "\\" + list[1]
        file = open(base + "\\pagesource.txt", "w")
        file.write(self._driver.page_source)
        file.close()

class Pyse(object):
    '''
    主要封装selenium常用方法
    '''
    TIMEOUT = 3 #超时时间
    POLL_FREQUENCY = 0.05  #超时时间内的检查间隔

    def __init__(self):
        self.driver = None

    def open_browser(self, browser, browserurl):
        '''
        创建webdriver,选择浏览器类型和浏览器地址
        browser:浏览器类型 如：firefox,chrome,u2,internet explorer,opera,phantomjs，需下载相应driver | browserurl:浏览器地址
        '''
        if browser == "firefox" or browser == "ff":
            driver = webdriver.Firefox(executable_path=browserurl)
        elif browser == "chrome":
            driver = webdriver.Chrome(executable_path=browserurl)
        elif browser == "u2":
            __browser_url = browserurl
            __prefs = {'download.default_directory':'D:\\U2\\Downloads\\fk'}
            chrome_options = Options()
            chrome_options.binary_location = __browser_url
            chrome_options.add_experimental_option('prefs', __prefs)
            # chrome_options.add_argument("--user-data-dir=C:/Users/Administrator/AppData/Local/U2/User\ Data")#加缓存
            # chrome_options.add_extension("ActiveXForChrome_1.3.0.crx")
            # executable_path = "C:/Users/Administrator/AppData/Local/U2/chromedriver.exe"
            driver = webdriver.Chrome(chrome_options=chrome_options)
        elif browser == "internet explorer" or browser == "ie":
            driver = webdriver.Ie(executable_path=browserurl)
        elif browser == "opera":
            driver = webdriver.Opera(executable_path=browserurl)
        elif browser == "phantomjs":
            dcap = dict(DesiredCapabilities.PHANTOMJS)
            dcap["phantomjs.page.settings.userAgent"] = ("Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36 FH/1.0.0.2 (D7E6D8902CF1F892)(C650C8A73DEADC49)")
            driver = webdriver.PhantomJS(desired_capabilities=dcap, executable_path=browserurl)
        elif browser == 'edge':
            driver = webdriver.Edge(executable_path=browserurl)
        try:
            self.driver = driver
        except Exception:
            print traceback.format_exc()
            raise NameError("Not found %s browser,You can enter 'ie', 'ff', 'opera', 'phantomjs', 'edge' or 'chrome'." %browser)

    def enter(self,locator,secs=TIMEOUT):
        self.get_element(locator,secs).send_keys(Keys.ENTER)

    def back_space(self,locator, secs=TIMEOUT):
        self.get_element(locator,secs).send_keys(Keys.BACK_SPACE)

    def space(self,locator, secs=TIMEOUT):
        self.get_element(locator,secs).send_keys(Keys.SPACE)

    def tab(self,locator, secs=TIMEOUT):
        self.get_element(locator,secs).send_keys(Keys.TAB)

    def espace(self,locator, secs=TIMEOUT):
        self.get_element(locator,secs).send_keys(Keys.ESCAPE)

    def control_a(self,locator, secs=TIMEOUT):
        self.get_element(locator,secs).send_keys(Keys.CONTROL,'a')

    def control_c(self,locator, secs=TIMEOUT):
        self.get_element(locator,secs).send_keys(Keys.CONTROL,'c')

    def control_x(self,locator, secs=TIMEOUT):
        self.get_element(locator,secs).send_keys(Keys.CONTROL,'x')

    def control_v(self,locator, secs=TIMEOUT):
        self.get_element(locator,secs).send_keys(Keys.CONTROL,'v')

    def open(self, url):
        '''
        打开页面
        url:页面地址 | wait：页面打开后等待时间，不填默认为0不等待
        '''
        self.driver.get(url)


    def max_window(self):
        '''
        Set browser window maximized.
        '''
        self.driver.maximize_window()

    def set_window(self, wide, high):
        '''
        Set browser window wide and high.
        '''
        self.driver.set_window_size(wide, high)

    def input_text(self, locator, text, secs=TIMEOUT):
        '''
        Operation input box.
        '''
        self.clear_text(locator,secs)
        self.get_element(locator,secs).send_keys(text)

    def clear_text(self, locator, secs=TIMEOUT):
        '''
        Clear the contents of the input box.
        '''
        self.get_element(locator, secs).clear()

    def click(self, locator, secs=TIMEOUT):
        '''
        It can click any text / image can be clicked
        Connection, check box, radio buttons, and even drop-down box etc..
        '''
        self.element_clickable(locator, secs).click()


    def scroll_click(self,locator, secs=TIMEOUT):
        '''
        :param secs:
        :return:
        '''
        target = self.get_element(locator, secs)
        self.driver.execute_script("arguments[0].scrollIntoView(false);", target)
        self.click(locator,secs)

    def right_click(self, locator, secs=TIMEOUT):
        '''
        Right click element.
        '''
        el = self.element_clickable(locator, secs)
        ActionChains(self.driver).context_click(el).perform()

    def select_by_value(self,locator,value,secs=TIMEOUT):
        e1 = self.get_element(locator, secs)
        Select(e1).select_by_value(value)


    def move_to_element(self, locator, secs=TIMEOUT):
        '''
        Mouse over the element.
        '''
        el = self.get_element(locator, secs)
        ActionChains(self.driver).move_to_element(el).perform()

    def move_to_element_offset_click(self,locator, secs=TIMEOUT):
        '''
        Mouse over the element.
        '''
        el = self.element_clickable(locator, secs)
        ActionChains(self.driver).move_to_element(el).click().perform()

    def move_to_element_offset_right_click(self,locator, dx, dy, secs=TIMEOUT):
        '''
        Mouse over the element.

        Usage:
        driver.move_to_element("css=>#el")
        '''
        el = self.element_clickable(locator, secs)
        ActionChains(self.driver).move_to_element_with_offset(el, dx, dy).context_click().perform()

    def double_click(self, locator, secs=TIMEOUT):
        '''
        Double click element.

        Usage:
        driver.double_click("css=>#el")
        '''
        el = self.element_clickable(locator, secs)
        ActionChains(self.driver).double_click(el).perform()

    def drag_and_drop(self, el_locator, ta_locator, secs=TIMEOUT):
        '''
        Drags an element a certain distance and then drops it.

        Usage:
        driver.drag_and_drop("css=>#el","css=>#ta")
        '''
        el = self.element_located_visiable(el_locator, secs)
        ta = self.element_located_visiable(ta_locator, secs)
        ActionChains(self.driver).drag_and_drop(el, ta).perform()

    def close(self):
        '''
        Simulates the user clicking the "close" button in the titlebar of a popup
        window or tab.

        Usage:
        driver.close()
        '''
        self.driver.close()

    def quit(self):
        '''
        Quit the driver and close all the windows.

        Usage:
        driver.quit()
        '''
        self.driver.quit()

    def submit(self, locator, secs=TIMEOUT):
        '''
        Submit the specified form.

        Usage:
        driver.submit("css=>#el")
        '''
        el = self.get_element(locator, secs)
        el.submit()

    def F5(self):
        '''
        Refresh the current page.

        Usage:
        driver.F5()
        '''
        self.driver.refresh()
        sleep(2)

    def js(self, script):
        '''
        Execute JavaScript scripts.

        Usage:
        driver.js("window.scrollTo(200,1000);")
        '''
        return self.driver.execute_script(script)

    def get_attribute(self, locator, attribute, secs=TIMEOUT):
        '''
        获取元素属性的值
        Gets the value of an element attribute.
        attribute：元素的属性，例如class,type之类
        Usage:
        driver.get_attribute("css=>#el","type")
        '''
        el = self.get_element(locator, secs)
        return el.get_attribute(attribute)

    def get_attributes(self, locator, attribute, secs=TIMEOUT):
        '''
        获取元素属性的值
        Gets the value of an element attribute.
        attribute：元素的属性，例如class,type之类
        Usage:
        driver.get_attribute("css=>#el","type")
        '''
        els = self.get_elements(locator, secs)
        rs = []
        for el in els:
            rs.append(el.get_attribute(attribute))
        return rs

    def get_text(self, locator, secs=TIMEOUT):
        '''
        Get element text information.

        Usage:
        driver.get_text("css=>#el")
        '''
        el = self.get_element(locator, secs)
        return el.text

    def get_display(self, locator, secs=TIMEOUT):
        '''
        Gets the element to display,The return result is true or false.

        Usage:
        driver.get_display("css=>#el")
        '''
        el = self.get_element(locator, secs)
        return el.is_displayed()

    def get_title(self):
        '''
        Get window title.

        Usage:
        driver.get_title()
        '''
        return self.driver.title

    def get_url(self):
        '''
        Get the URL address of the current page.

        Usage:
        driver.get_url()
        '''
        return self.driver.current_url

    def get_windows_img(self, file_path,name="screenshot",width="800px"):
        '''
        Get the current window screenshot.

        Usage:
        driver.get_windows_img()
        '''
        self.screenshot = Screenshot(file_path)
        try:
            path = self.screenshot._get_screenshot_path(name, file_path)
            # self.driver.get_screenshot_as_file(path)
            self.screenshot._embed_screenshot(path, width)
            # self.driver.get_windows_img(path, width)
        except Exception,e:
            print traceback.format_exc()
            self.screenshot.take_screenshot(name, width)

    def implicit_wait(self, secs):
        '''
        Implicitly wait.All elements on the page.

        Usage:
        driver.wait(10)
        '''
        self.driver.implicitly_wait(secs)

    def accept_alert(self):
        '''
        Accept warning box.

        Usage:
        driver.accept_alert()
        '''
        self.driver.switch_to.alert.accept()

    def dismiss_alert(self):
        '''
        Dismisses the alert available.

        Usage:
        driver.dismiss_alert()
        '''
        self.driver.switch_to.alert.dismiss()


    def switch_to_frame_out(self):
        '''
        Returns the current form machine form at the next higher level.
        Corresponding relationship with switch_to_frame () method.

        Usage:
        driver.switch_to_frame_out()
        '''
        self.driver._switch_to.default_content()

    # def open_new_window(self, locator):
    #     '''
    #     Open the new window and switch the handle to the newly opened window.
    #
    #     Usage:
    #     driver.open_new_window()
    #     '''
    #     original_windows = self.get_current_window_handle()
    #     self.click(locator)
    #     sleep(3)
    #     all_handles = self.get_all_handles()
    #     for handle in all_handles:
    #         if handle != original_windows:
    #             self.switch_to_window(handle)

    def get_all_handles(self):
        return self.driver.window_handles

    def get_current_window_handle(self):
        return self.driver.current_window_handle

    def switch_to_window(self, window_name):
        self.driver.switch_to_window(window_name)
        # self.driver._switch_to.window(window_name)

    def element_present(self, locator, secs=TIMEOUT):
        '''
        判断元素是否存在，返回True or False
        Determine whether the elements exist
        '''
        flag = True
        try:
            self.get_element(locator, secs)
        except:
            flag = False
        return flag

    def title_is(self, title):
        '''
        判断title是否符合预期
        :param title: 标题
        :return:  True or False
        '''
        return EC.title_is(title)(self.driver)

    def title_contains(self, title):
        '''
        判断title是否包含预期字符
        :param title: title
        :return:  True or False
        '''
        return EC.title_contains(title)(self.driver)


    def get_element(self, locator, secs=TIMEOUT):
        '''
        等待元素出现，限定时间内不出现视为找不到,会抛出TimeoutException异常
        @param locator: 元素位置 格式为id/name/class/link_text/xpath/css => "xxx"
        @param secs: 超时时间
        @return 元素对象，在超时时间内若未找到元素则会抛出超时异常
        '''
        element = self._explicit_wait(secs).until(EC.presence_of_element_located(self._locator_split(locator)))
        return element

    def get_elements(self, locator, secs=TIMEOUT):
        '''
        获取所有元素集合 ，限定时间内不出现视为找不到,会抛出TimeoutException异常
        @param locator: 元素位置 格式为id/name/class/link_text/xpath/css => "xxx"
        @param secs: 超时时间
        @return 元素对象，在超时时间内若未找到元素则会抛出超时异常
        '''
        elements = self._explicit_wait(secs).until(EC.presence_of_all_elements_located(self._locator_split(locator)))
        return elements

    def get_texts(self,locator, secs=TIMEOUT):
        elements = self.get_elements(locator,secs)
        text_list = []
        for element in elements:
            text_list.append(element.text)
        return text_list

    def get_text_by_el(self,locator1,locator2, secs=TIMEOUT):#[回流人员,重点;回流人员;重点年龄段,重点;回流人员;重点年龄段;重点考察人员]
        element1s = self.get_elements(locator1,secs)
        lens = len(element1s)
        text_list = []
        for i in range(1,lens+1):
            element2s = self.get_elements(locator2.format(str(i)),secs)
            text = ""
            for element2 in element2s:
                text = text + element2.text + ";"
            text_list.append(text.strip(";"))
        return text_list


    def element_not_present(self, locator, secs=TIMEOUT):
        '''
        在限定时间内，检查元素是否消失（不存在）
        @param locator: 元素位置 格式为id/name/class/link_text/xpath/css => "xxx"
        @param secs: 检查的超时时间
        @return True(不存在) or False（存在）
        '''
        if self.element_present(locator):
            try:
                flag = self._explicit_wait(secs).until_not(EC.presence_of_element_located(self._locator_split(locator)))
            except TimeoutException:
                flag = False
        else:
            flag = True
        return flag

    def element_located_visiable(self, locator, secs=TIMEOUT):
        '''
        在限定时间内，检查元素是否可视（Visibility means that the element is not only displayed
    but also has a height and width that is greater than 0.）
        @param locator: 元素位置 格式为id/name/class/link_text/xpath/css => "xxx"
        @param secs: 检查的超时时间
        @return 元素对象 or 触发超时异常
        '''
        element = self._explicit_wait(secs).until(EC.visibility_of_element_located(self._locator_split(locator)))
        return element

    def element_visiable(self, element, secs=TIMEOUT):
        '''
        在限定时间内，检查元素是否可视（Visibility means that the element is not only displayed
    but also has a height and width that is greater than 0.）
        @param element: selenuim元素对象
        @param secs: 检查的超时时间
        @return 元素对象 or 触发超时异常
        '''
        element = self._explicit_wait(secs).until(EC.visibility_of(element))
        return element

    def text_present_in_element(self, locator, text, secs=TIMEOUT):
        '''
        在限定时间内判断某个元素标签中的文本值中是否存在text字符串， element.text
        @param locator: 元素位置 格式为id/name/class/link_text/xpath/css => "xxx"
        @param text: 需要判断是否存在的字符串
        @param secs: 检查的超时时间
        @return True or False 即存在或者不存在
        '''
        try:
            flag = self._explicit_wait(secs).until(EC.text_to_be_present_in_element(self._locator_split(locator), text))
        except TimeoutException:
            print traceback.format_exc()
            flag = False
        return flag

    def text_present_in_element_value(self, locator, text, secs=TIMEOUT):
        '''
        在限定时间内判断某个元素对象的value属性中是否存在text字符串， element.get_attribute("value")
        @param locator: 元素位置 格式为id/name/class/link_text/xpath/css => "xxx"
        @param text: 需要判断是否存在的字符串
        @param secs: 检查的超时时间
        @return True or False 即存在或者不存在
        '''
        try:
            flag = self._explicit_wait(secs).until(EC.text_to_be_present_in_element_value(self._locator_split(locator), text))
        except TimeoutException:
            print traceback.format_exc()
            flag = False
        return flag

    def switch_to_frame(self, locator, secs=TIMEOUT):
        '''
        Switch to the specified frame.
        @param locator: 元素定位
        @return True or False
        '''
        self._explicit_wait(secs).until(EC.frame_to_be_available_and_switch_to_it(self._locator_split(locator)))

    
    def element_clickable(self, locator, secs=TIMEOUT):
        '''
        在限定时间内，检查元素是否可以被点击
        @param locator: 元素位置 格式为id/name/class/link_text/xpath/css => "xxx"
        @param secs: 检查的超时时间
        @return 元素对象 or 触发超时异常
        '''
        element = self._explicit_wait(secs).until(EC.element_to_be_clickable(self._locator_split(locator)))
        return element
    
    def element_selected(self, element, secs=TIMEOUT):
        '''
        在限定时间内，检查元素对象是否被选中
        @param element: 元素对象
        @param secs: 检查的超时时间
        @return True(selected) or False（not selected）
        '''
        try:
            flag = self._explicit_wait(secs).until(EC.element_to_be_selected(element))
        except TimeoutException:
            print traceback.format_exc()
            flag = False
        return flag
    
    def element_located_selected(self, locator, secs=TIMEOUT):
        '''
        在限定时间内，检查元素位置是否被选中
        @param locator: 元素位置 格式为id/name/class/link_text/xpath/css => "xxx"
        @param secs: 检查的超时时间
        @return True(selected) or False（not selected）
        '''
        try:
            flag = self._explicit_wait(secs).until(EC.element_located_to_be_selected(self._locator_split(locator)))
        except TimeoutException:
            print traceback.format_exc()
            flag = False
        return flag
    
    def alert_present(self, secs=TIMEOUT):
        '''
        在限定时间内，检查当前页面是否存在alert框
        @param secs: 检查的超时时间
        @return alert元素对象 or 触发超时异常
        '''
        alert = self._explicit_wait(secs).until(EC.alert_is_present())
        return alert
    
    def _locator_split(self, locator):
        '''
        确定元素位置定位的类型
        '''
        if "=>" not in locator:
            print traceback.format_exc()
            raise NameError("Positioning syntax errors, lack of '=>'.")
        by = locator.split("=>")[0]
        value = locator.split("=>")[1]
        if by == "id":
            _by = By.ID
        elif by == "name":
            _by = By.NAME
        elif by == "class":
            _by = By.CLASS_NAME
        elif by == "tag_name":
            _by = By.TAG_NAME
        elif by == "link_text":
            _by = By.LINK_TEXT
        elif by == "xpath":
            _by = By.XPATH
        elif by == "css":
            _by = By.CSS_SELECTOR
        elif by == "partial_link_text":
            _by = By.PARTIAL_LINK_TEXT
        else:
            print traceback.format_exc()
            raise NameError("Please enter the correct targeting elements,'id','name','class','link_text','xpath','css'.")
        return _by, value

    def _explicit_wait(self,secs=TIMEOUT, poll_frequency=POLL_FREQUENCY):
        '''
        初始化显性等待
        @param secs: 超时时间
        @param poll_frequency: 检查时间间隔（在超时时间内不断尝试）
        '''
        _wait = CustomWebDriverWait(driver=self.driver, timeout=secs, poll_frequency=poll_frequency)
        return _wait

# if __name__ == '__main__':
   # run = Pyse()
   # run.open_browser('u2', 'C:/Users/Administrator/AppData/Local/U2/Application/u2.exe')
#    run.open("http://172.16.5.39:8080/nebula/SSO!login.action?isDev=yes")
#    print run.title_is("登录")
#    print run.title_contains('登')
#    print run.get_element("xpath=>//div[@class='subtitle']", 1)
#    print run.get_elements("xpath=>//div[@class='subtitle']", 1)
#    print run.element_not_present("xpath=>//div[@class='subtitle']", 1)
#    print run.element_located_visiable("xpath=>//div[@class='subtitle1']", 1)
#    print run.element_visiable(run.driver.find_element('xpath', "//div[@class='subtitle']"), 1)
#    print run.text_present_in_element("xpath=>//div[@class='subtitle']", 'PLATFORM', 1)
#    print run.text_present_in_element_value("xpath=>//div[@class='subtitle']", 'PLATFORM', 1)
#    print run.element_clickable("xpath=>//div[@class='subtitle']", 1)
#    print run.element_selected(run.driver.find_element('xpath', "//div[@class='subtitle']"), 1)
#    print run.element_located_selected("xpath=>//div[@class='subtitle']", 1)
#    print run.alert_present(1)
#    # run.get_element("123")
#    
#    locator = "xpath=>//div[@class='subtitle']"
#    e = run.element_clickable(locator, 1)
#    if e:
#        run.click(locator)
#    else:
#        print 'unclickable'
