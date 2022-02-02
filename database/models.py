from .db import db

class User(db.Document):
    user_id = db.LongField(required=True, unique=True)
    is_bot = db.BooleanField(required=True)
    username = db.StringField(required=True)
    is_admin = db.BooleanField(required=True)
    is_moderator = db.BooleanField(required=True)

class Group(db.Document):
    group_id = db.LongField(required=True, unique=True)
    group_name = db.StringField(required=True)
    group_ban_list = db.ListField(db.DictField())
    group_mute_list = db.ListField(db.DictField())
    member_list = db.ListField(db.StringField())