import logging

from sqlalchemy.exc import OperationalError
from wxcloudrun import db

# 初始化日志
logger = logging.getLogger('log')

class DAO:
    def __init__(self, db):
        self.db = db

    def get_team_by_id(self, team_id):
        team = Team.query.filter_by(id=team_id).first()
        return team

    def add_team(self, user_id, team_info):
        team = Team(
            user_id=user_id,
            distance=team_info['distance'],
            limit=team_info['limit'],
            location=team_info['location'],
            max_speed=team_info['max_speed'],
            min_speed=team_info['min_speed'],
            note=team_info['note'],
            num_people=team_info['num_people'],
            route=team_info['route'],
            start_date=team_info['start_date'],
            time=team_info['time'],
            title=team_info['title'],
        )
        self.db.session.add(team)
        self.db.session.commit()
        return team.id

    def delete_team(self, team_id):
        team = self.get_team_by_id(team_id)
        if not team:
            return False
        self.db.session.delete(team)
        self.db.session.commit()
        return True

    def update_team(self, team_id, team_info):
        team = self.get_team_by_id(team_id)
        if not team:
            return False
        team.distance = team_info.get('distance', team.distance)
        team.limit = team_info.get('limit', team.limit)
        team.location = team_info.get('location', team.location)
        team.max_speed = team_info.get('max_speed', team.max_speed)
        team.min_speed = team_info.get('min_speed', team.min_speed)
        team.note = team_info.get('note', team.note)
        team.num_people = team_info.get('num_people', team.num_people)
        team.route = team_info.get('route', team.route)
        team.start_date = team_info.get('start_date', team.start_date)
        team.time = team_info.get('time', team.time)
        team.title = team_info.get('title', team.title)
        self.db.session.commit()
        return True

    def get_participants_by_team_id(self, team_id):
        participants = TeamParticipant.query.filter_by(team_id=team_id).all()
        return participants

    def add_participant(self, team_id, user_id):
        participant = TeamParticipant(
            team_id=team_id,
            user_id=user_id,
        )
        self.db.session.add(participant)
        self.db.session.commit()
        return participant.id

    def delete_participant(self, participant_id):
        participant = TeamParticipant.query.filter_by(id=participant_id).first()
        if not participant:
            return False
        self.db.session.delete(participant)
        self.db.session.commit()
        return True

    def get_user_by_id(self, user_id):
        user = User.query.filter_by(id=user_id).first()
        return user

    def add_user(self, user_id):
        user = User(
            id=user_id,
        )
        self.db.session.add(user)
        self.db.session.commit()
        return user.id

    def delete_user(self, user_id):
        user = self.get_user_by_id(user_id)
        if not user:
            return False
        self.db.session.delete(user)
        self.db.session.commit()
        return True
