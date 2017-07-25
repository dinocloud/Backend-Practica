from flask_classy import FlaskView
from flask import Flask, jsonify, request
from models import *


class TasksView(FlaskView):

    def index(self):
        return jsonify({'tasks': Task.query.all()})

    def get(self, id_task):
        return jsonify({'task': Task.query.get(id_task)})

    def post(self):
        if not request.json or not 'task_name' in request.json:
            return 400
        tsk = Task(request.json.task_name, request.json.get('task_description', ''),
                   request.json.get('date_created', ''))
        db.session.add(tsk)
        db.session.commit()
        return jsonify({'user': tsk}), 201


    def put(self, id_task):
        tsk = User.query.get(id_task)
        tsk.task_name = request.json.get('task_name', tsk.name)
        tsk.task_description = request.json.get('task_description', tsk.task_description)
        tsk.date_created = request.json.get('date_created', tsk.date_created)
        db.session.commit()
        return jsonify({'task': tsk})


    def delete(self, id_task):
        db.session.delete(User.query.get(id_task))
        db.session.commit()
        return jsonify({'result': True})
