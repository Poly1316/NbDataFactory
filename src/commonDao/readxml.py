#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author wangxiaotao
Created on 2018-01-24
"读取xml文件公共方法"
"""
from xml.etree.ElementTree import ElementTree, Element


class ReadXml(object):
    def __init__(self, in_path):
        """
        读取并解析xml文件
        in_path: xml路径
        return: ElementTree
        """
        self.tree = ElementTree()
        self.tree.parse(in_path)

    def get_root(self):
        return self.tree.getroot()

    def write_xml(self, out_path):
        """将xml文件写出
        tree: xml树
        out_path: 写出路径
        """
        self.tree.write(out_path, encoding="utf-8", xml_declaration=True)

    def if_match(self, node, kv_map):
        """判断某个节点是否包含所有传入参数属性
           node: 节点
           kv_map: 属性及属性值组成的map"""
        for key in kv_map:
            if node.get(key) != kv_map.get(key):
                return False
        return True


    # ---------------search -----

    def find_nodes(self, path, fa=None):
        """查找某个路径匹配的所有节点
           tree: xml树
           path: 节点路径"""
        if fa is None:
            return self.tree.findall(path)
        else:
            return fa.findall(path)


    def get_node_by_keyvalue(self, nodelist, kv_map):
        """根据属性及属性值定位符合的节点，返回节点
           nodelist: 节点列表
           kv_map: 匹配属性及属性值map"""
        result_nodes = []
        for node in nodelist:
            if self.if_match(node, kv_map):
                result_nodes.append(node)
        return result_nodes


    # ---------------change -----

    def change_node_properties(self, nodelist, kv_map, is_delete=False):
        """修改/增加 /删除 节点的属性及属性值
           nodelist: 节点列表
           kv_map:属性及属性值map"""
        for node in nodelist:
            for key in kv_map:
                if is_delete:
                    if key in node.attrib:
                        del node.attrib[key]
                else:
                    node.set(key, kv_map.get(key))


    def change_node_text(self, nodelist, text, is_add=False, is_delete=False):
        """改变/增加/删除一个节点的文本
           nodelist:节点列表
           text : 更新后的文本"""
        for node in nodelist:
            if is_add:
                node.text += text
            elif is_delete:
                node.text = ""
            else:
                node.text = text


    def create_node(self, tag, property_map, content):
        """新造一个节点
           tag:节点标签
           property_map:属性及属性值map
           content: 节点闭合标签里的文本内容
           return 新节点"""
        element = Element(tag, property_map)
        element.text = content
        return element


    def add_child_node(self, nodelist, element):
        """给一个节点添加子节点
           nodelist: 节点列表
           element: 子节点"""
        for node in nodelist:
            node.append(element)


    def del_node_by_tagkeyvalue(self, nodelist, tag, kv_map=None):
        """同过属性及属性值定位一个节点，并删除之
           nodelist: 父节点列表
           tag:子节点标签
           kv_map: 属性及属性值列表"""
        for parent_node in nodelist:
            children = parent_node.getchildren()
            for child in children:
                if kv_map is None:
                    if child.tag == tag:
                        parent_node.remove(child)
                else:
                    if child.tag == tag and if_match(child, kv_map):
                        parent_node.remove(child)


if __name__ == "__main__":
    # 1. 读取xml文件  
    rx = ReadXml("../Config/data_task.xml")
    root = rx.get_root()
    print root

    # 2. 属性修改  
    # A. 找到父节点  
    nodes = rx.find_nodes("tables")[0]
    print nodes
    # for __node in nodes:
    #     for __a in __node.iter():
    #         print __a.text
    # B. 通过属性准确定位子节点
    # result_nodes = get_node_by_keyvalue(nodes, {"name": "sh_mh_passenger_in_dz"})
    # print result_nodes
    # # C. 修改节点属性
    # change_node_properties(result_nodes, {"age": "1"})
    # D. 删除节点属性
    # change_node_properties(result_nodes, {"value": ""}, True)
    #
    # 3. 节点修改
    # A.新建节点
    a = rx.create_node("field", {"name": "sh_mh_passenger_in_dz_1", "type":u"随机整数"}, "\n\t\t")
    # B.插入到父节点之下
    rx.add_child_node(root, a)
    nodes = rx.find_nodes("field", fa=nodes)
    print nodes
    b = rx.get_node_by_keyvalue(nodes, {"name":"sh_mh_passenger_in_dz_1"})
    print b
    bb = rx.create_node("tab1", {}, "123")
    rx.add_child_node(b, bb)
    # nodes = find_nodes(nodes, "fields")
    # __nodes = get_node_by_keyvalue(nodes, {"name": "15"})
    # print __nodes
    # a = create_node("field", {"name": "credit_id"}, "0")
    # add_child_node(__nodes, a)
    # __nodes = get_node_by_keyvalue(nodes, {"name": "credit_id"})
    # a = create_node("tag1", {"name", "uuu"}, "15")
    # add_child_node(nodes, a)


    # 4. 删除节点  
    # # 定位父节点
    # del_parent_nodes = find_nodes(tree, "fields")
    # print del_parent_nodes
    # # 准确定位子节点并删除之
    # del_node_by_tagkeyvalue(del_parent_nodes, "field")

    # 5. 修改节点文本  
    # 定位节点  
    # text_nodes = get_node_by_keyvalue(find_nodes(tree, "processers/services/service/chain"), {"sequency": "chain3"})
    # change_node_text(text_nodes, "new text")

    # 6. 输出到结果文件  
    rx.write_xml("./out.xml")

