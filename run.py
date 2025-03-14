# 创建应用实例
import sys
from wxcloudrun import app
from wxcloudrun.logging_config import logger

# 启动Flask Web服务
if __name__ == '__main__':
    logger.info('Starting Flask application')
    app.run(host=sys.argv[1], port=sys.argv[2])
