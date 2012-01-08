#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

from config import loadconfig
username, password = loadconfig()

from imageshack import ImageShack

i = ImageShack(username, password)
i.get_tag_list()
