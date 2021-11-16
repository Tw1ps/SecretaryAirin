import json
import ipaddress


def load_txt(filepath: str, encode: str = "utf-8") -> list:
    """
    读取txt文件内容并转为list

    :param str filepath :  .txt filepath
    :return : txt to list data
    :rtype  : list
    """
    data = list()
    try:
        with open(filepath, mode="r", encoding=encode) as txt_file:
            data = txt_file.read().split("\n")
    except Exception as identifier:
        if encode != "GBK":
            data = load_txt(filepath, "GBK")
    return data


def load_json(filepath: str, encode: str = "utf-8"):
    data = None
    try:
        with open(filepath, mode="r", encoding=encode) as json_file:
            data = json.load(json_file)
    except Exception as identifier:
        if encode != "GBK":
            data = load_json(filepath, "GBK")
    return data


def deduplicate(data: list) -> list:
    """
    去除list中的重复数据
    """
    result = list(set(data))
    if '' in result:
        result.remove('')
    return result


def cidr_to_iplist(cidr: str) -> list:
    result = None
    ip_list = ipaddress.ip_network(cidr)
    result = list(ip_list)
    result.remove(ip_list.network_address)
    result.remove(ip_list.broadcast_address)
    return result
