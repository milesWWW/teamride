import logging
import os
from logging.handlers import RotatingFileHandler

LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_LEVEL = logging.INFO
LOG_DIR = 'logs'
LOG_FILE = 'app.log'

# 创建日志目录
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# 配置日志
logging.basicConfig(
    level=LOG_LEVEL,
    format=LOG_FORMAT,
    handlers=[
        RotatingFileHandler(
            os.path.join(LOG_DIR, LOG_FILE),
            maxBytes=1024*1024,
            backupCount=5
        ),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)