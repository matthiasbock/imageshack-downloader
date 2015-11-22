#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

from ConfigParser import RawConfigParser

from httpclient import HttpClient
from htmlparser import between

def loadconfig():
	parser = RawConfigParser()
	parser.read('imageshack.conf')
	username = parser.get('Login', 'Username')
	password = parser.get('Login', 'Password')
	del parser

	return username, password

class ImageShack_Account:
	def __init__(self):
		self.r = HttpClient(debug=False)
		self.logged_in = False
		self.Images = None
		self.Tags = None
		self.Albums = None

	def login(self, username, password):
		# GET is sufficient
		#self.r.GET('imageshack.us/auth.php?username='+username+'&password'+password)

		# but we use POST, to check, if login was successfull
		self.r.POST('imageshack.us/auth.php', {'stay_logged_in':'true', 'format':'json', 'username':username, 'password':password})

		import simplejson
		json = simplejson.loads(str(self.r.Page))
		self.logged_in = json['status'] is True
		
		if self.logged_in:
			self.get_number_of_pages()
		
		return self.logged_in

	def __del__(self):
		try:
			self.r.GET('my.imageshack.us/logout.php')
		except:
			pass


	# Images

	def get_number_of_pages(self):
		self.r.GET('my.imageshack.us/images.php?ipage=1')

		# number of image pages
		self.pages = int(between(self.r.Page, '<input type="hidden" id="inumpages" value="', '"'))
		# number of images in total
		self.images = int(between(self.r.Page, '<input type="hidden" id="inumitems" value="', '"'))

	def get_images_on_page(self, ipage):
		self.r.GET('my.imageshack.us/images.php?ipage='+str(ipage))

		# number of images on current page
		current_page_images = int(between(self.r.Page, '<input type="hidden" id="inumcached" value="', '"'))

		# parse divs
		from parse_images import Image

		images = {}
		for i in range(current_page_images):
			# ix = id of image on current page
			img = Image( between(self.r.Page, '<div id="i'+str(i)+'">', '</div></div></div></div>', include_after=True) )

			# img.id = global id of image
			images[ img.id ] = img

		return images


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
			#self.Tags.append(Tag(between(self.r.Page, '<input type="hidden" id="tn'+str(page)+'_'+str(number)+'" value="', '"'), self))

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

		self.inumitems = int(between(self.r.Page, '<input type="hidden" id="inumitems" value="', '"'))		# galleries
		self.inumcached = int(between(self.r.Page, '<input type="hidden" id="inumcached" value="', '"'))	# number of galleries listed

		self.Albums = []
		#for i in range(self.inumcached):
		#	self.Albums.append(Album(between(self.r.Page, '<div id="i'+str(i)+'">', '</div></div>', include_after=True), self))
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


