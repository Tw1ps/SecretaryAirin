import re
import ipaddress

from typing import List

from modules.resolve import Resolve

from config.log import logger


ISIPV4_1 = 1
ISIPV4_2 = 2
ISIPV4_3 = 3
ISIPV4_4 = 4
ISIPV4_5 = 5
ISCIDR = 6
ISDOMAIN = 7
ISURL = 8

ip_list = list()
domain_list = list()


def data_sort(data: dict, reverse: bool = True) -> dict:
    """
    数据排序，将数据按照ip数量排序

    :param dict data    :  dict
    :param bool reverse :  顺序或倒序
    :return : 经排序的数据
    :rtype  : dict
    """
    try:
        sort_data = sorted(data.items(), key=lambda x: len(x[1]), reverse=reverse)
        return dict(sort_data)
    except Exception as identifier:
        logger.log("ERROR", repr(identifier))
    return data


def data_statistics(data: dict) -> None:
    ipcount = 0
    for itm in data:
        ip_list = data.get(itm)
        first_data = list(ip_list.items())[0][0]
        info = data.get(itm).get(first_data)
        logger.log(
            "INFOR",
            f"CIDR: {itm}  \tIP count: {len(ip_list)}\tLocaltion: {info.get('localtion')}\tISP: {info.get('isp')}\tCDN: {info.get('cdn')}",
        )
        ipcount += len(ip_list)

    logger.log("ALERT", f"CIDR total: {len(data)} \tIP total: {ipcount}")
    logger.log("TRACE", f"Data: {data}")


def data_conversion(datas: dict) -> list:
    results = list()
    for cidr in datas:
        for ip in datas[cidr]:
            if len(datas[cidr][ip]["domain"]):
                for domain in datas[cidr][ip]["domain"]:
                    results.append(
                        {
                            "cidr": cidr,
                            "ip": ip,
                            "domain": domain,
                            "localtion": datas[cidr][ip].get("localtion"),
                            "isp": datas[cidr][ip].get("isp"),
                            "cdn": datas[cidr][ip].get("cdn"),
                        }
                    )
            else:
                results.append(
                    {
                        "cidr": cidr,
                        "ip": ip,
                        "domain": None,
                        "localtion": datas[cidr][ip].get("localtion"),
                        "isp": datas[cidr][ip].get("isp"),
                        "cdn": datas[cidr][ip].get("cdn"),
                    }
                )

    return results


def analy_ipv4_1(args: str) -> None:
    ip_list.append(args.split(":")[0])
    return None


def analy_ipv4_2(args: str) -> None:
    src, dst = args.split("-")
    lsrc = [int(i) for i in src.split(".")]
    ldst = [int(i) for i in dst.split(".")]
    if lsrc[-2] < ldst[-2]:
        tmp = lsrc[-2]
        while tmp <= ldst[-2]:
            cidr = ".".join([str(i) for i in lsrc[0:2]])
            ip_list.extend([ip for ip in ipaddress.ip_network(f"{cidr}.{tmp}.0/24")])
            tmp += 1
    elif lsrc[-1] < ldst[-1]:
        tmp = lsrc[-1]
        while tmp <= ldst[-1]:
            ip_list.append(f'{".".join([str(i) for i in lsrc[0:3]])}.{tmp}')
            tmp += 1
    else:
        ip_list.extend([src, dst])
    return None


def analy_ipv4_3(args: str) -> None:
    src, dst = args.split("-")
    lsrc = [int(i) for i in src.split(".")]
    ldst = int(dst)
    if lsrc[-1] < ldst:
        tmp = lsrc[-1]
        while tmp <= ldst:
            ip_list.append(f'{".".join([str(i) for i in lsrc[0:3]])}.{tmp}')
            tmp += 1
    else:
        ip_list.append(src)
    return None


def analy_ipv4_4(args: str) -> None:
    ip_list.extend(args.split("/"))
    return None


def analy_ipv4_5(args: str) -> None:
    ip_list.append(re.search("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", args).group(0))
    return None


def analy_cidr(args: str) -> None:
    while True:
        try:
            ip_list.extend([ip for ip in ipaddress.ip_network(args)])
            break
        except Exception as identifier:
            tmp = args.split(".")
            c = tmp[:3]
            e, mask = tmp[-1].split("/")
            if int(e) == 0:
                break
            old_args = args
            args = f'{".".join(c)}.{int(e) - 1}/{mask}'
            logger.log("DEBUG", f"Bad CIDR: {old_args}, try {args}")
            logger.log("DEBUG", repr(identifier))
    return None


def analy_url(args: str) -> None:
    domain_list.append(args.split(":")[1][2:].split("/")[0])
    return None


