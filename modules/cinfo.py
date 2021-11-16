from common.ipreg import IpRegData
from common.check import is_cdn


def search(datas: dict) -> dict:
    q = IpRegData()
    for cidr in datas:
        res = is_cdn(cidr)
        info = q.query(cidr.split("/")[0])
        for ip in datas[cidr]:
            datas[cidr][ip]["localtion"] = info.get("addr")
            datas[cidr][ip]["isp"] = info.get("isp")
            datas[cidr][ip]["cdn"] = res

    return datas
