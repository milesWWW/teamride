from datetime import datetime
from wxcloudrun import db


# 计数表
class Team(db.Model):
    __tablename__ = 'teams'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(32), default='default')
    distance = db.Column(db.Float, default=0.0)
    limit = db.Column(db.Integer, default=0)
    location = db.Column(db.String(255))
    max_speed = db.Column(db.Float, default=0.0)
    min_speed = db.Column(db.Float, default=0.0)
    note = db.Column(db.String(255))
    num_people = db.Column(db.Integer, default=0)
    route = db.Column(db.String(255))
    start_date = db.Column(db.String(16))
    time = db.Column(db.String(16))
    title = db.Column(db.String(255))
    # activity_id = db.Column(db.Integer, db.ForeignKey('team_participants.id'))
    
class TeamParticipant(db.Model):
    __tablename__ = 'team_participants'

    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'))
    user_id = db.Column(db.String(32), db.ForeignKey('users.id'))

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.String(32), primary_key=True)
