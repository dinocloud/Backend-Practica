from flask_classy import FlaskView
from flask import Flask, jsonify, request
from models import *


class UsersView(FlaskView):

    def index(self):
        return jsonify({'users': User.query.all()})

    def get(self, id_user):
        return jsonify({'user': User.query.get(id_user)})

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
        return jsonify({'user': usr}), 201


    def put(self, id_user):
        usr = User.query.get(id_user)
        usr.username = request.json.get('username', usr.name)
        usr.password = request.json.get('password', usr.password)
        db.session.commit()
        return jsonify({'user': usr})


    def delete(self, id_user):
        db.session.delete(User.query.get(id_user))
        db.session.commit()
        return jsonify({'result': True})
