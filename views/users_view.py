from flask_classy import FlaskView
from flask import Flask, jsonify, request
from models import *


class UsersView(FlaskView):

    def index(self):
        return jsonify({'users': User.query.all()})

    def get(self, id_user):
        return jsonify({'user': User.query.get(id_user)})

    def post(self):
        if not request.json or not 'username' in request.json:
            return 400
        usr = User(request.json.username, request.json.get('password', ''))
        db.session.add(usr)
        db.session.commit()
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
