# imageshack-downloader

Python scripts to download all your images from the image hoster imageshack.com/us. <br/>
Especially relevant in the light of the forthcoming deletion of all free accounts in January 2016.

Read more about that:
https://medium.com/@ImageShack/3984af30964e

License: GNU GPLv3

## Usage

Clone this repo and create a file named imageshack.conf with the following content:
<pre>
[Login]
Username=your username
Password=your password
</pre>
Run:
<pre>./main.py</pre>
or
<pre>python main.py</pre>

Depends on python-simplejson, python-configparser and wget.
