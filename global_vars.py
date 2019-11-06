import logging, config
from utils.logger import logger

log_level = eval("logging."+config.log_level.upper())
log_path = None
log = logger(log_level, log_path)



