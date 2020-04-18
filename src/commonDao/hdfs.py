# -*- coding: utf-8 -*-
"""
@author wangxiaotao
created on 2017-11-14
"ssh远程Hadoop集群的方式造数据，创建目录、上传数据、删除目录、"
"""
import paramiko
import logging
from commonFunc import md5_sth


class HdfsPositionDo(object):
    def __init__(self, host, username, password, port=22):
        """
        构造函数
        :param host:
        :param username:
        :param password:
        :param port:
        :return:
        """
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(host, int(port), username, password)

    def mkdir(self, command):
        """
        hadoop文件夹创建
        :param command:创建的文件夹路径
        :return:
        """
        mkdir_str_f = 'hadoop fs -mkdir -p '
        mkdir_l = '/opt/software/hadoop/hadoop-2.6.0/bin/' + mkdir_str_f + command + '\n'
        logging.debug(u'创建文件夹的命令为{0}'.format(mkdir_l))
        stdin, stdout, stderr = self.ssh.exec_command(mkdir_l)
        err = stderr.readlines()
        out = stdout.readlines()
        if (err):
            logging.error(u'查询出错{0}'.format(err))
        else:
            logging.info(u'成功创建目录{0}'.format(mkdir_l))
            return str(out).decode('string_escape')

    def put(self, file_path, dir):
        """
        hadoop上传文件，hadoop fs -put
        :param file_path: 需要上传的文件绝对路径，在远程的机器本地
        :param dir: 需要上传到的文件夹
        :return:
        """
        put_str = '/opt/software/hadoop/hadoop-2.6.0/bin/' + 'hadoop fs -put ' + file_path + ' ' + dir + '\n'
        logging.debug(u'上传文件的命令为{0}'.format(put_str))
        stdin, stdout, stderr = self.ssh.exec_command(put_str)
        err = stderr.readlines()
        out = stdout.readlines()
        if (err):
            logging.error(u'查询出错{0}'.format(err))
        else:
            logging.info(u'成功上传文件到{0}'.format(put_str))
            return str(out).decode('string_escape')

    def remove(self, path):
        """
        hadoop删除文件夹，hadoop fs -rm -r
        :param path:
        :return:
        """
        remove_str = '/opt/software/hadoop/hadoop-2.6.0/bin/' + 'hadoop fs -rm -r ' + path + '\n'
        logging.info(u'将要移除的文件夹为{0}'.format(remove_str))
        stdin, stdout, stderr = self.ssh.exec_command(remove_str)
        err = stderr.readlines()
        out = stdout.readlines()
        if (err):
            logging.error(u'查询出错{0}'.format(err))
        else:
            return str(out).decode('string_escape')

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

    def query_hbase(self, attribute_value):
        md5_string = '{0}\t01'.format(attribute_value)
        last_string = md5_sth(md5_string)
        command = "cd /home/nebula/NebulaPF_DataCenter_Gaia/tool/\nsh simple_query.sh t#NB_APP_RPERSON_EXACT " \
                  "c#MD_ID:'{0}' isAllReturn#true"\
            .format(last_string)
        # command = "sh /home/nebula/NebulaPF_DataCenter_Gaia/tool/simple_query.sh t#NB_APP_RPERSON_EXACT " \
        #           "c#MD_ID:'{0}' isAllReturn#true"\
        #     .format(last_string)
        print command
        stdin, stdout, stderr = self.ssh.exec_command(command)
        err = stderr.readlines()
        out = stdout.readlines()
        if (err):
            logging.error(u'查询出错{0}'.format(err))
        else:
            return str(out).decode('string_escape')

    def ssh_close(self):
        self.ssh.close()

if __name__ == '__main__':
    from commonFunc import get_config
    host = get_config('HDFS', 'host', '../Config/HDFS.conf')
    port = get_config('HDFS', 'port', '../Config/HDFS.conf')
    username = get_config('HDFS', 'username', '../Config/HDFS.conf')
    password = get_config('HDFS', 'password', '../Config/HDFS.conf')
    HPD = HdfsPositionDo(host, username, password, port)
    HPD.query_hbase('650202199511281621')