def analy_domain(args: str) -> None:
    domain = args.split(":")[0].split("/")[0]
    if domain.endswith("."):
        domain = domain[:-1]
    domain_list.append(domain)
    return None


# 用于兼容各种令人窒息的列表（厚礼蟹）

# 10.1.1.1
ipv4_pattern1 = "^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}[:]{0,1}\d{0,5}$"
# 10.1.1.1-10.1.1.255
ipv4_pattern2 = (
    "^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}-\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$"
)
# 10.1.1.1-254
ipv4_pattern3 = "^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}-\d{1,3}$"
# 10.1.1.1/10.0.0.2
ipv4_pattern4 = (
    "^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$"
)
# http://10.0.0.1/test
ipv4_pattern5 = "^http[s]{0,1}://\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}.*$"
# 10.0.0.0/24
cidr_pattern = "^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/\d{1,2}$"
# http://example.com
url_pattern = "^http[s]{0,1}://.*$"
# example.com
domain_pattern = "^.*?\..*$"


def match_type(args: str) -> int:
    if re.match(ipv4_pattern1, args):
        return ISIPV4_1
    elif re.match(ipv4_pattern2, args):
        return ISIPV4_2
    elif re.match(ipv4_pattern3, args):
        return ISIPV4_3
    elif re.match(ipv4_pattern4, args):
        return ISIPV4_4
    elif re.match(ipv4_pattern5, args):
        return ISIPV4_5
    elif re.match(cidr_pattern, args, re.I):
        return ISCIDR
    elif re.match(url_pattern, args, re.I):
        return ISURL
    elif re.match(domain_pattern, args, re.I):
        return ISDOMAIN
    else:
        return 0


def pretreatment(data: str) -> List[str]:
    """他可能是一行写了很多个IP，搜谢特\n
    比如\n
    10.0.0.1 10.0.0.2 10.0.0.1;100.0.0.2,200.0.0.1 ; 100.0.2.3\n
    还要注意全角的标点符号

    Args:
        data (str): 一行数据

    Returns:
        List[str]: 处理，一定要处理
    """
    ret = list(
        set(
            data.replace(" ", "\n")
            .replace(";", "\n")
            .replace("、", "\n")
            .replace(",", "\n")
            .replace("，", "\n")
            .replace("；", "\n")
            .split("\n")
        )
    )
    if "" in ret:
        ret.remove("")
    return ret


def reduce(ip_list: list, domain_dict: dict = None) -> dict:
    datas = dict()
    for ip in ip_list:
        ip = str(ip)
        cidr = f'{".".join(ip.split(".")[:3])}.0/24'
        if cidr not in datas:
            datas[cidr] = dict()
        if ip not in datas[cidr]:
            datas[cidr].update(
                {ip: {"domain": list(), "cdn": None, "localtion": None, "isp": None}}
            )
    for domain in domain_dict:
        tmp = domain_dict.get(domain)
        if type(tmp) == str:
            cidr = f'{".".join(ip.split(".")[:3])}.0/24'
            if cidr not in datas:
                datas[cidr] = dict()
            if ip not in datas[cidr]:
                datas[cidr].update(
                    {
                        ip: {
                            "domain": [domain],
                            "cdn": None,
                            "localtion": None,
                            "isp": None,
                        }
                    }
                )
            else:
                datas[cidr][ip]["domain"].append(domain)
        elif type(tmp) == list:
            for ip in tmp:
                cidr = f'{".".join(ip.split(".")[:3])}.0/24'
                if cidr not in datas:
                    datas[cidr] = dict()
                if ip not in datas[cidr]:
                    datas[cidr].update(
                        {
                            ip: {
                                "domain": [domain],
                                "cdn": None,
                                "localtion": None,
                                "isp": None,
                            }
                        }
                    )
                else:
                    datas[cidr][ip]["domain"].append(domain)
    return datas


forward = {
    ISIPV4_1: analy_ipv4_1,
    ISIPV4_2: analy_ipv4_2,
    ISIPV4_3: analy_ipv4_3,
    ISIPV4_4: analy_ipv4_4,
    ISIPV4_5: analy_ipv4_5,
    ISCIDR: analy_cidr,
    ISDOMAIN: analy_domain,
    ISURL: analy_url,
}


def analysis(datas: List[str]):
    logger.log("INFOR", "Start analysis")
    for item in datas:
        for itm in pretreatment(item):
            flag = match_type(itm)
            if flag:
                forward.get(flag)(itm)
            else:
                logger.log("DEBUG", f"Dad arguments: {itm}")
    logger.log("INFOR", "Finished analysis")

    domain_dict = dict()
    if len(domain_list):
        resolver = Resolve(domain_list)
        domain_dict = resolver.run()

    datas = reduce(ip_list, domain_dict)
    return datas
