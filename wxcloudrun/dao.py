import logging
from datetime import datetime, timedelta
from sqlalchemy.exc import OperationalError
from wxcloudrun import db
from wxcloudrun.model import Team, User, TeamParticipant
from sqlalchemy import asc

# 初始化日志
logger = logging.getLogger('log')

class DAO:
    def __init__(self, db):
        self.db = db

    def _convert_teaminfo_to_team(self, team_info):
        if not team_info:
            return None

        return Team(**{
            self.camel_to_snake(key): value for key, value in team_info.items()
        })        

    def _convert_team_to_teaminfo(self, team):
        if not team:
            return None

        return {
            self.snake_to_camel(key): value for key, value in team.__dict__.items()
            if not key.startswith('_sa_instance_state')
        }        

    def get_all_teaminfo(self):
        teams = Team.query.order_by(desc(Team.datetime)).all()
        return [self._convert_team_to_teaminfo(team) for team in teams]

    def get_team_by_id(self, team_id):
        team = Team.query.filter_by(id=team_id).first()
        return team

    def get_team_by_user_id_create(self, user_id):
        teams = Team.query.filter_by(user_id=user_id).order_by(asc(Team.datetime)).all()
        return [self._convert_team_to_teaminfo(team) for team in teams]


    def get_teaminfo_by_id(self, team_id):
        return self._convert_team_to_teaminfo(self.get_team_by_id(team_id))
        

    def add_team(self, team_info):
        team = self._convert_teaminfo_to_team(team_info)
        self.db.session.add(team)
        self.db.session.commit()
        return team.id

    def delete_team(self, team_id):
        team = self.get_team_by_id(team_id)
        if not team:
            return False
        participants = self.get_participants_by_team_id(team_id)
        for participant in participants:
            self.db.session.delete(participant)    
        self.db.session.delete(team)
        self.db.session.commit()
        return True

    def update_team(self, team_id, team_info):
        team = self.get_team_by_id(team_id)
        if not team:
            return False

        team_info_snake_case = {self.camel_to_snake(key): value for key, value in team_info.items()}

        for key, value in team_info_snake_case.items():
            if not key.startswith('_sa_instance_state'):
                setattr(team, key, value)

        self.db.session.commit()
        return True
    
    def add_number(self, team_id, num=1):
        team = self.get_team_by_id(team_id)
        if not team:
            return False
        if team.num_people>=0:
            team.num_people = team.num_people+num
        self.db.session.commit()
        return True

    def get_participants_by_team_id(self, team_id):
        participants = TeamParticipant.query.filter_by(team_id=team_id).all()
        return participants

    def get_teams_by_user_id(self, user_id):
        team_participants = TeamParticipant.query.filter_by(user_id=user_id).all()
        team_ids = [participant.team_id for participant in team_participants]
        teams=[]
        for team_id in team_ids:
            team = self.get_team_by_id(team_id)
            if team:
                teams.append(team)
        # teams = [self.get_team_by_id(team_id) for team_id in team_ids]
        return teams

    def add_participant(self, team_id, user_id):
        participant = TeamParticipant(
            team_id=team_id,
            user_id=user_id,
        )
        
        self.add_number(team_id)
        self.db.session.add(participant)
        self.db.session.commit()
        return participant.id

    def delete_participant(self, team_id, user_id):
        participant = TeamParticipant.query.filter_by(user_id=user_id, team_id=team_id).first()
        if not participant:
            return False
        self.add_number(team_id, num=-1)       
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

    def camel_to_snake(self, s):
        return ''.join(['_' + i.lower() if i.isupper() else i for i in s]).lstrip('_')

    def snake_to_camel(self, s):
        components = s.split('_')
        return components[0] + ''.join(i.capitalize() for i in components[1:])

    def cleanup_expired_teams(self):
        current_time = datetime.now()
        expiration_period = timedelta(days=1)
        expiration_threshold = current_time - expiration_period
        expired_teams = Team.query.filter(Team.datetime <= expiration_threshold).all()
        for team in expired_teams:
            self.delete_team(team.id)

