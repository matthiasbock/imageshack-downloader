#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

from htmlparser import between

class Image:
	def __init__(self, html):
		self.id		= between(html, '<div class="ii">', '</div>')
		self.server	= between(html, '<div class="is">', '</div>')
		self.folder		= between(html, '<div class="ib">', '</div>')
		self.filename	= between(html, '<div class="if">', '</div>')
		self.date		= between(html, '<div class="id">', '</div>')
		self.public	= between(html, '<div class="ip">', '</div>')
#		self.tags		= between(html, '<div class="tags">', '</div></div></div>')

		self.url		= "http://img"+self.server+".imageshack.us/img"+self.server+"/"+self.folder+"/"+self.filename

"""
http://imageshack.us/a/img521/1934/p1200867.jpg

<div id="i0">
	<div class="ii">785100844</div>
	<div class="is">521</div>
	<div class="if">p1200867.jpg</div>
	<div class="ib">1934</div>
	<div class="it">y</div>
	<div class="id">2011-12-16 05:42:56</div>
	<div class="ip">n</div>
	<div class="ic"></div>
	<div class="isz">176</div>
	<div class="ist">http://yfrog.com/ehp1200867j</div>
	<div class="tags">
		<div class="tag">
			<div class="id">72439013</div>
			<div class="tid">2800152</div>
			<div class="name">sampletag1</div>
		</div>
		<div class="tag">
			<div class="id">72439014</div>
			<div class="tid">2116</div>
			<div class="name">sampletag2</div>
		</div>
	</div>
</div>
"""