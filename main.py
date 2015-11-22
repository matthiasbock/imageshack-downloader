#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

from api import ImageShack_Account
from sys import exit
import os
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

print "Downloading:"
# to folder "images"
try:
    os.mkdir("images")
except:
    pass

# Download all images
counter         = 1
total           = frog.image_count
download_errors = []
for img in frog.images["images"]:
    # save image in a subfolder
    saveto = os.path.join("images", img["original_filename"])
    print str(counter)+" of "+str(total)+" ("+"{0:.2f}".format(float(counter)/total)+"%): "+img["original_filename"]
    counter += 1

    # invoke wget for downloading
    process = wget(img["direct_link"], saveto, frog.client.Cookies)
    process.wait()
    
    # remember all failed downloads
    if process.returncode != 0:
        download_errors.append(img["direct_link"])

print "Download completed."

# Print a list of the failed downloads
if len(download_errors) > 0:
    print "\nThere were errors attempting to download the following files:"
    for url in download_errors:
        print url
    print ""
