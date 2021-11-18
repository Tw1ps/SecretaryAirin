import json
import time
from typing import Dict, List

import pandas as pd
from pandas import DataFrame

from config import settings
from config.log import logger


class Exporter(object):
    def __init__(self, data: Dict[str, list] = None, **kwargs: dict) -> None:
        """
        基于pandas的结果生成器，目前支持XLSX/CSV/JSON

        数据格式为 {"表名1": 可被DataFrame转换的输出数据, "表名2": 同1}

        Just like {"Sheet1": [{"name": "Litiansuo", "age": 24, "position": "student"}]}

        :param str      filename :   As literally
        :param str      fmt      :   Result format (default excel), support excel/csv/json
        :param str      path     :   Result path (default None, automatically generated)
        :param bool     index    :   As literally
        :param bool     header   :   As literally
        """
        self.data = data
        self.path: str = kwargs.get("path")
        self.fmt: str = kwargs.get("fmt")
        self.filename: str = kwargs.get("filename")
        self.index: bool = kwargs.get("index")
        self.header: bool = kwargs.get("header")
        self.results_paths = list()
        self.callable = dict()

    def config_param(self) -> None:
        if self.fmt == None:
            self.fmt = settings.results_save_format
        if self.path == None:
            self.path = settings.results_save_path
        if self.index == None:
            self.index = settings.results_save_with_index
        if self.header == None:
            self.header = settings.results_save_with_header
        if self.filename == None:
            self.filename = f'all_statistics_results_{time.strftime("%Y%m%d_%H%M%S", time.localtime())}'

        self.callable.update(
            {
                "csv": self.to_csv,
                "json": self.to_json,
                "xlsx": self.to_excel,
            }
        )

    def check_param(self) -> None:
        if self.fmt.lower() not in self.callable:
            logger.log(
                "ALERT",
                f"Format {self.fmt} not found, use {settings.results_save_format}",
            )
            self.fmt = settings.results_save_format

    @staticmethod
    def to_excel(
        data: Dict[str, list],
        path: str,
        filename: str,
        index: bool = False,
        header: bool = True,
    ) -> List[str]:
        results_paths = list()
        fullpath = f"{path}/{filename}.xlsx"
        results_paths.append(fullpath)
        ew = pd.ExcelWriter(fullpath)

        for itm in data:
            df = DataFrame(data.get(itm))
            df.to_excel(ew, sheet_name=itm, index=index, header=header)

        ew.save()
        ew.close()
        return results_paths

    @staticmethod
    def to_csv(
        data: Dict[str, list],
        path: str,
        filename: str,
        index: bool = False,
        header: bool = True,
    ) -> List[str]:
        results_paths = list()

        for itm in data:
            fullpath = f"{path}/{filename}_{itm}.csv"
            results_paths.append(fullpath)
            df = DataFrame(data.get(itm))
            df.to_csv(fullpath, index=index, header=header)

        return results_paths

    @staticmethod
    def to_json(
        data: Dict[str, list], path: str, filename: str, **kwargs: dict
    ) -> List[str]:
        """
        Just call json.dump(data)

        Not pandas

        Args:
            data (Dict[str, list]): [description]
            path (str): [description]
            filename (str): [description]

        Returns:
            List[str]: [description]
        """
        results_paths = list()
        fullpath = f"{path}/{filename}.json"
        results_paths.append(fullpath)

        with open(fullpath, mode="w") as json_file:
            json.dump(data, json_file)

        return results_paths

    def main(self) -> None:
        kwargs = dict()
        kwargs["data"] = self.data
        kwargs["path"] = self.path
        kwargs["filename"] = self.filename
        kwargs["index"] = self.index
        kwargs["header"] = self.header
        self.results_paths = self.callable[self.fmt](**kwargs)

    def run(self) -> None:
        logger.log("INFOR", "Start exporting results")
        try:
            self.config_param()
            self.check_param()
            self.main()
            for fullpath in self.results_paths:
                logger.log("ALERT", f"The work result: {fullpath}")
        except Exception as identifier:
            logger.log("ERROR", repr(identifier))

        return self.results_paths
