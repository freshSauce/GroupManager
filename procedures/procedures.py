from __future__ import absolute_import

import requests as r

from time import time as now
from json import dumps

API_URL = "https://api.telegram.org/bot{}".format(config["CONFIG"]["BOT_TOKEN"])


def ban_user(user_id, group_id, time):
    time = int(now) + time
    result = r.post(
        API_URL + "/banChatMember",
        data={
            "chat_id": group_id,
            "user_id": user_id,
            "until_date": time
        }
    )
    if result.status_code == 200:
        return True
    else:
        return False


def unban_user(user_id, group_id):
    result = r.post(
        API_URL + "/unbanChatMember",
        data={
            "chat_id": group_id,
            "user_id": user_id,
            "only_if_banned": True
        }
    )
    if result.status_code == 200:
        return True
    else:
        return False


def kick_user(user_id, group_id):
    result = r.post(
        API_URL + "/unbanChatMember",
        data={
            "chat_id": group_id,
            "user_id": user_id
        }
    )
    if result.status_code == 200:
        return True
    else:
        return False


def mute_user(user_id, group_id, time):
    time = int(now) + time
    result = r.post(
        API_URL + "/restrictChatMember",
        data={
            "chat_id": group_id,
            "user_id": user_id,
            "permissions": dumps({"can_send_messages": False}),
            "until_date": time
        }
    )
    if result.status_code == 200:
        return True
    else:
        return False


def promote_to_moderator(user_id, group_id):
    result = r.post(
        API_URL + "/promoteChatMember",
        data={
            "chat_id": group_id,
            "user_id": user_id,
            "can_delete_messages": True,
            "can_invite_users": True,
            "can_restrict_members": True,
            "can_pin_messages": True,
        }
    )
    if result.status_code == 200:
        result = r.post(
            API_URL + "/setChatAdministratorCustomTitle",
            data={
                "chat_id": group_id,
                "user_id": user_id,
                "custom_title": "Moderator"
            }
        )
        if result.status_code == 200:
            return True
        else:
            return False
    else:
        return False
