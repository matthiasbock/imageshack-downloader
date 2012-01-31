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

	def download_image_list(self, ipage=1, tagid=-1):
		if not self.logged_in:
			if not self.login():
				return False

		self.r.GET('my.imageshack.us/images.php?ipage='+str(ipage)+'&tagid='+str(tagid)+'&rand='+rand() )

		self.inumpages = int(between(self.r.Page, '<input type="hidden" id="inumpages" value="', '"'))		# image page count
		self.inumitems = int(between(self.r.Page, '<input type="hidden" id="inumitems" value="', '"'))		# image count
		self.inumcached = int(between(self.r.Page, '<input type="hidden" id="inumcached" value="', '"'))	# number of images listed on current page

# values below are available but not used in the code, maybe at some pointer later
#		self.istartpage = int(between(self.r.Page, '<input type="hidden" id="istartpage" value="', '"'))	# 1
#		self.iendpage = int(between(self.r.Page, '<input type="hidden" id="iendpage" value="', '"'))		# page until which the cache works

		mc = memcache.Client(['127.0.0.1:11211'], debug=1)
		filenames = []
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
#			print pickle.loads(mc.get(image['filename']))['date']	# for debugging: read from memcache, what we just stored there
			filenames.append( image['filename'] )
		mc.set('imageshackfs-'+self.username+'-filenames', pickle.dumps(filenames))
		del mc
		self.got_image_list = True

	def get_image_list(self, ipage=1, tagid=-1):
		if not self.got_image_list:
			self.download_image_list(ipage, tagid)

		mc = memcache.Client(['127.0.0.1:11211'], debug=1)
		return pickle.loads( mc.get('imageshackfs-'+self.username+'-filenames') )

	def download_tag_list(self):
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
		mc.set('imageshackfs-'+self.username+'-tags', pickle.dumps(tags))
#		print pickle.loads(mc.get('imageshack-tags'))	# for debugging: read from memcache, what we just stored there
		del mc
		self.got_tag_list = True

	def get_tag_list(self):
		if not self.got_tag_list:
			self.download_tag_list()

		mc = memcache.Client(['127.0.0.1:11211'], debug=1)
		return pickle.loads( mc.get('imageshackfs-'+self.username+'-tags') )

	def download_album_list(self):
		if not self.logged_in:
			if not self.login():
				return False
		
		self.r.GET('my.imageshack.us/my_gallery/')
		self.r.Page.save()

		self.inumitems = int(between(self.r.Page, '<input type="hidden" id="inumitems" value="', '"'))		# galleries
		self.inumcached = int(between(self.r.Page, '<input type="hidden" id="inumcached" value="', '"'))	# number of galleries listed

		mc = memcache.Client(['127.0.0.1:11211'], debug=1)
		for i in range(self.inumcached):
			div = between(self.r.Page, '<div id="i'+str(i)+'">', '</div></div>', include_after=True)
			gallery = {
				'title'		: between(div, '<div class="igt">', '</div>'),
				'link'		: between(div, '<div class="ipl">', '</div>'),
				'created'	: between(div, '<div class="id">', '</div>'),
				'modified'	: between(div, '<div class="idm">', '</div>'),
				'server'	: between(div, '<div class="igs">', '</div>'),
				'preview'	: between(div, '<div class="ign">', '</div>')
				}
			mc.set(gallery['link'], pickle.dumps(gallery))
#			print pickle.loads(mc.get(gallery['link']))['title'] # for debugging: read from memcache, what we just stored there
		del mc

	def create_album(self, name):
		return

	def __del__(self):
		self.r.GET('my.imageshack.us/logout.php')

