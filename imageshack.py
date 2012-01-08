#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

from robot import Robot
import random
from htmlparser import between
import memcache
import pickle
from math import ceil

class ImageShack:
	def __init__(self, username=None, password=None):
		self.username = username
		self.password = password
		self.r = Robot(debug=True)
		self.logged_in = False
		random.seed()

	def login(self, username=None, password=None):
		if username is None or password is None:
			username = self.username
			password = self.password
		if username is None or password is None:
			return False

		self.r.POST('imageshack.us/auth.php', {'stay_logged_in':'true', 'format':'json', 'username':username, 'password':password})
		print str(self.r.Page)
		return True

	def get_picture_list(self, ipage, tagid=-1):
		if not self.logged_in:
			if not self.login():
				return False

		rand = '0.'+''.join([str(random.randint(0,9)) for i in range(16)])
		self.r.GET('my.imageshack.us/images.php?ipage='+str(ipage)+'&tagid='+str(tagid)+'&rand='+rand)

		self.inumpages = int(between(self.r.Page, '<input type="hidden" id="inumpages" value="', '"'))		# pages
		self.inumitems = int(between(self.r.Page, '<input type="hidden" id="inumitems" value="', '"'))		# images
#		self.istartpage = int(between(self.r.Page, '<input type="hidden" id="istartpage" value="', '"'))	# 1
#		self.iendpage = int(between(self.r.Page, '<input type="hidden" id="iendpage" value="', '"'))		# page until which the cache works
		self.inumcached = int(between(self.r.Page, '<input type="hidden" id="inumcached" value="', '"'))	# number of images listed

		mc = memcache.Client(['127.0.0.1:11211'], debug=1)
		for i in range(self.inumcached):
			div = between(self.r.Page, '<div id="i'+str(i)+'">', '</div></div></div></div>', include_after=True)
			image = {
				'id'		: between(div, '<div class="ii">', '</div>'),
				'server'	: between(div, '<div class="is">', '</div>'),
				'filename'	: between(div, '<div class="if">', '</div>'),
				'bytes'		: between(div, '<div class="ib">', '</div>'),
				'date'		: between(div, '<div class="id">', '</div>'),
				'public'	: between(div, '<div class="ip">', '</div>'),
				'tags'		: between(div, '<div class="tags">', '</div></div></div>')
				}
			mc.set(image['filename'], pickle.dumps(image))
#			print pickle.loads(mc.get(image['filename']))['date']
		del mc

	def get_tag_list(self):
		if not self.logged_in:
			if not self.login():
				return False

		self.r.GET('my.imageshack.us/v_images.php')

		self.tnumitems = int(between(self.r.Page, '<input type="hidden" id="tnumitems"    value="', '"'))

		tags = []
		tags_per_page = 20
		for i in range(self.tnumitems):
			page = i/tags_per_page
			number = i % tags_per_page
			tag = between(self.r.Page, '<input type="hidden" id="tn'+str(page)+'_'+str(number)+'" value="', '"')
			tags.append(tag)

		mc = memcache.Client(['127.0.0.1:11211'], debug=1)
		mc.set('imageshack-tags', pickle.dumps(tags))
		print pickle.loads(mc.get('imageshack-tags'))
		del mc

