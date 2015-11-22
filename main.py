#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

from configparser import loadconfig
username, password = loadconfig()

from api import ImageShack_Account

print 'Login ...'
frog = ImageShack_Account()
if frog.login(username, password):
	print 'success'
else:
	print 'login failed'
	from sys import exit
	exit()

print 'Number of images: '+str(frog.images)
print 'Number of pages: '+str(frog.pages)

# download all images
from os import mkdir
from wget import wget

# all pages
try:
	mkdir('images')
except:
	pass
for page in range(frog.pages):
	# put in a separate folder
	folder = 'page'+str(page+1).zfill(2)
	print folder+' ...'
#	try:
#		mkdir(folder)
#	except:
#		pass
	folder = 'images'

	# all images
	images = frog.get_images_on_page(page+1)
	processes = []
	for i in images.keys():
		processes.append( wget(images[i].url, folder+'/'+images[i].filename, frog.r.Cookies) )
	print str(len(processes))+' download processes started. Waiting for all downloads to finish before continuing ...'
	for p in processes:
		p.wait()

print 'completed.'

#print 'Requesting album list ...'
#albums = i.get_album_list()
#print len(albums)
#for album in albums:
#	print album.title

