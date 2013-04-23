import config
import time
import multipart
import StringIO
# from gi.repository import Gtk, Gdk
import gtk
import os
import pynotify

SERVER = 'puush.me'
API_END_POINT = '/api/tb'
FORMAT = 'png'

def screenshot(x, y, w, h):

	screenshot = gtk.gdk.Pixbuf.get_from_drawable(gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, True, 8, w, h),
		gtk.gdk.get_default_root_window(),
		gtk.gdk.colormap_get_system(),
		x, y, 0, 0, w, h)

	_postSS(screenshot)


def _postSS(screenshot):

	fileName = time.strftime('ss (%Y-%m-%d at %H.%M.%S).' + FORMAT)

	# split the apiKey for the basicAuth
	config.apiKey = config.apiKey.lower()
	l = int(len(config.apiKey)/2)
	basicAuth = (config.apiKey[:l], config.apiKey[l:])

	# save file into buf
	picBuf = StringIO.StringIO()
	screenshot.save_to_callback(_saveToBuf, FORMAT, {}, {'buf' :picBuf})

	# build file list
	fileList = [('media', fileName, picBuf.getvalue())]

	link = multipart.post_multipart(SERVER, 'http://%s%s' % (SERVER, API_END_POINT), files=fileList, basicAuth=basicAuth)
	# link = "<mediaurl>http://puu.sh/2ES4o.png</mediaurl>"
	print link
	
	# link looks like "<mediaurl>http://puu.sh/2ES4o.png</mediaurl>"
	# strip open and close tags
	link = link[10:len(link) - 11]

	clip = gtk.clipboard_get ('CLIPBOARD')

	clip.set_text(link, -1)
	clip.store()

	if pynotify.init("puush"):
		n = pynotify.Notification("Puush completed", link)
		with open(os.path.dirname(__file__) + '/icon.png') as logo:
			loader = gtk.gdk.PixbufLoader('png')
			loader.write(logo.read())
			loader.close()
			n.set_icon_from_pixbuf(loader.get_pixbuf())
		n.show()
	else:
		print "Error starting pynotify"

	
def _saveToBuf(buf, d):
	d['buf'].write(buf)
