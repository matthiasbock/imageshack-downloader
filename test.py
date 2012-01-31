#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

from config import loadconfig
username, password = loadconfig()

from imageshack import ImageShack

print 'Login ...'
i = ImageShack(username, password)

#print 'Requesting image list ...'
#l = i.get_image_list()
#print l
#print len(l)

print 'Requesting tag list ...'
print i.get_tag_list()

