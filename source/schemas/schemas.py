from marshmallow import Schema, fields


class UserSchema(Schema):
    id_user = fields.Integer()
    username = fields.String()


class TaskStatusSchema(Schema):
    id_task_status = fields.Integer()
    description = fields.String()


class TaskSchema(Schema):
    id_task = fields.Integer()
    task_name = fields.String()
    task_description = fields.String()
    date_created = fields.DateTime()
    id_task_status = fields.Integer()
    task_status = fields.Nested(TaskStatusSchema())


class PaginationSchema(Schema):
    pages = fields.Integer()
    prev_num = fields.Integer()
    has_prev = fields.Boolean()
    has_next = fields.Boolean()
    next_num = fields.Integer()


class TaskOwnerSchema(Schema):
    owner = fields.Nested(UserSchema())
    task = fields.Nested(TaskSchema())
