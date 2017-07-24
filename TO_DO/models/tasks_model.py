from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from database import db


class Task(db.Models):
    __tablename__ = 'tasks'
    id_task = db.Column(Integer, primary_key=True)
    task_name = db.Column(String(50), nullable=False)
    task_description = db.Column(String(200))
    date_created = db.Column(DateTime, nullable=False)
    id_task_status = db.Column(ForeignKey(Integer, 'task_statuses.id_task_status'))

    def __init__(self, id_task=None, task_name=None, task_description=None, date_created=None,
                 id_task_status=None):
        self.id_task = id_task
        self.task_name = task_name
        self.task_description = task_description
        self.date_created = date_created
        self.id_task_status = id_task_status


class TaskStatus(db.Models):
    __tablename__ = 'task_statuses'
    id_task_status = db.Column(Integer, primary_key=True)
    description = db.Column(String(70))

    def __init__(self, id_task_status=None, description=None):
        self.id_task_status = id_task_status
        self.description = description


class TaskOwner(db.Models):
    __tablename__ = 'task_owners'
    id_task_owner = db.Column(Integer, primary_key=True)
    id_task = db.Column(ForeignKey(Integer, 'tasks.id_task'))
    id_user = db.Column(ForeignKey(Integer, 'users.id_user'))

    def __init__(self, id_task_owner=None, id_task=None, id_user=None):
        self.id_task_owner = id_task_owner
        self.id_task = id_task
        self.id_user = id_user
