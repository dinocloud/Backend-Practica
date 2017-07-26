from marshmallow import Schema, fields


class UserSchema(Schema):
    id_user = fields.Integer()
    username = fields.String()


class TaskSchema(Schema):
    id_task = fields.Integer()
    task_name = fields.String()
    task_description = fields.String()
    date_created = fields.DateTime()
    id_task_status = fields.Integer()
