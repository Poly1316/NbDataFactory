#!/usr/bin/env python
# -*- coding: utf8 -*-
"""此模块封装了 文件内容解析，处理的相关功能，比如解析nb文件、按列替换文件内容等"""
import codecs
import fileinput
import os
import re
import sys
import random
import datetime, time
import shutil
import fnmatch
import json
import glob
from atbase.timeoperation import localtime
# from fude import Fude
# from remote.ssh import SSH as _SSH
# from system_cmd import scp_put as _scp_put
from atbase.system_cmd import list_files_in_directory as _list_files_in_directory
from atbase.system_cmd import basename as _basename
from atbase.system_cmd import dirname as _dirname

reload(sys)
sys.setdefaultencoding('utf-8')


def readfile(filename, mode='rb', encoding="utf-8", errors='strict', buffering=1, isnullrow=True):
    """
    # 读文件用\n做分隔,并去除多余的\n,后生成列表返回
    :param encoding: 文件编码方式，默认utf8
    :param filename: 文件绝对路径
    :return:返回文件内容，类型list
    """
    _file_list_ = []
    with codecs.open(filename, mode=mode, encoding=encoding, errors=errors,
                     buffering=buffering) as _openfile_:
        _readfile_ = _openfile_.readlines()
        for line in _readfile_:
            _line_ = line.rstrip('\r\n')
            if isnullrow:
                if _line_:
                    _file_list_.append(_line_)
            else:
                _file_list_.append(_line_)
    return _file_list_


def formatnbfile(filename, isnullrow=True, mode='rb', encoding="utf-8", errors='strict', buffering=1):
    """
    #将文件读出并且每行按\t分割  返回类型[["","","","",""],["","","","",""],[]],其中
    每个元素为每行内容，每个元素中的list的每个子元素为每行的每个字段内容。
    :param isnullrow:
    :param filename: 待读文件
    :return:返回类型[["","","","",""],["","","","",""],[]]
    """
    content = readfile(filename, isnullrow=isnullrow, mode=mode, encoding=encoding, errors=errors,
                       buffering=buffering)
    request_con = []
    for eachline in content:
        request_con.append(eachline.split("\t"))
    return request_con


def readfile_towhole(filename):
    """
    #直接返回文件的全部内容
    :param filename: 待读文件
    :return:类型str
    """
    with codecs.open(filename, mode='rb', encoding=None, errors='strict',
                     buffering=1) as _openfile_:
        result = _openfile_.read()
    return result


def writelisttofile(filename=None, contentlist=None, encoding='utf-8', mode="w",
                    errors='strict', buffering=1, cutoperator="\n"):
    """
    #用于将list内容写入文件
    :param filename:待写入的文件
    :param contentlist: 代写内容，类型str
    :param encoding: 文件编码方式，默认utf8
    :param mode: 写的方式默认是“w”
    :param cutoperator: 各个contentlist的元素的分隔符
    :return:无
    """
    if contentlist is None:
        contentlist = []
    with codecs.open(filename, mode=mode, encoding=encoding, errors=errors,
                     buffering=buffering) as _openfile_:
        for one in contentlist:
            _openfile_.write(one + cutoperator)


def replace_file_capturetime(originfile, newfile, column, day=-1):
    """
    #修改nb或bcp文件中的时间列。
    :param originfile:源文件
    :param newfile: 新文件
    :param column:时间列
    :param day:修改的天数，提前为负数，推迟为正数
    """
    #
    day *= 86400
    read_file = readfile(originfile)
    line_num = len(read_file)
    current_time = localtime()
    rewrite_file = codecs.open(newfile, 'w', encoding='UTF-8')
    for index, line in enumerate(read_file):
        line_list = line.split('\t')
        if isinstance(column, list):
            original_time = int(line_list[int(column[0]) - 1])
        else:
            original_time = int(line_list[int(column) - 1])
        new_current_time = time.strftime("%Y%m%d", time.localtime(int(current_time + day)))
        new_original_time = time.strftime("%H%M%S", time.localtime(int(original_time)))
        rewrite_time = int(time.mktime(datetime.datetime(
            int(new_current_time[0:4]), int(new_current_time[4:6]), int(new_current_time[6:8]),
            int(new_original_time[0:2]), int(new_original_time[2:4]), int(new_original_time[4:6])
        ).timetuple()))

        if isinstance(column, list):
            for i in column:
                line_list[int(i) - 1] = str(rewrite_time)
        else:
            line_list[int(column) - 1] = str(rewrite_time)

        if (index + 1) is line_num:
            rewrite_file.write("\t".join(line_list))
        else:
            rewrite_file.write("\t".join(line_list) + '\n')
    rewrite_file.close()


