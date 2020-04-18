#coding=utf-8
# author: chenfei 2018-3-22 9:44:02
# 读取配置文件
import ConfigParser
import traceback
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('Reader')

class ReadConfig(object):
    def __init__(self, conf):
        self.conf = conf
        self._read()

    def _read(self):
        self.cf = ConfigParser.ConfigParser()
        try:
            self.cf.read(self.conf)
        except ConfigParser.ParsingError, e:
            logger.info('解析配置文件{}失败，请检查配置文件格式！'.format(self.conf))
            logger.error(traceback.format_exc())

    def get_sections(self):
        return self.cf.sections()

    def get_options_by_section(self, section):
        return self.cf.options(section)

    def get_items_by_section(self, section):
        data = {}
        items = self.cf.items(section)
        for line in items:
            key = line[0]
            value = line[1]
            if isinstance(value, list):
                value = value[0]
            if value.find(':false') > 0:
                value = value.replace(':false',':False')
            if value == 'self': # 如果eval('self')会变成一个实例对象
                data[key] = value
                continue
            try:
                data[key] = eval(value)
            except:
                data[key] = value
        return data

    def set_value(self, section, key, value):
        return self.cf.set(section, key, value)

    def set_value_updated(self, section, key, value):
        self.cf.set(section, key, value)
        with open(self.conf, 'w') as f:
            self.cf.write(f)


class Reader(ReadConfig):
    def __init__(self, conf):
        super(Reader, self).__init__(conf)
        self.config = self.get_all()

    def get_all(self):
        config = {}
        for section in self.get_sections():
            config[section] = self.get_items_by_section(section)
        return config
