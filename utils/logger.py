# -*- coding: utf-8 -*-

import logging


# class Logger:
#     @staticmethod
def logger(level=logging.DEBUG, logPath=None):
    # LOG_FORMAT = "%(asctime)s %(name)s %(levelname)s %(pathname)s %(message)s "  # 配置输出日志格式
    LOG_FORMAT = "%(asctime)s %(name)s %(levelname)s  %(message)s "  # 配置输出日志格式
    DATE_FORMAT = '%Y-%m-%d  %H:%M:%S %a '  # 配置输出时间的格式，注意月份和天数不要搞乱了
    if (logPath):
        logging.basicConfig(level=level,
                            format=LOG_FORMAT,
                            datefmt=DATE_FORMAT,
                            # filename=r"d:\test\test.log" #有了filename参数就不会直接输出显示到控制台，而是直接写入文件
                            filename=logPath
                            )
    else:
        logging.basicConfig(level=level,
                            format=LOG_FORMAT,
                            datefmt=DATE_FORMAT,
                            )
    return logging
