import os

# 是否开启debug模式
DEBUG = True

# 读取数据库环境变量
username = os.environ.get("MYSQL_USERNAME", 'root')
password = os.environ.get("MYSQL_PASSWORD", 'root')
db_address = os.environ.get("MYSQL_ADDRESS", '127.0.0.1:3306')

APPID = "wxd0b5cbe3cc0b35cf"
APP_SECRET = "0c907756be7219f29d2e49d11a5c570d"
