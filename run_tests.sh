#!/bin/bash

# 安装依赖
pip install -r requirements.txt

# 运行测试并生成覆盖率报告
pytest --cov=wxcloudrun tests/

# 生成HTML格式的覆盖率报告
coverage html

# 打开覆盖率报告
open htmlcov/index.html