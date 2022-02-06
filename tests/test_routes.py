import sys
import json
import unittest

from app import app, api
from nose2.tools import such
from database.db import MongoEngine
from database.models import Group, User
from routes.routes import initialize_routes
from mongoengine import connect, disconnect, errors
from tests.test_mongodb_conn import MongoDBTest
from routes.serializers import GroupApiGet, GroupApiPost, GroupApiPut, GroupApiDelete

class TestRoutes(MongoDBTest):
	@classmethod
	def setUp(cls):
		MongoDBTest.setUpClass()
		cls.app = app
		cls.app.config['TESTING'] = True
		cls.client = cls.app.test_client()
		cls.api = api
		try:
			cls.group = Group(group_id=1, group_name="Test Group", group_ban_list=[], group_mute_list=[], member_list=[])
			cls.group.save()
			cls.user = User(user_id=1, is_bot=False, username="test", is_admin=True, is_moderator=True)
			cls.user.save()
		except errors.NotUniqueError as e:
			cls.group = Group.objects(group_id=1).first()
			cls.user = User.objects(user_id=1).first()
		with cls.api.app.app_context():
			initialize_routes(cls.api)
		
		
	@classmethod
	def tearDownClass(cls):
		MongoDBTest.tearDownClass()
		
	def test_group_get(self):
		response = self.client.get('/get_info/1')
		data = response.data.decode('utf-8').replace('\n', '')
		self.assertEqual(response.status_code, 200)
		self.assertEqual(data, json.dumps(self.group.to_json()))
  
	def test_group_get_not_found(self):
		response = self.client.get('/get_info/999999999999')
		self.assertEqual(response.status_code, 400)
	
	def test_group_get_bad_request(self):
		response = self.client.get('/get_info/error')
		self.assertEqual(response.status_code, 404)
  
	''' def test_group_post(self):
		response = self.client.post('/group/1')
		data = response.data.decode('utf-8').replace('\n', '')
		self.assertEqual(response.status_code, 200)
		self.assertEqual(data, {
			"success": True,
			"message": f"group {group.group_id} added successfully to the database."
		}) '''
  
	def test_group_put(self):
		actions = ['member', 'mute', 'ban']
		elserror = {"error": "available actions: ban, mute, member, promote"}
		error = {"success": False, "error": "group not found in db"}
		for action in actions:
			user_id = len(self.group.member_list)
			try:
				response = self.client.put(f'/modify/1/{action}/{user_id}')
				data = response.data.decode('utf-8').replace('\n', '')
			except Exception as e:
				continue
			self.assertEqual(data, 
                json.dumps({
					"success":
						True,
					"message":
						f"Action '{action.capitalize()}' was perfomed succesfully on user {user_id} in group {self.group.group_id}"
				})
			)
			self.assertEqual(self.group.member_list, [i+1 for i in range(user_id)])
   
		response = self.client.put('/modify/3/member/2')
		data = response.data.decode('utf-8').replace('\n', '')
		self.assertEqual(response.status_code, 404)
		self.assertEqual(data, json.dumps(error))
		response = self.client.put('/modify/1/add/22')
		data = response.data.decode('utf-8').replace('\n', '')
		self.assertEqual(response.status_code, 400)
		self.assertEqual(data, json.dumps(elserror))	
			
if __name__ == "__main__":
	import nose2
	nose2.main()