# replace_file_capturetime(originfile=r"J:\20150807_EMAIL_20150807_cjtest1001_170001_001.001.001.002.nb",newfile=r"J:\1.nb",column=[41,42],day=-1)

def replace_file_capturetime_new(originfile, newfile, column, daylist=None):
    # 修改nb或bcp文件中的capturetime
    sec_list = []
    if daylist is None:
        daylist = []
    for eachday in daylist:
        eachsec = eachday * 86400
        sec_list.append(eachsec)
    read_file = readfile(originfile)
    line_num = len(read_file)
    current_time = localtime()
    rewrite_file = codecs.open(newfile, 'w', encoding='UTF-8')
    for index, line in enumerate(read_file):
        line_list = line.split('\t')
        original_time = int(line_list[int(column) - 1])
        new_current_time = time.strftime("%Y%m%d", time.localtime(int(current_time + sec_list[index])))
        new_original_time = time.strftime("%H%M%S", time.localtime(int(original_time)))
        rewrite_time = int(time.mktime(datetime.datetime(
            int(new_current_time[0:4]), int(new_current_time[4:6]), int(new_current_time[6:8]),
            int(new_original_time[0:2]), int(new_original_time[2:4]), int(new_original_time[4:6])
        ).timetuple()))

        line_list[int(column) - 1] = str(rewrite_time)
        if (index + 1) is line_num:
            rewrite_file.write("\t".join(line_list))
        else:
            rewrite_file.write("\t".join(line_list) + '\n')
    rewrite_file.close()


# replace_file_capturetime_new(originfile=r"J:\test\fileoperation\41.nb",newfile=r"J:\test\fileoperation\2.nb",column="41",daylist=[-1,-2,-3,-1])

def sort_file_jsonColumn(file_path, column, defaltmatch='*.nb'):
    ####功能说明：读取指定路径下所有.nb后缀的文件（默认），将文件中指定列的json格式按照key排序后存储 by郭凡####
    # 读取路径下以".nb"结尾的所有文件存入列表
    list = glob.glob(file_path + os.sep + defaltmatch)
    # 遍历所有文件，进行读写操作
    for bcp in list:
        with open(bcp, 'r') as f1:
            # 将文件全部读入content
            content = f1.readlines()
        with open(bcp, 'w') as f2:
            # 逐行读取
            for line in content:
                # 将每行数据的以'\t'分隔切分后存入line列表
                line = line.split("\t")
                # 获取列数
                line_num = len(line)
                if column > line_num or column < 1:
                    raise IndexError
                else:
                    if line[column - 1].rstrip('\r\n') == '':
                        f2.write('\t'.join(line))
                    else:
                        # 将指定的json格式列进行排序
                        # strict=False表示解码时不做编码检查；sort_keys=True表示对json列做排序；ensure_ascii=False表示编码时不对ascii码做检查
                        # replace("\u0019",chr(25) 表示将acsii编码16进制的19号替换为控制符
                        line[column - 1] = ((json.dumps(json.loads(line[column - 1].rstrip('\r\n'), strict=False),
                                                        sort_keys=True, ensure_ascii=False)).replace(" ", "")).replace(
                            "\u0019", chr(25))
                        # 将替换后的整行数据逐行写入文件
                        if column == line_num:
                            # 如果为最后一列则在每行的数据结尾加换行符
                            f2.write(('\t'.join(line) + '\n').encode('utf-8'))
                        else:
                            # 如果不是最后一列，则顺序写数据
                            f2.write(('\t'.join(line)).encode('utf-8'))


def change_batch(filedir=None, condmatch=None, column=0, day=0):
    """
    #修改文件中的capturetime，支持不同后缀名的文件
    :param filedir: 文件所在路径
    :param condmatch: 后缀匹配，如果不填，则默认修改全部文件
    :param column: capturetime所在列
    :param day: 以当前时间为基准，提前或推后的天数，正数为延后，负数为提前
    :return:
    """
    day = day * 86400
    current_time = localtime()
    replace_time = current_time + int(day)
    filelist = _list_files_in_directory(filedir)
    for eachfile in filelist:
        if condmatch != "":
            if eachfile.split(".")[-1] == condmatch:
                # if eachfile == "D:\NB_APP_HARDWARESTRING\AUTH-111.bcp":
                file = FileReplace(eachfile)
                file.colreplace(column, [str(replace_time)])
        else:
            file = FileReplace(eachfile)
            file.colreplace(column, [str(replace_time)])


