import json
import csv
import time

from config import settings
from config.log import logger


# 生成json结果文件
def json_report(data: list, path: str, encode: str = "utf-8") -> str:
    filename = (
        f'all_cidr_result_{time.strftime("%Y%m%d_%H%M%S", time.localtime())}.json'
    )
    result_json = f"{path}/{filename}"
    with open(result_json, mode="w", encoding=encode) as json_file:
        json.dump(data, json_file)
    return result_json


# 生成csv结果文件
def csv_report(data: list, path: str, encode: str = "utf-8") -> str:
    filename = f'all_cidr_result_{time.strftime("%Y%m%d_%H%M%S", time.localtime())}.csv'
    result_csv = f"{path}/{filename}"
    field = [
        "cidr",
        "ip",
        "domain",
        "localtion",
        "isp",
        "cdn",
    ]
    with open(result_csv, mode="w", encoding=encode) as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=field)
        writer.writeheader()
        for itm in data:
            writer.writerow(itm)
    return result_csv


# 入口
def entrance(
    data: list,
    path: str = settings.result_save_path,
    fmt: str = settings.result_save_format,
    encode: str = settings.result_save_encode,
) -> str:
    # 用于匹配文件格式与函数
    match = {"csv": csv_report, "json": json_report}

    # 调用对应函数
    logger.log("INFOR", "Start exporting results")
    try:
        if fmt in match:
            filepath = match[fmt](data, path, encode)
            logger.log("ALERT", f"The work result: {filepath}")
        else:
            logger.log("ERROR", "Bad file format")
    except Exception as identifier:
        logger.log("ERROR", repr(identifier))
        filepath = identifier

    return filepath
