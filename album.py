#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

from htmlparser import between

class Album:
	def __init__(self, html, account):
		self.title	= between(html, '<div class="igt">', '</div>')
		self.link	= between(html, '<div class="ipl">', '</div>')
		self.created	= between(html, '<div class="id">', '</div>')
		self.modified	= between(html, '<div class="idm">', '</div>')
		self.server	= between(html, '<div class="igs">', '</div>')
		self.preview	= between(html, '<div class="ign">', '</div>')
		self.account	= account