# change_batch(filedir=r"D:\NB_APP_HARDWARESTRING",condmatch="bcp",column=1,day=-1)

def merge_file(path, newfile_name='', postfix='*.nb', mode='w'):
    """
    #将文件夹下的指定类型文件合并
    :param path: 合并该文件夹下的文件
    :param newfile_name: 合并后的新文件存储路径和文件名，要求不能与待合并的文件同名。如果不填则默认把合并后的新文件放在path下，文件名为mergefile
    :param postfix: 合并该类型的问价
    :param mode: 写文件的方式，如果需要累加方式，则改成"a"
    :return:
    """
    if newfile_name == '':
        newfile_name = os.path.join(path, "mergefile")
    basename = _basename(newfile_name)
    with open(newfile_name, mode) as dest:
        for top, dirs, filenames in os.walk(path):
            for filename in fnmatch.filter(filenames, postfix):
                if filename == basename: continue  # 当待合并的文件名与合并后的新文件同名，跳过。
                with open(os.path.join(top, filename)) as src:  # top 为顶级目录，open里要带上文件目录
                    shutil.copyfileobj(src, dest)  # 按块读文件，不会因为文件过大而崩溃


# merge_file('J:\work\hdfs')

class FileReplace(object):
    """
    #文件替换。参数：inplace=1表示替换文件本身，默认为1.如何为0时只打印替换结果不写入文件
    函数：lineReplace 行替换
    函数：fileInsert  指定行插入
    函数：valueReplace value替换
    """

    def __init__(self, file, inplace=1):
        """
        #此类只要用于文件替换相关操作
        :param file: 文件绝对路径
        :param inplace: inplace=0表示只是输出替换，并不会替换文件本身，inplace=1表示替换文件本身
        :return:
        """
        self.__file = file
        self.__inplace = inplace

    def linereplace(self, orglinenum, newstring):
        """
        #用于行替换
        :param orglinenum: 替换行数
        :param newstring: 替换的行内容
        :return:视inplace的条件决定是输出打屏还是直接在文件中进行直接修改
        """
        for line in fileinput.input(self.__file, inplace=self.__inplace):
            if fileinput.lineno() is orglinenum:
                print newstring
            else:
                print line

    def fileinsert(self, linenos=None, strings=None):
        """
        #按照指定行插入
        :param linenos:插入的行数，支持多个 [1,2,3] [1]
        :param strings:对应插入行数的行内容 ["","",""] [""]
        :return:视inplace的条件决定是输出打屏还是直接在文件中进行直接修改
        """
        # ---complete # linenos=[1,2] strings=['test1','test2']    '指定行插入行'

        if linenos is None:
            linenos = []

        if strings is None:
            strings = []

        if os.path.exists(self.__file):
            lineno = 0
            i = 0
            for line in fileinput.input(self.__file, inplace=self.__inplace):
                lineno += 1
                line = line.strip()
                if i < len(linenos) and linenos[i] is lineno:
                    if i >= len(strings):
                        print "\n", line
                    else:
                        print strings[i]
                        print line
                    i += 1
                else:
                    print line

    def valuereplace(self, pattern, newstring, group=0):  # complete
        """
        #指定值进行替换'
        :param pattern:pattern可以是一个字符串，或者一个正则表达式
        :param newstring:对应替换成的新的字符串
        :param group:为pattern正则中的 第几个匹配块
        :return:视inplace的条件决定是输出打屏还是直接在文件中进行直接修改

        pattern可以是一个字符串，或者一个正则表达式
        如：要匹配username=123456@qq.com的123456，pattern可以写成'username=([\d]{6})@([\w]+).com',这个正则表达式有3个分组:
                group(0)表示整个正则匹配中的，就是username=123456@qq.com
                group（1）表示([\d]{6})匹配中的，就是123456
                group(2)表示([\w]+)匹配中的，就是qq
                。。。。。。以此类推。。。。。
        如果group=0，表示替换group（0）
        如果group=1，表示替换group（1）
        。。。。。以此类推。。。。。。
       """
        for line in fileinput.input(self.__file, inplace=self.__inplace, mode="rb"):

            oldstring = re.match(pattern, line)
            if oldstring:
                print re.sub(re.match(pattern, line).group(group), newstring, line).strip('\n')
            else:
                print line.strip()

    def colreplace(self, col, newstring=None, splitexp='\t'):
        """
        #指定列进行替换
        :param col: 待替换列，支持多个 [1,2,3]  [1]
        :param newstring: 替换成的新字符串  ["","",""]  [""]
        :param splitexp: 行 切割符号，默认为\t
        :return:视inplace的条件决定是输出打屏还是直接在文件中进行直接修改
        """
        if newstring is None:
            newstring = []
        if col <= 0:
            print 'param col wrong'
        else:
            for line in fileinput.input(self.__file, inplace=self.__inplace):
                if col > len(line.split(splitexp)):
                    print line.strip()
                else:
                    listline = line.split(splitexp)
                    if listline[col - 1].find('\n') >= 0:
                        # 需要判断newstring是1还是大于1
                        if len(newstring) is 1:
                            listline[col - 1] = newstring[0] + '\n'
                        elif len(newstring) is 0:
                            print 'newstring is null'
                        else:
                            listline[col - 1] = random.choice(newstring)
                    else:
                        if len(newstring) is 1:
                            listline[col - 1] = newstring[0]
                        elif len(newstring) is 0:
                            print 'newstring is null'
                        else:
                            listline[col - 1] = random.choice(newstring)
                    for i in range(len(listline)):
                        if i is not len(listline) - 1:
                            print listline[i] + splitexp,
                        else:
                            print listline[i],

    def filereplace_foronecol(self, col, newstring=None, linenum=None, splitexp='\t'):
        """
        #替换文件指定行的某一列
        filereplace_foronecol(col=15, newstring=['542301650531827'],linenum=[1], splitexp='\t')
        :param col: 待替换的一列，如 1
        :param newstring: 待替换的值，如['hello']
        :param linenum: 待替换的行，如 [2],[3,4,5]
        :param splitexp: 行 切割符号，默认为\t
        :return:
        """
        if newstring is None:
            newstring = []

        if linenum is None:
            linenum = []

        if col <= 0:
            print 'param col wrong'
        else:
            for line in fileinput.input(self.__file, inplace=self.__inplace):
                if len(linenum) is not 0:
                    if fileinput.lineno() in linenum:
                        if col > len(line.split(splitexp)):
                            print line.strip()
                        else:
                            listline = line.split(splitexp)
                            if listline[col - 1].find('\n') >= 0:
                                # 需要判断newstring是1还是大于1
                                if len(newstring) is 1:
                                    listline[col - 1] = newstring[0] + '\n'
                                elif len(newstring) is 0:
                                    print 'newstring is null'
                                else:
                                    listline[col - 1] = random.choice(newstring)
                            else:
                                if len(newstring) is 1:
                                    listline[col - 1] = newstring[0]
                                elif len(newstring) is 0:
                                    print 'newstring is null'
                                else:
                                    listline[col - 1] = random.choice(newstring)
                            for i in range(len(listline)):
                                if i is not len(listline) - 1:
                                    print listline[i] + splitexp,
                                else:
                                    print listline[i],
                    else:
                        print line.strip('\n')
                else:
                    if col > len(line.split(splitexp)):
                        print line.strip()
                    else:
                        listline = line.split(splitexp)
                        if listline[col - 1].find('\n') >= 0:
                            # 需要判断newstring是1还是大于1
                            if len(newstring) is 1:
                                listline[col - 1] = newstring[0] + '\n'
                            elif len(newstring) is 0:
                                print 'newstring is null'
                            else:
                                listline[col - 1] = random.choice(newstring)
                        else:
                            if len(newstring) is 1:
                                listline[col - 1] = newstring[0]
                            elif len(newstring) is 0:
                                print 'newstring is null'
                            else:
                                listline[col - 1] = random.choice(newstring)
                        for i in range(len(listline)):
                            if i is not len(listline) - 1:
                                print listline[i] + splitexp,
                            else:
                                print listline[i],

    def filereplace(self, cols, newstring=None, linenum=None, splitexp='\t'):
        """
        #替换文件指定行的指定列，行可为多行，列可为多列
        :param col: 待替换的一列，如 [1],[3,4]
        :param newstring: 待替换的值，如['hello'],['hello','world']
        :param linenum: 待替换的行，如 [2],[3,4,5]
        :param splitexp: 行 切割符号，默认为\t
        :return:
        """
        if newstring is None:
            newstring = []

        if linenum is None:
            linenum = []

        for i in range(len(cols)):
            self.filereplace_foronecol(int(cols[i]), [newstring[i]], linenum, splitexp)


