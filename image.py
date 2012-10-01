#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

from htmlparser import between

class Image:
	def __init__(self, html, account):
		self.id		= between(html, '<div class="ii">', '</div>')
		self.server	= between(html, '<div class="is">', '</div>')
		self.filename	= between(html, '<div class="if">', '</div>')
		self.bytes	= between(html, '<div class="ib">', '</div>')
		self.date	= between(html, '<div class="id">', '</div>')
		self.public	= between(html, '<div class="ip">', '</div>')
		self.tags	= between(html, '<div class="tags">', '</div></div></div>')
		self.account	= account

