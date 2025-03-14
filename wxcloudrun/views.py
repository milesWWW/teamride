from datetime import datetime
from flask import render_template, request
from run import app
from wxcloudrun.dao import delete_counterbyid, query_counterbyid, insert_counter, update_counterbyid
from wxcloudrun.model import Counters
from wxcloudrun.response import make_succ_empty_response, make_succ_response, make_err_response
from wxcloudrun.auth import token_required
from wxcloudrun.logging_config import logger


@app.route('/')
def index():
    """
    :return: 返回index页面
    """
    return render_template('index.html')


@app.route('/api/count', methods=['POST'])
@token_required
def count():
    """
    :return:计数结果/清除结果
    """
    logger.info(f'POST /api/count request: {request.get_json()}')

    # 获取请求体参数
    params = request.get_json()

    # 检查action参数
    if 'action' not in params:
        logger.warning('Missing action parameter')
        return make_err_response('缺少action参数')

    # 按照不同的action的值，进行不同的操作
    action = params['action']

    # 执行自增操作
    if action == 'inc':
        counter = query_counterbyid(1)
        if counter is None:
            counter = Counters()
            counter.id = 1
            counter.count = 1
            counter.created_at = datetime.now()
            counter.updated_at = datetime.now()
            insert_counter(counter)
        else:
            counter.id = 1
            counter.count += 1
            counter.updated_at = datetime.now()
            update_counterbyid(counter)
        logger.info(f'Incremented counter to {counter.count}')
        return make_succ_response(counter.count)

    # 执行清0操作
    elif action == 'clear':
        delete_counterbyid(1)
        logger.info('Counter cleared')
        return make_succ_empty_response()

    # action参数错误
    else:
        logger.warning(f'Invalid action parameter: {action}')
        return make_err_response('action参数错误')


@app.route('/api/count', methods=['GET'])
@token_required
def get_count():
    """
    :return: 计数的值
    """
    logger.info('GET /api/count request')
    counter = Counters.query.filter(Counters.id == 1).first()
    count = 0 if counter is None else counter.count
    logger.info(f'Current count: {count}')
    return make_succ_response(count)
