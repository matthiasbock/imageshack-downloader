#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

from robot import Robot
import random
from htmlparser import between
import memcache
import pickle
from math import ceil

def rand():
	return '0.'+''.join([str(random.randint(0,9)) for i in range(16)])	# 0.xxxxxxxxxxxxxxxx

class Image:
	def __init__(self, html):
		self.id		= between(html, '<div class="ii">', '</div>')
		self.server	= between(html, '<div class="is">', '</div>')
		self.filename	= between(html, '<div class="if">', '</div>')
		self.bytes	= between(html, '<div class="ib">', '</div>')
		self.date	= between(html, '<div class="id">', '</div>')
		self.public	= between(html, '<div class="ip">', '</div>')
		self.tags	= between(html, '<div class="tags">', '</div></div></div>')

class Album:
	def __init__(self, html):
		self.title	= between(html, '<div class="igt">', '</div>')
		self.link	= between(html, '<div class="ipl">', '</div>')
		self.created	= between(html, '<div class="id">', '</div>')
		self.modified	= between(html, '<div class="idm">', '</div>')
		self.server	= between(html, '<div class="igs">', '</div>')
		self.preview	= between(html, '<div class="ign">', '</div>')

class ImageShack:
	def __init__(self, username=None, password=None):
		self.reset()
		self.username = username
		self.password = password

	def reset(self):
		random.seed()
		self.r = Robot(debug=False)
		self.logged_in = False
		self.got_image_list = False
		self.got_tag_list = False
		self.got_album_list = False

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

		mc = memcache.Client(['127.0.0.1:11211'], debug=1)
		filenames = []
		for i in range(self.inumcached):
			image = Image( between(self.r.Page, '<div id="i'+str(i)+'">', '</div></div></div></div>', include_after=True) )
			mc.set( image.filename, pickle.dumps(image) )
			filenames.append( image.filename )
		mc.set('imageshackfs-'+self.username+'-filenames', pickle.dumps(filenames))
		self.got_image_list = True

	def get_image_list(self, ipage=1, tagid=-1):
		if not self.got_image_list:
			self.download_image_list(ipage, tagid)

		mc = memcache.Client(['127.0.0.1:11211'], debug=1)
		return pickle.loads( mc.get('imageshackfs-'+self.username+'-filenames') )

	# Tags

	def download_tag_list(self):
		if not self.logged_in:
			if not self.login():
				return False

		self.r.GET('my.imageshack.us/v_images.php')

		self.tnumitems = int(between(self.r.Page, '<input type="hidden" id="tnumitems"    value="', '"'))

		tags = []
		tags_per_page = 20
		for i in range(self.tnumitems):
			page = i / tags_per_page
			number = i % tags_per_page
			tag = between(self.r.Page, '<input type="hidden" id="tn'+str(page)+'_'+str(number)+'" value="', '"')
			tags.append(tag)

		mc = memcache.Client(['127.0.0.1:11211'], debug=1)
		mc.set('imageshackfs-'+self.username+'-tags', pickle.dumps(tags))
		self.got_tag_list = True

	def get_tag_list(self):
		if not self.got_tag_list:
			self.download_tag_list()

		mc = memcache.Client(['127.0.0.1:11211'], debug=1)
		return pickle.loads( mc.get('imageshackfs-'+self.username+'-tags') )

	# Albums

	def download_album_list(self):
		if not self.logged_in:
			if not self.login():
				return False
		
		self.r.GET('my.imageshack.us/my_gallery/')
		self.r.Page.save()

		self.inumitems = int(between(self.r.Page, '<input type="hidden" id="inumitems" value="', '"'))		# galleries
		self.inumcached = int(between(self.r.Page, '<input type="hidden" id="inumcached" value="', '"'))	# number of galleries listed

		albums = []
		mc = memcache.Client(['127.0.0.1:11211'], debug=1)
		for i in range(self.inumcached):
			gallery = Album( between(self.r.Page, '<div id="i'+str(i)+'">', '</div></div>', include_after=True) )
			mc.set( gallery.link, pickle.dumps(gallery) )
			albums.append( gallery )
		mc.set('imageshackfs-'+self.username+'-albums', pickle.dumps(albums))
		self.got_album_list = True

	def get_album_list(self):
		if not self.got_album_list:
			self.download_album_list()

		mc = memcache.Client(['127.0.0.1:11211'], debug=1)
		return pickle.loads( mc.get('imageshackfs-'+self.username+'-albums') )

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


