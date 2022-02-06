from flask import request
from database.models import User, Group
from flask_restx import Resource
from procedures.procedures import *


class GroupApiGet(Resource):

	def get(self, group_id):
		try:
			group = Group.objects(group_id=group_id).first()
			if group == None:
				return {"success": False, "error": "group not found in db"}, 400
			return group.to_json()
		except ValueError:
			return {"success": False, "error": "group_id must be an integer"}, 400
		except Exception as e:
			return {"success": False, "error": str(e)}, 500


class GroupApiPost(Resource):
	def post(self, group_id):
		try:
			group = Group.objects(group_id=group_id).first()
			if group == None:
				group = Group(group_id=group_id)
			group.group_name = request.json['group_name']
			group.save()

			return {
				"success": True,
				"message": f"group {group_id} added successfully to the database."
			}, 200
		except KeyError:
			return {"success": False, "error": "argument group_name is required"}, 400
		except ValueError:
			return {"success": False, "error": "group_id must be an integer"}, 400
		except Exception as e:
			return {"success": False, "error": str(e)}, 500

class GroupApiPut(Resource):
	def put(self, group_id, action, user_id):
		group = Group.objects(group_id=group_id).first()
		if group == None:
				return {"success": False, "error": "group not found in db"}, 404

		if action == 'ban':
			if user_id in group.group_ban_list:
				return {"success": False, "error": "user already banned"}, 400
			ban_status, ban_json = ban_user(user_id, group_id, request.json['time'])
			if ban_status:
				group.member_list.remove(user_id)
				group.group_ban_list.append(user_id)
			else:
				return {"success": False, "error": ban_json}, 400
		elif action == 'mute':
			if user_id in group.group_mute_list:
				return {"success": False, "error": "user already muted"}, 400
			mute_status, mute_json = mute_user(user_id, group_id, request.json['time'])
			if mute_status:
				group.group_mute_list.append(user_id)
			else:
				return {"success": False, "error": mute_json}, 400
		elif action == 'member':
			if user_id in group.member_list or user_id in group.group_mute_list:
				return {"success": False, "error": "user already member"}, 400
			if user_id in group.group_ban_list:
				return {"success": False, "error": "user banned"}, 400
		elif action == 'promote':
			if user_id in group.group_ban_list or user_id in group.group_mute_list:
				return {"success": False, "error": "user not elegible for promotion"}, 400
			promote_status, promote_json = promote_user(user_id, group_id)
			if promote_status:
				pass
			else:
				return {"success": False, "error": promote_json}, 400
		else:
			return {"error": "available actions: ban, mute, member, promote"}, 400
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
			if user_id not in group.group_ban_list:
				return {"success": False, "error": "user not banned"}, 400
			unban_status, unban_json = unban_user(user_id, group_id)
			if unban_status:
				group.group_ban_list.remove({'user_id': user_id})
				group.member_list.append(user_id)
			else:
				return {"success": False, "error": unban_json}, 400
			
		elif action == 'mute':
			if user_id not in group.group_mute_list:
				return {"success": False, "error": "user not muted"}, 400
			unmute_status, unmute_json = unmute_user(user_id, group_id)
			if unmute_status:
				group.group_mute_list.remove({'user_id': user_id})
			else:
				return {"success": False, "error": unmute_json}, 400
		elif action == 'member':
			group.member_list.remove(user_id)
		elif action == 'promote':
			if user_id not in group.member_list:
				return {"success": False, "error": "user not member"}, 400
			demote_status, demote_json = demote_user(user_id, group_id)
			if demote_status:
				pass
			else:
				return {"success": False, "error": demote_json}, 400

		else:
			return {"error": "available actions: ban, mute, member."}, 400
		group.save()
		return {
			"success":
				True,
			"message":
				f"Action '{action.capitalize()}' was perfomed succesfully on user {user_id} in group {group_id}"
		}, 200

class UserApiGet(Resource):
	def get(self, user_id):
		try:
			user = User.objects(user_id=user_id).first()
			if user == None:
				return {"success": False, "error": "user not found in db"}, 404
			return user.to_json()
		except ValueError:
			return {"success": False, "error": "user_id must be an integer"}, 400
		except Exception as e:
			return {"success": False, "error": str(e)}, 500
	

class UserApiPost(Resource):
	def post(self, user_id):
		try:
			user = User.objects(user_id=user_id).first()
			if user == None:
				user = User(user_id=user_id)
			user.username = request.json['username']
			user.is_admin = request.json['is_admin']
			user.is_moderator = request.json['is_moderator']
			user.is_bot = request.json['is_bot']
			user.save()

			return {
				"success": True,
				"message": f"user {user_id} added successfully to the database."
			}, 200
		except KeyError as error:
			return {"success": False, "error": f"argument {error.args[0]} is required"}, 400
		except ValueError:
			return {"success": False, "error": "user_id must be an integer"}, 400
		except Exception as e:
			return {"success": False, "error": str(e)}, 500


class UserApiPut(Resource):
	def put(self, user_id):
		user = User.objects(user_id=user_id).first()
		if user == None:
				return {"success": False, "error": "user not found in db"}, 404

		user.username = request.json.get('username') or user.username
		user.is_admin = request.json.get('is_admin') or user.is_admin
		user.is_moderator = request.json.get('is_moderator') or user.is_moderator
		user.is_bot = request.json.get('is_bot') or user.is_bot
		user.save()

		return {
			"success":
				True,
			"message":
				f"user {user_id} updated successfully in the database."
		}, 200

