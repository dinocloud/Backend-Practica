from flask_classy import FlaskView
from flask import Flask, jsonify, request
from models import *
from schemas import *


class TasksView(FlaskView):
    task_schema = TaskSchema()

    def index(self):
        tasks = Task.query.all()
        tasks_data = self.task_schema.dump(tasks, many=True).data
        return jsonify({'task': tasks_data}), 200

    def get(self, id_task):
        task = Task.query.filter_by(id_task=int(id_task)).first()
        task_data = self.task_schema.dump(task).data
        return jsonify({'task': task_data})

    def post(self):
        data = request.json
        task_name = data.get('task_name', None)
        if not task_name:
            return 400
        task_description = data.get('task_description', None)
        tsk = Task(task_name=task_name, task_description=task_description)
        try:
            db.session.add(tsk)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return 409
        task = Task.query.filter_by(task_name=tsk.task_name).first()
        task_data = self.task_schema.dump(task).data
        return jsonify({'task': task_data}), 201


    def put(self, id_task):
        data = request.json
        task = Task.query.filter_by(id_task=int(id_task)).first()
        task.task_name = data.get('task_name', None)
        task.task_description = data.get('task_description', None)
        try:
            db.session.merge(task)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return 409
        task_data = self.task_schema.dump(task).data
        return jsonify({'task': task_data})


    def delete(self, id_task):
        try:
            db.session.delete(Task.query.get(id_task))
            db.session.commit()
        except Exception as e:
            return jsonify({'result': False})
        return jsonify({'result': True})