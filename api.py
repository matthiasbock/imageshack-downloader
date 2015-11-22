#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

# config file parser
from ConfigParser import RawConfigParser

# HTTP client
from httpclient import HttpClient
from htmlparser import between

# JSON parser
from simplejson import loads,dumps

#
# Object to hold authentication token
# and provide methods to access imageshack.com
#
class ImageShack_Account:

    def __init__(self):
        self.client = HttpClient(debug=False)
        self.logged_in = False
        self.images = None
        self.albums = None
        self.tags = None

    def authenticate(self):
        #
        # Open imageshack.conf
        # and read username and password
        # to use as login credentials 
        #
        parser = RawConfigParser()
        parser.read('imageshack.conf')
        username = parser.get('Login', 'Username')
        password = parser.get('Login', 'Password')
        del parser

        # POSTing requires an API key
        api_key = open("api_key.txt").read()

        #
        # Authentication:
        # POST to https://api.imageshack.com/v2/user/login
        # see http://api.imageshack.us/
        #
        params = {
                    'api_key'       : api_key,
                    'username'      : username,
                    'password'      : password,
                    'set_cookies'   : '1',
                    'remember_me'   : '1'
                 }
        self.client.POST('https://api.imageshack.com/v2/user/login', params)

        print str(self.client.Page)

        # Parse response as JSON
        json = loads(str(self.client.Page))
        self.logged_in = json["success"] is True

        # Extract username from response
        # In the config file it could be the email address
        self.username = json["result"]["username"]
        
        return self.logged_in

    #
    # Images
    #
    def get_user_images(self):
        #GET https://api.imageshack.com/v2/user/<username>/images
        return
        
        
    def get_number_of_pages(self):
        self.client.GET('my.imageshack.us/images.php?ipage=1')

        # number of image pages
        self.pages = int(between(self.client.Page, '<input type="hidden" id="inumpages" value="', '"'))
        # number of images in total
        self.images = int(between(self.client.Page, '<input type="hidden" id="inumitems" value="', '"'))

    def get_images_on_page(self, ipage):
        self.client.GET('my.imageshack.us/images.php?ipage='+str(ipage))

        # number of images on current page
        current_page_images = int(between(self.client.Page, '<input type="hidden" id="inumcached" value="', '"'))

        # parse divs
        from parse_images import Image

        images = {}
        for i in range(current_page_images):
            # ix = id of image on current page
            img = Image( between(self.client.Page, '<div id="i'+str(i)+'">', '</div></div></div></div>', include_after=True) )

            # img.id = global id of image
            images[ img.id ] = img

        return images

    def upload_image(self, path):
        return

    def delete_image(self, image):
        return

    #
    # Tags
    #
    def get_tag_list(self):
        if self.Tags is None:
            self.download_tag_list()
        return self.Tags
        
    def download_tag_list(self):
        if not self.logged_in:
            if not self.login():
                return False

        self.client.GET('my.imageshack.us/v_images.php')

        self.tnumitems = int(between(self.client.Page, '<input type="hidden" id="tnumitems"    value="', '"'))

        self.Tags = []
        tags_per_page = 20
        for i in range(self.tnumitems):
            page = i / tags_per_page
            number = i % tags_per_page
            #self.Tags.append(Tag(between(self.client.Page, '<input type="hidden" id="tn'+str(page)+'_'+str(number)+'" value="', '"'), self))

        self.got_tag_list = True

    def add_tag(self, picture, tag):
        return

    def delete_tag(self, picture, tag):
        return

    #
    # Albums
    #
    def get_album_list(self):
        if self.Albums is None:
            self.download_album_list()
        return self.Albums

    def download_album_list(self):
        if not self.logged_in:
            if not self.login():
                return False
        
        self.client.GET('my.imageshack.us/my_gallery/')

        self.inumitems = int(between(self.client.Page, '<input type="hidden" id="inumitems" value="', '"'))        # galleries
        self.inumcached = int(between(self.client.Page, '<input type="hidden" id="inumcached" value="', '"'))    # number of galleries listed

        self.Albums = []
        #for i in range(self.inumcached):
        #    self.Albums.append(Album(between(self.client.Page, '<div id="i'+str(i)+'">', '</div></div>', include_after=True), self))
        self.got_album_list = True
    
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
