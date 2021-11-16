import ipaddress

from common.utils import load_json
from config import settings


data_dir = settings.data_storage_dir

# from https://github.com/al0ne/Vxscan/blob/master/lib/iscdn.py
cdn_ip_cidr = load_json(data_dir.joinpath("cdn_ip_cidr.json"))


def is_cdn(args: str) -> bool:
    """判断CIDR/IP是否为CDN

    :param str args :  IP/CIDR string
    :rtype  : bool
    """
    network_address = ipaddress.ip_address(args.split("/")[0])
    for cdn_cidr in cdn_ip_cidr:
        if network_address in ipaddress.ip_network(cdn_cidr):
            return True
    return False
