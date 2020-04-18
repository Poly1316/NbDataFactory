# 代码运行环境构建
1. 若要使用该平台时，需要安装64位python2.7环境或联系测试部汪啸涛获取env虚拟环境
1. 在代码所在目录执行，其中--find-links需要修改为AllPackages所在目录</br>
    pip install -r requirements.txt -I --no-index --find-links=AllPackages所在路径
1. 数据生成请先在/Config/table_fields.xls配置字段类型，在/Config/config.conf配置table_name字段，然后运行/main/run.py即可生成所需txt或者nb文件；如果字段不符合需求，可以在/Conf/data_task.conf配置字段参数，修正数据类型

# 代码功能介绍
&emsp;&emsp;该工具主要作用是方便业务测试过程中数据的构造，大数据应用项目存在较多部分功能需要造大量数据，耗时耗力，所以设计该工具，简化数据构造过程。该工具主要通过读取Excel表字段，通过指定各字段关键词，自动生成符合要求的数据类型。该工具主要支持构造的数据类型如下：</br>
&emsp;&emsp;1. 可构造后缀为nb、bcp、txt等文本类格式数据，文本分隔符自定义；</br>
&emsp;&emsp;2. 支持构造生成数据SQL，使用使用直接拿着对应SQL文件去需要生成数据的数据库执行即可。

## 生成文本类数据配置方式