# 创建应用实例
import sys
from wxcloudrun import app
from wxcloudrun.api import api_bp

app.register_blueprint(api_bp, url_prefix='/api')

# 启动Flask Web服务
if __name__ == '__main__':
    app.run(host=sys.argv[1], port=sys.argv[2])
    
