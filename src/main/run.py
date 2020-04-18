# -*- coding: utf-8 -*-
"""
@author wangxiaotao
@version 0.0.3
created on 2018-02-28
"运行主程序"
"""
import logging.config
from src.dataDao.txt_data_birth import TxtBirth as tb
from src.commonDao.commonFunc import CommonUtil as cul

try:
    logging.config.fileConfig("../Config/txt_data_birth_log.conf")
    logger = logging.getLogger("root")
except Exception as e:
    print e
    logging.basicConfig(level=logging.info,
                        format="%(asctime)s %(funcName)s:%(lineno)d %(levelname)s:%(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S")
    logging.exception(e)

def run():
    """
    运行主函数
    :return:None
    """
    line = cul.get_config('data_platform', 'txt_line', file_path='../Config/config.conf')
    table_name = cul.get_config('data_platform', 'table_name', file_path='../Config/config.conf')
    _format = cul.get_config('data_platform', 'format', file_path='../Config/config.conf')
    _field_split = cul.get_config('data_platform', 'field_split', file_path='../Config/config.conf')
    if _field_split == '' or _field_split == '\t':
        _field_split_n = '\t'
    else:
        _field_split_n = _field_split
    _excel_path = cul.get_config('data_platform', 'excel_path', file_path='../Config/config.conf')
    # 读取配置文件，判断是否存在逗号，若存在，则table_name转为列表类型
    if ',' in table_name:
        table_name = table_name.split(',')
    tb().txt_birth(line=int(line), table_name=table_name, format=_format, field_split=_field_split_n,
                   file_path=_excel_path)

if __name__ == '__main__':
    run()

