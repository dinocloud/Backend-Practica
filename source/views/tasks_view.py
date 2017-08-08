from flask_classy import FlaskView
from flask import jsonify, request
from schemas import *
from utils import *
from sqlalchemy import or_
from sqlalchemy import and_
from datetime import datetime
from werkzeug.exceptions import Conflict, NotFound, InternalServerError



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
            raise NotFound('Task name is None')
        task_description = data.get('task_description', None)
        due_date = data.get('due_date', None)
        if due_date is not None:
            due_date = datetime.fromtimestamp(int(due_date)).strftime('%Y-%m-%d %H:%M:%S')
        tsk = Task(task_name=task_name, task_description=task_description, due_date=due_date)
        try:
            db.session.add(tsk)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise InternalServerError('Task not added')

        owner = TaskOwner(id_task_owner=int(user.id_user), id_task=int(tsk.id_task),
                         id_user=int(user.id_user))
        try:
            db.session.add(owner)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise InternalServerError('User not added')

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
                    raise InternalServerError('User not added')
        task = Task.query.join(TaskOwner, Task.id_task == TaskOwner.id_task)\
            .filter_by(id_user=user.id_user).order_by(Task.date_created.desc()).first()
        task_data = self.task_schema.dump(task).data
        return jsonify({'task': task_data}), 201

    def put(self, id_task):
        logged_user = authorization(request.headers.get('Authorization', None))
        data = request.json
        task = Task.query.filter_by(id_task=int(id_task)).first()
        task.task_name = data.get('task_name', None)
        task.task_description = data.get('task_description', None)
        task.id_task_status = data.get('id_task_status',1)
        due_date = data.get('due_date', None)
        if due_date is not None:
            due_date = datetime.fromtimestamp(int(due_date)).strftime('%Y-%m-%d %H:%M:%S')
        task.due_date = due_date

        users = set(data.get('users'))
        task_collaborators = TaskOwner.query.filter_by(id_task=id_task).filter(
            TaskOwner.id_task_owner != TaskOwner.id_user).with_entities(TaskOwner.id_user).all()
        collaborators = set([collaborator[0] for collaborator in task_collaborators])
        add_users = users.difference(collaborators)
        delete_collaborators = collaborators.difference(users)

        if add_users is not None:
            for user_to_add in add_users:
                user = TaskOwner(id_task_owner=logged_user.id_user, id_task=id_task, id_user=user_to_add)
                try:
                    db.session.add(user)
                    db.session.commit()
                except Exception as e:
                    db.session.rollback()
                    raise InternalServerError('User not added')

        if delete_collaborators is not None:
            for user_to_delete in delete_collaborators:
                delete_user = TaskOwner.query.filter_by(id_task=id_task, id_user=user_to_delete).first()
                try:
                    db.session.delete(delete_user)
                    db.session.commit()
                except Exception as e:
                    db.session.rollback()
                    raise InternalServerError('User not deleted')
        try:
            db.session.merge(task)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise InternalServerError('Task not added')
        task_data = self.task_schema.dump(task).data
        return jsonify({'task': task_data})


    def delete(self, id_task):
        authorization(request.headers.get('Authorization', None))
        task_collaborators = TaskOwner.query.filter_by(id_task=id_task)
        try:
            for owner in task_collaborators:
                db.session.delete(owner)
            task = Task.query.get(id_task)
            db.session.delete(task)
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

