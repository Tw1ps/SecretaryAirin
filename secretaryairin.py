#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import fire
from datetime import datetime

from common.utils import load_txt

from modules import analyzer, export
from modules import cinfo

from config import settings
from config.log import logger


red = "\033[1;31m"
yellow = "\033[01;33m"
blue = "\033[01;34m"
end = "\033[0m"

secretary_banner = f"""{red}
 _____                 _               _____ _     _     
|   __|___ ___ ___ ___| |_ ___ ___ _ _|  _  |_|___|_|___ {yellow}
|__   | -_|  _|  _| -_|  _| .'|  _| | |     | |  _| |   |{blue}
|_____|___|___|_| |___|_| |__,|_| |_  |__|__|_|_| |_|_|_|
                                  |___|                  {end}
"""


class SecretaryAirin(object):
    """
    SecretaryAirin help summary page

    SecretaryAirin is a ip address statistics tool

    Example:
        python3 airin.py www.example.com - run
        python3 airin.py ./domains.txt - run
        python3 airin.py 192.168.0.0/24 - run
        python3 airin.py ./list.txt --path . - run
        python3 airin.py ./list.txt --fmt json - run

    Note:
        " - run" is a fixed format
        --fmt   csv/json (result format)
        --path  Result path (default None, automatically generated)
    """

    def __init__(self, *args: tuple, fmt: str = None, path: str = None, **kwargs: dict):
        """
        :param tuple    *args    :   One or more IP/CIDR/DOMAIN/URL or File path of .txt
        :param str      fmt      :   Result format (default csv)
        :param str      path     :   Result path (default None, automatically generated)
        """
        self.args = args
        self.kwargs = kwargs
        self.fmt = fmt
        self.path = path
        self.datas = list()
        self.__str_list = list()

    def config_param(self):
        """
        Config parameter
        """
        if self.path is None:
            self.path = settings.result_save_path
        if self.fmt is None:
            self.fmt = settings.result_save_format

    def check_param(self):
        """
        Check parameter
        """
        if len(self.args) == 0:
            logger.log("FATAL", "You least provide one targets parameter")
            exit(1)

    def load_data(self):
        """
        Load file data
        """
        logger.log("DEBUG", f"Arguments: {self.args}")
        for itm in self.args:
            if itm.endswith(".txt"):
                self.__str_list += load_txt(itm)
            else:
                self.__str_list.append(itm)

    def main(self):
        """
        Main function
        """
        datas = analyzer.analysis(self.__str_list)

        datas = cinfo.search(datas)

        datas = analyzer.data_sort(datas)
        analyzer.data_statistics(datas)
        self.datas = analyzer.data_conversion(datas)

        export.entrance(self.datas, self.path, self.fmt)

        return self.datas

    def run(self):
        """
        SecretaryAirin running entrance
        """
        print(secretary_banner)
        dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[*] Starting SecretaryAirin @ {dt}\n")
        logger.log("INFOR", "Start running SecretaryAirin")

        self.config_param()
        self.check_param()
        self.load_data()
        self.main()

        logger.log("INFOR", "Finished SecretaryAirin")


if __name__ == "__main__":
    fire.Fire(SecretaryAirin)
