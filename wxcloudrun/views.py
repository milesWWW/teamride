from datetime import datetime
from flask import render_template, request
from run import app
import requests
from wxcloudrun.response import make_succ_empty_response, make_succ_response, make_err_response
from flask import Blueprint, jsonify, request
from .model import Team, TeamParticipant, User
from .dao import DAO
from wxcloudrun import db
import config
from .api import api_bp

dao = DAO(db)

USER_ID = "openid"

@app.before_first_request
def create_tables():
    db.create_all()

@app.before_request
def log_request_info():
    app.logger.debug('Headers: %s', request.headers)
    app.logger.debug('Body: %s', request.get_data())
    app.logger.debug('Endpoint: %s', request.endpoint)
    app.logger.debug('Method: %s', request.method)
    app.logger.debug('URL: %s', request.url)
    app.logger.debug('Matching URL Rule: %s', request.url_rule)

@api_bp.route('/get_openid', methods=['POST'])
def get_openid():
    code = request.json.get('code')

    if not code:
        return jsonify({'message': 'code not found'}), 400

    # 调用微信接口，获取用户openid和session_key
    appid = config.APPID
    secret = config.APP_SECRET
    url = 'https://api.weixin.qq.com/sns/jscode2session?appid={}&secret={}&js_code={}&grant_type=authorization_code'.format(appid, secret, code)
    res = requests.get(url)
    openid = res.json().get('openid')
    session_key = res.json().get('session_key')

    # 将openid和session_key存入数据库或其他存储方式
    # ...

    return jsonify({'openid': openid}), 200

# 获取队伍列表
@api_bp.route('/teams', methods=['GET'])
def get_teams():
    teams = dao.get_all_teaminfo()
    team_list = []
    for team_dict in teams:
        team_dict.pop('_sa_instance_state', None)
        team_list.append(team_dict)
    return jsonify(team_list)

# 获取队伍详情
@api_bp.route('/teams/<int:team_id>', methods=['GET'])
def get_team_detail(team_id):
    team_dict = dao.get_teaminfo_by_id(team_id)
    if not team_dict:
        return jsonify({'message': 'Team not found'}), 404
    team_dict.pop('_sa_instance_state', None)
    participants = dao.get_participants_by_team_id(team_id)
    participant_list = []
    for participant in participants:
        user = dao.get_user_by_id(participant.user_id)
        if user:
            participant_dict = participant.__dict__
            participant_dict.pop('_sa_instance_state', None)
            participant_dict['user'] = user.__dict__
            participant_list.append(participant_dict)
    team_dict['participants'] = participant_list
    return jsonify(team_dict)

# 创建队伍
@api_bp.route('/teams', methods=['POST'])
def create_team():
    # user_id = request.json.get(USER_ID)
    team_info = request.json.get('team_info', {})
    # if not user_id:
    #     return jsonify({'message': 'User ID not found'}), 400
    team_id = dao.add_team(team_info)
    return jsonify({'id': team_id})

# 更新队伍
@api_bp.route('/teams/<int:team_id>', methods=['PUT'])
def update_team(team_id):
    team_info = request.json.get('team_info', {})
    result = dao.update_team(team_id, team_info)
    if not result:
        return jsonify({'message': 'Team not found'}), 404
    return jsonify({'message': 'Team updated successfully'})

# 删除队伍
@api_bp.route('/teams/<int:team_id>', methods=['DELETE'])
def delete_team(team_id):
    result = dao.delete_team(team_id)
    if not result:
        return jsonify({'message': 'Team not found'}), 404
    return jsonify({'message': 'Team deleted successfully'})

# 获取我创建的队伍
@api_bp.route('/users/my_team', methods=['GET'])
def get_teams_by_me():
    user_id = request.json.get(USER_ID)
    teams = dao.get_team_by_user_id_create(user_id)
    team_list = []
    for team_dict in teams:
        team_dict.pop('_sa_instance_state', None)
        team_list.append(team_dict)
    return jsonify(team_list)

# 获取我参与的队伍
@api_bp.route('/users/teams', methods=['GET'])
def get_teams_by_user_id():
    user_id = request.json.get(USER_ID)
    teams = dao.get_teams_by_user_id(user_id)
    team_list = [dao._convert_team_to_teaminfo(team) for team in teams]
    return jsonify(team_list)

# 添加参与者
@api_bp.route('/teams/<int:team_id>/participants', methods=['POST'])
def add_participant(team_id):
    user_id = request.json.get(USER_ID)
    if not user_id:
        return jsonify({'message': 'User ID not found'}), 400
    participants = dao.get_participants_by_team_id(team_id)
    for participant in participants:
        if user_id == participant.user_id:
            return jsonify({'message': 'User already joined the team'}), 404
    result = dao.add_participant(team_id, user_id)
    return jsonify({'id': result})

# 删除参与者
@api_bp.route('/teams/participants/<int:team_id>', methods=['DELETE'])
def delete_participant(team_id):
    user_id = request.json.get(USER_ID)
    result = dao.delete_participant(team_id=team_id, user_id=user_id)
    if not result:
        return jsonify({'message': 'Participant not found'}), 404
    return jsonify({'message': 'Participant deleted successfully'})

# 创建用户
@api_bp.route('/users', methods=['POST'])
def create_user():
    user_id = request.json.get(USER_ID)
    if not user_id:
        return jsonify({'message': 'User ID not found'}), 400
    new_user_id = dao.add_user(user_id)
    return jsonify({'id': new_user_id})
