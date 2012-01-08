#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

from robot import Robot

class ImageShack:
	def __init__(self, username=None, password=None):
		self.username = username
		self.password = password
		self.r = Robot(debug=True)

	def login(self, username=None, password=None):
		if username is None or password is None:
			username = self.username
			password = self.password
		if username is None or password is None:
			return False

		self.r.GET('imageshack.us')
		self.r.POST('/auth.php', {'stay_logged_in':'true', 'format':'json', 'username':username, 'password':password})
		print str(self.r.Page)

