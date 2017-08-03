from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from database import db
import datetime


class Task(db.Model):
    __tablename__ = 'tasks'
    id_task = db.Column(Integer, primary_key=True)
    task_name = db.Column(String(150), nullable=False)
    task_description = db.Column(String(300))
    date_created = db.Column(DateTime, nullable=False)
    id_task_status = db.Column(Integer, ForeignKey('task_statuses.id_task_status'))
    description = db.relationship('TaskStatus', backref=db.backref('task status per task'))

    def __init__(self, task_name=None, task_description=None,
                 id_task_status=1):
        self.task_name = task_name
        self.task_description = task_description
        self.date_created = datetime.datetime.now()
        self.id_task_status = id_task_status


class TaskStatus(db.Model):
    __tablename__ = 'task_statuses'
    id_task_status = db.Column(Integer, primary_key=True)
    description = db.Column(String(70))

    def __init__(self, id_task_status=None, description=None):
        self.id_task_status = id_task_status
        self.description = description


class TaskOwner(db.Model):
    __tablename__ = 'task_owners'
    id_task_owner = db.Column(Integer, ForeignKey('users.id_user'), primary_key=True)
    id_task = db.Column(Integer, ForeignKey('tasks.id_task'), primary_key=True)
    id_user = db.Column(Integer, ForeignKey('users.id_user'), primary_key=True)
    owner = db.relationship('User', foreign_keys=[id_task_owner], backref=db.backref('tasks_owner_per_task'))
    task = db.relationship('Task', foreign_keys=[id_task], backref=db.backref('tasks_that_belong_to_the_owner'))

    def __init__(self, id_task_owner=None, id_task=None, id_user=None):
        self.id_task_owner = id_task_owner
        self.id_task = id_task
        self.id_user = id_user