class ConfFileReplace(object):
    def __init__(self, ipup=None):
        """
        构造函数，此类目前支持linux文件的替换备份和还原
        :param ipup:目的ip地址
        :param sourcefile:待上传的文件
        :param dstfile:目的文件
        :return:无
        """
        self._ipup = ipup.strip()
        self.cmd = _SSH()
        self.cmd.connect(self._ipup)

    def backup(self, dst=None, ismvpath=None):  # assert
        """
        用于linux系统中的文件或者目录备份
        :param dst:待备份的文件或者目录，类型str，如果是目录请不要写成/home/123/ 写成/home/123
        :param ismvpath:两种备份模式，第一种直接将文件或者目录备份中*_ATBACKUP，第二种即传入此参数值，将文件或者目录拷贝至此临时目录进行备份
        :return:assert式返回
        """
        isfile_status = self.cmd.isfile(dst)
        isdir_status = self.cmd.isdir(dst)
        self.ismvpath = ismvpath
        if isfile_status[0] is 0:  # 判断是否存在，存在才备份
            if ismvpath != None:
                status, stdout, stderr = self.cmd.mv(dst, ismvpath)
                assert status == 0, (stdout, stderr)
            else:
                status, stdout, stderr = self.cmd.mv(dst, dst + "_ATBACKUP")
                assert status == 0, (stdout, stderr)
        if isdir_status[0] is 0:
            if dst[-1] == "/":
                dst = dst[:-1]
            if ismvpath != None:
                status, stdout, stderr = self.cmd.mv(dst, ismvpath)
                assert status == 0, (stdout, stderr)
            else:
                status, stdout, stderr = self.cmd.mv(dst, dst + "_ATBACKUP")
                assert status == 0, (stdout, stderr)

    def upload(self, source, dst):  # assert
        """
        上传
        :param source:待上传文件或者目录，类型str
        :param dst:上传目的路劲，类型str
        :return:assert式返回
        """
        status, stdout, stderr = _scp_put(self._ipup, source, dst)
        assert status == 0, (stdout, stderr)

    def restore(self, dst):  # assert
        """
        还原,目录不要带最后一个分隔符  如\ /
        :param dst:需要还原的文件或者目录，如果是目录请不要写成/home/123/ 写成/home/123，类型str
        :return:assert式返回
        """
        if self.ismvpath == None:
            isfile_status = self.cmd.isfile(dst + "_ATBACKUP")
            isdir_status = self.cmd.isdir(dst + "_ATBACKUP")
            if isfile_status[0] is 0 or isdir_status[0] is 0:
                status, stdout, stderr = self.cmd.mv(dst + "_ATBACKUP", dst)
                assert status == 0, (stdout, stderr)
        else:
            isfile_status = self.cmd.isfile(self.ismvpath + "/" + _basename(dst))
            isdir_status = self.cmd.isdir(self.ismvpath + "/" + _basename(dst))
            if isfile_status[0] is 0 or isdir_status[0] is 0:
                status, stdout, stderr = self.cmd.mv(self.ismvpath + "/" + _basename(dst), _dirname(dst))
                assert status == 0, (stdout, stderr)

    def restartpro(self, proname):  # assert
        """
        杀进程
        :param proname: fude的进程名 类型str
        :return: aseert式返回
        """
        self._ipupfude = Fude(self._ipup)
        status, stdout, stderr = self._ipupfude.kill(proname)
        assert status == 0, (stdout, stderr)

    def pkill(self, proname_pkill):
        """
        杀进程
        :param proname_pkill:pkill 能跟的进程名 类型str
        :return: aseert式返回
        """
        return self.cmd.exec_command("pkill " + proname_pkill)


if __name__ == '__main__':
    a = FileReplace('E:\data_ds_test\NB_APP_HERO_TRAIN_RELINFO-1508568423-20171021-0.nb', inplace=1)
    a.filereplace_foronecol(col=15, newstring=['542301650531827'],linenum=[1], splitexp='\t')
