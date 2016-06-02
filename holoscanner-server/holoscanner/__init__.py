import logging
from holoscanner import config


console = logging.StreamHandler()
formatter = logging.Formatter(config.LOG_FORMAT)
console.setFormatter(formatter)

logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger().addHandler(console)

base_logger = logging.getLogger(__name__)
# base_logger.addHandler(console)
base_logger.setLevel(config.LOG_LEVEL)
