from datetime import datetime
from flask import render_template, request
from run import app
from wxcloudrun.response import make_succ_empty_response, make_succ_response, make_err_response
from flask import Blueprint, jsonify, request
from .model import Team, TeamParticipant, User
from .dao import DAO
from wxcloudrun import db

api_bp = Blueprint('api', __name__)
app.register_blueprint(api_bp, url_prefix='/api')

dao = DAO(db)

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

# 获取队伍列表
@api_bp.route('/teams', methods=['GET'])
def get_teams():
    teams = Team.query.all()
    team_list = []
    for team in teams:
        team_dict = team.__dict__
        team_dict.pop('_sa_instance_state', None)
        team_list.append(team_dict)
    return jsonify(team_list)

# 获取队伍详情
@api_bp.route('/teams/<int:team_id>', methods=['GET'])
def get_team_detail(team_id):
    team = dao.get_team_by_id(team_id)
    if not team:
        return jsonify({'message': 'Team not found'}), 404
    team_dict = team.__dict__
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
    user_id = request.json.get('user_id')
    team_info = request.json.get('team_info', {})
    if not user_id:
        return jsonify({'message': 'User ID not found'}), 400
    team_id = dao.add_team(user_id, team_info)
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

# 添加参与者
@api_bp.route('/teams/<int:team_id>/participants', methods=['POST'])
def add_participant(team_id):
    user_id = request.json.get('user_id')
    if not user_id:
        return jsonify({'message': 'User ID not found'}), 400
    result = dao.add_participant(team_id, user_id)
    return jsonify({'id': result})

# 删除参与者
@api_bp.route('/teams/participants/<int:participant_id>', methods=['DELETE'])
def delete_participant(participant_id):
    result = dao.delete_participant(participant_id)
    if not result:
        return jsonify({'message': 'Participant not found'}), 404
    return jsonify({'message': 'Participant deleted successfully'})

# 创建用户
@api_bp.route('/users', methods=['POST'])
def create_user():
    user_id = request.json.get('user_id')
    if not user_id:
        return jsonify({'message': 'User ID not found'}), 400
    new_user_id = dao.add_user(user_id)
    return jsonify({'id': new_user_id})
