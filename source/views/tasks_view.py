from flask_classy import FlaskView
from flask import Flask, jsonify, request
from models import *
from schemas import *
from utils import *
from sqlalchemy import or_
from sqlalchemy import and_



class TasksView(FlaskView):
    task_schema = TaskSchema()
    user_schema = UserSchema()
    task_owner_schema = TaskOwnerSchema()
    status_schema = TaskStatusSchema()

    class TasksPaginationSchema(PaginationSchema):
        items = fields.List(fields.Nested(TaskSchema))

    pagination_schema = TasksPaginationSchema()

    def index(self):
        authorization(request.headers.get('Authorization', None))
        page = request.args.get('page', None)
        per_page = request.args.get('per_page', None)
        tasks = Task.query.paginate(page, per_page, error_out=False)
        tasks_data = self.pagination_schema.dump(tasks).data
        return jsonify(tasks_data), 200

    def get(self, id_task):
        authorization(request.headers.get('Authorization', None))
        task = Task.query.filter_by(id_task=int(id_task)).first()
        task_data = self.task_schema.dump(task).data
        return jsonify({'task': task_data})

    def post(self):
        user = authorization(request.headers.get('Authorization', None))
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

        owner = TaskOwner(id_task_owner=int(user.id_user), id_task=int(tsk.id_task),
                         id_user=int(user.id_user))
        try:
            db.session.add(owner)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return 409

        for task_user_id in data.get('users'):
            user_repeated = TaskOwner.query.filter_by(id_task_owner=owner.id_task_owner,
                                              id_task=tsk.id_task, id_user=task_user_id).first()
            task_user = TaskOwner(id_task_owner=user.id_user,
                             id_task=tsk.id_task, id_user=task_user_id)

            if user_repeated is None:
                try:
                    db.session.add(task_user)
                    db.session.commit()
                except Exception as e:
                    db. session.rollback()
                    return 409

        task = Task.query.filter_by(task_name=tsk.task_name).first()
        task_data = self.task_schema.dump(task).data
        return jsonify({'task': task_data}), 201

    def put(self, id_task):
        authorization(request.headers.get('Authorization', None))
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
        authorization(request.headers.get('Authorization', None))
        try:
            db.session.delete(Task.query.get(id_task))
            db.session.commit()
        except Exception as e:
            return jsonify({'result': False})
        return jsonify({'result': True})

    def get_task_per_user(self):
        user = authorization(request.headers.get('Authorization', None))
        all_tasks = TaskOwner.query.filter(or_(and_(TaskOwner.id_task_owner==user.id_user, TaskOwner.id_user==user.id_user), TaskOwner.id_user==user.id_user)).all()
        all_tasks_data = self.task_owner_schema.dump(all_tasks, many=True).data

        for index, task in enumerate(all_tasks_data):
            task_obj = task.get('task')
            colls = TaskOwner.query.filter_by(id_task=task_obj.get('id_task')).filter(TaskOwner.id_task_owner != TaskOwner.id_user).all()
            colls_list = list()
            for coll in colls:
                coll_object = User.query.get(coll.id_user)
                colls_list.append(coll_object)
            colls_data = self.user_schema.dump(colls_list, many=True).data
            task['users'] = colls_data
            all_tasks_data[index] = task
        return jsonify({'all_tasks':all_tasks_data})


    def get_statuses(self):
        statuses = TaskStatus.query.all()
        statuses_data = self.status_schema.dump(statuses, many=True).data
        return jsonify({'statuses':statuses_data})

