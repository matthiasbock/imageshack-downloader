#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

from htmlparser import between

class Tag:
	def __init__(self, html, account):
		self.tag	= html
		self.account	= account

