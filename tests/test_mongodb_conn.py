import os
import unittest

from json import dumps
from app import app, config

from database.models import Group, User
from mongoengine import connect, disconnect, get_connection

class MongoDBTest(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		disconnect()
		connect('groupmanager', host='mongodb://localhost:27017')

	@classmethod
	def tearDownClass(cls):
	   disconnect()
	   
	def test_mongodb_conn(self):
		self.assertIsNotNone(get_connection())

	def test_mongodb_conn_settings(self):
		self.assertEqual(app.config['MONGODB_SETTINGS']['host'], 'mongodb://localhost:27017/groupmanager')