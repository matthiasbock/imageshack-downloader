#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

# config file parser
from ConfigParser import RawConfigParser

# HTTP client
from httpclient import HttpClient
from htmlparser import between

# JSON parser
import simplejson as json

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
                    'remember_me'   : '0'
                 }
        self.client.POST('https://api.imageshack.com/v2/user/login', params)

        # Server error, that sometimes happens        
        if str(self.client.Page).find("404 Not Found") > -1:
            return False

        # Parse response as JSON
        response = json.loads(str(self.client.Page))
        self.logged_in  = response["success"] is True
        if not self.logged_in:
            return False
        
        # Extract username and token from response
        # In the config file it could be the email address
        self.username   = response["result"]["username"]
        self.auth_token = response["result"]["auth_token"] 
        
        return True

    #
    # Images
    #
    def get_user_images(self):
        # Method:   GET https://api.imageshack.com/v2/user/<username>/images
        # Response: ImagesListModel
        
        # get total number of images
        self.client.GET("https://api.imageshack.com/v2/user/"+self.username+"/images?limit=1")
        
        response = json.loads(str(self.client.Page))
        if not response["success"] is True:
            print "Error!"
            return

        self.image_count = response["result"]["total"]

        # request a complete list of images
        self.client.GET("https://api.imageshack.com/v2/user/"+self.username+"/images?limit="+str(self.image_count))

        response = json.loads(str(self.client.Page))
        if not response["success"] is True:
            print "Error!"
            return        

        self.images = response["result"]
        
        return
