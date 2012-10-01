#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

from robot import Robot
import random
from htmlparser import between
import pickle
from math import ceil

from image import Image
from album import Album
from tag import Tag

def rand():
	return '0.'+''.join([str(random.randint(0,9)) for i in range(16)])	# 0.xxxxxxxxxxxxxxxx

class ImageShack:
	def __init__(self, username=None, password=None):
		self.reset()
		self.username = username
		self.password = password

	def reset(self):
		random.seed()
		self.r = Robot(debug=False)
		self.logged_in = False
		self.Images = None
		self.Tags = None
		self.Albums = None

	def login(self, username=None, password=None):
		if username is None or password is None:
			username = self.username
			password = self.password
		if username is None or password is None:
			return False

		self.r.POST('imageshack.us/auth.php', {'stay_logged_in':'true', 'format':'json', 'username':username, 'password':password})

		import simplejson
		json = simplejson.loads(str(self.r.Page))
		self.logged_in = json['status'] is True
		return self.logged_in

	def __del__(self):
		try:
			self.r.GET('my.imageshack.us/logout.php')
		except:
			pass

	# Images

	def download_image_list(self, ipage=1, tagid=-1):
		if not self.logged_in:
			if not self.login():
				return False

		self.r.GET('my.imageshack.us/images.php?ipage='+str(ipage)+'&tagid='+str(tagid)+'&rand='+rand() )

		self.inumpages = int(between(self.r.Page, '<input type="hidden" id="inumpages" value="', '"'))		# image pages
		self.inumitems = int(between(self.r.Page, '<input type="hidden" id="inumitems" value="', '"'))		# image count
		self.inumcached = int(between(self.r.Page, '<input type="hidden" id="inumcached" value="', '"'))	# images on current page

		self.Images = []
		for i in range(self.inumcached):
			self.Images.append(Image(between(self.r.Page, '<div id="i'+str(i)+'">', '</div></div></div></div>', include_after=True), self))

	def get_image_list(self, ipage=1, tagid=-1):
		if self.Images is None:
			self.download_image_list(ipage, tagid)
		return self.Images

	# Tags

	def download_tag_list(self):
		if not self.logged_in:
			if not self.login():
				return False

		self.r.GET('my.imageshack.us/v_images.php')

		self.tnumitems = int(between(self.r.Page, '<input type="hidden" id="tnumitems"    value="', '"'))

		self.Tags = []
		tags_per_page = 20
		for i in range(self.tnumitems):
			page = i / tags_per_page
			number = i % tags_per_page
			self.Tags.append(Tag(between(self.r.Page, '<input type="hidden" id="tn'+str(page)+'_'+str(number)+'" value="', '"'), self))

		self.got_tag_list = True

	def get_tag_list(self):
		if self.Tags is None:
			self.download_tag_list()
		return self.Tags

	# Albums

	def download_album_list(self):
		if not self.logged_in:
			if not self.login():
				return False
		
		self.r.GET('my.imageshack.us/my_gallery/')
		self.r.Page.save()

		self.inumitems = int(between(self.r.Page, '<input type="hidden" id="inumitems" value="', '"'))		# galleries
		self.inumcached = int(between(self.r.Page, '<input type="hidden" id="inumcached" value="', '"'))	# number of galleries listed

		self.Albums = []
		for i in range(self.inumcached):
			self.Albums.append(Album(between(self.r.Page, '<div id="i'+str(i)+'">', '</div></div>', include_after=True), self))
		self.got_album_list = True

	def get_album_list(self):
		if self.Albums is None:
			self.download_album_list()
		return self.Albums

	# Methods

	def upload_image(self, path):
		return

	def delete_image(self, image):
		return

	def add_tag(self, picture, tag):
		return

	def delete_tag(self, picture, tag):
		return

	def create_album(self, name):
		return

	def delete_album(self, album):
		return

	def add_to_album(self, album, image):
		return

	def delete_from_album(self, album, image):
		return

	def set_album_cover(self, album, image):
		return

	def change_sort_order(self, album, image, position):
		return


