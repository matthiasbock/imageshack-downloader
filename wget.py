#!/usr/bin/python

def wget(url, saveto, cookies):
	from subprocess import Popen
	from shlex import split

	Cookie = 'Cookie: '
	for key in cookies.keys():
		Cookie += key+'='+cookies[key]+';'

	p=Popen( split('/usr/bin/wget "'+url+'" --output-document="'+saveto+'" --header="'+Cookie+'" --timeout=2 --tries=1 --no-verbose') )

	from time import sleep
	sleep(0.4)
	
	return p
