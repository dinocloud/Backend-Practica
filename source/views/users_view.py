from flask_classy import FlaskView
from flask import Flask, jsonify, request
from models import *
from schemas import *


class UsersView(FlaskView):
    user_schema = UserSchema()

    def index(self):
        users = User.query.all()
        users_data = self.user_schema.dump(users, many=True).data
        return jsonify({'user': users_data}), 200


    def get(self, id_user):
        user = User.query.filter_by(id_user=int(id_user)).first()
        user_data = self.user_schema.dump(user).data
        return jsonify({'user': user_data})

    def post(self):
        data = request.json
        username = data.get('username', None)
        if not username:
            return 400
        password = data.get('password', None)
        usr = User(username, password)
        try:
            db.session.add(usr)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return 409
        user = User.query.filter_by(username=usr.username).first()
        user_data = self.user_schema.dump(user).data
        return jsonify({'user': user_data}), 201


    def put(self, id_user):
        data = request.json
        user = User.query.filter_by(id_user=int(id_user)).first()
        user.password = data.get('password', None)
        try:
            db.session.merge(user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return 409
        user_data = self.user_schema.dump(user).data
        return jsonify({'user': user_data})


    def delete(self, id_user):
        db.session.delete(User.query.get(id_user))
        db.session.commit()
        return jsonify({'result': True})
