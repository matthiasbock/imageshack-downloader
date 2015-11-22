#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

from api import ImageShack_Account
from sys import exit
from os import mkdir
from wget import wget

print "Login ..."
frog = ImageShack_Account()
if frog.authenticate():
    print "User "+frog.username+" successfully logged in."
else:
    print "Error: Login failed."
    exit()

print "Requesting a list of "+frog.username+"'s images..."
frog.get_user_images()
print "User has "+str(frog.image_count)+" image(s) online."

exit()

# iterate over all image pages
try:
    mkdir('images')
except:
    pass
for page in range(frog.pages):
    # put in a separate folder
    folder = 'page'+str(page+1).zfill(2)
    print folder+' ...'
#    try:
#        mkdir(folder)
#    except:
#        pass
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
