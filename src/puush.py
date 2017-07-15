
import gtk
from os.path import dirname
from StringIO import StringIO
from time import sleep, strftime
from subprocess import check_call
from multipart import post_multipart
from pynotify import init, Notification

import config


FORMAT = 'png'
NOTIFY_TIMEOUT = 10


def screenshot(x, y, w, h):
	screenshot = gtk.gdk.Pixbuf.get_from_drawable(gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, True, 8, w, h), gtk.gdk.get_default_root_window(), gtk.gdk.colormap_get_system(), x, y, 0, 0, w, h)

	# Split the apiKey for the basicAuth
	config.apiKey = config.apiKey.lower()
	l = int(len(config.apiKey) / 2)
	basicAuth = (config.apiKey[:l], config.apiKey[l:])

	# Save file into the buffer
	pictureBuffer = StringIO()
	screenshot.save_to_callback(_saveToBuf, FORMAT, {}, {'buffer': pictureBuffer})

	link = post_multipart('puush.me', '/api/tb', files=[('media', strftime('ss (%Y-%m-%d at %H.%M.%S).' + FORMAT), pictureBuffer.getvalue())], basicAuth=basicAuth)

	# At this step, the link looks like '<mediaurl>http://puu.sh/2ES4o.png</mediaurl>'
	if link and link != 'Unauthorized':
		link = link.partition('<mediaurl>')[2].rpartition('</mediaurl>')[0]

	# Notify the user with the link provided (or an error, see below !)
	_notify(link)


def _notify(link):
	if link and link != 'Unauthorized':
		try:
			cmd = 'echo ' + link.strip() + ' | xclip -selection c.'
			check_call(cmd, shell=True)

		# The error for 'command not found' is subprocess.CalledProcessError
		except Exception as e:
			clip = gtk.clipboard_get('CLIPBOARD')
			clip.set_text(link, -1)
			clip.store()

	if init('puush'):
		if not link:
			n = Notification('Puush failed', 'You should check your Internet connection', 'file://' + dirname(__file__) + '/error.png')

		else:
			if link == 'Unauthorized':
				n = Notification('Puush failed', 'Your API key has been rejected', 'file://' + dirname(__file__) + '/warning.png')

			else:
				n = Notification('Puush completed', link, 'file://' + dirname(__file__) + '/success.png')

		n.show()
		sleep(NOTIFY_TIMEOUT)
		n.close()

	else:
		print 'Error starting PyNotify'


def _saveToBuf(buffer, d):
	d['buffer'].write(buffer)
