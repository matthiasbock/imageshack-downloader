#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

from config import loadconfig
username, password = loadconfig()

from imageshack import ImageShack

print 'Login ...'
i = ImageShack(username, password)

print 'Requesting image list ...'
images = i.get_image_list()
print len(images)

print 'Requesting album list ...'
i.get_album_list()


