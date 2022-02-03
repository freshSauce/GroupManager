from flask import Response, request
from database.models import User, Group
from flask_restx import Resource
#from procedures.procedures import *

class GroupApiGet(Resource):
	def get(self, group_id):
		try:
			group = Group.objects(group_id=group_id).first()
			if group == None:
				return {"success": False, "error": "group not found in db"}, 404
			return group.to_json()
		except ValueError:
			return {"success": False, "error": "group_id must be an integer"}, 400
		except Exception as e:
			return {"success": False, "error": str(e)}, 500


class GroupApiPost(Resource):
	def post(self, group_id):
		group = Group.objects(group_id=group_id).first()
		if group == None:
			group = Group(group_id=group_id)
		group.group_name = request.json['group_name']
		group.save()

		return {
			"success": True,
			"message": f"group {group_id} added successfully to the database."
		}, 200


class GroupApiPut(Resource):
	def put(self, group_id, action, user_id):
		group = Group.objects(group_id=group_id).first()
		if group == None:
    			return {"success": False, "error": "group not found in db"}, 404
   
		if action == 'ban':
			if user_id in group.group_ban_list:
				return {"success": False, "error": "user already banned"}, 400
			if user_id in group.group_mute_list:
				group.group_mute_list.remove(user_id)
				group.save()
		elif action == 'mute':
			if user_id in group.group_mute_list:
				return {"success": False, "error": "user already muted"}, 400
			if user_id in group.group_ban_list:
				group.group_ban_list.remove(user_id)
				group.save()
		elif action == 'member':
			if user_id in group.member_list:
				return {"success": False, "error": "user already member"}, 400
			if user_id in group.group_ban_list:
				group.group_ban_list.remove(user_id)
				group.save()
			if user_id in group.group_mute_list:
				group.group_mute_list.remove(user_id)
				group.save()
		else:
			return {"error": "available actions: ban, mute, member"}, 400
		group.save()
		return {
			"success":
				True,
			"message":
				f"Action '{action.capitalize()}' was perfomed succesfully on user {user_id} in group {group_id}"
		}, 200


class GroupApiDelete(Resource):
	def delete(self, group_id, action, user_id):
		group = Group.objects(group_id=group_id).first()
		if group == None:
			return {"success": False, "error": "group not found in db"}, 404
		if action == 'ban':
			group.group_ban_list.remove({'user_id': user_id})
		elif action == 'mute':
			group.group_mute_list.remove({'user_id': user_id})
		elif action == 'member':
			group.member_list.remove(user_id)
		else:
			return {"error": "available actions: ban, mute, member."}, 400
		group.save()
		return {
			"success":
				True,
			"message":
				f"Action '{action.capitalize()}' was perfomed succesfully on user {user_id} in group {group_id}"
		}, 200
