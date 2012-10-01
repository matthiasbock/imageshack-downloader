#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

def loadconfig():
	from ConfigParser import RawConfigParser

	parser = RawConfigParser()
	parser.read('imageshack.conf')
	username = parser.get('Login', 'Username')
	password = parser.get('Login', 'Password')
	del parser

	return username, password

