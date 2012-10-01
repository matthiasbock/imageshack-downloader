#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

from configparser import loadconfig
username, password = loadconfig()

from imageshack import ImageShack

print 'Login ...'
i = ImageShack(username, password)

print 'Requesting image list ...'
images = i.get_image_list()
print 'server says: '+str(i.inumitems)+' images in this account'
print 'I found '+str(len(images))+' images in this account'
for image in images:
	URL = "http://img"+image.server+".imageshack.us/img"+image.server+"/88/"+image.filename
	print URL
	i.r.GET(URL)
	i.r.Page.save(filename=image.filename)

#print 'Requesting album list ...'
#albums = i.get_album_list()
#print len(albums)
#for album in albums:
#	print album.title

