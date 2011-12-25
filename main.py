#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

from ConfigParser import RawConfigParser

parser = RawConfigParser()
parser.read('imageshack.conf')

username = parser.get('Login', 'Username')
password = parser.get('Login', 'Password')

del parser


from robot import Robot

r = Robot(debug=True)

r.GET('imageshack.us')
r.Page.save('index.html')

#	l_login
#	l_password

del r
