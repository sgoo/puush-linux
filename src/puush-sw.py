#!/usr/bin/env python
import gtk.gdk
import puush


# Original single window ss code from
# https://gist.github.com/s1n4/1459140

 
# Calculate the size of the whole screen
screenw = gtk.gdk.screen_width()
screenh = gtk.gdk.screen_height()
 
# Get the root and active window
root = gtk.gdk.screen_get_default()
 
if root.supports_net_wm_hint("_NET_ACTIVE_WINDOW") and root.supports_net_wm_hint("_NET_WM_WINDOW_TYPE"):
	active = root.get_active_window()
	# You definately do not want to take a screenshot of the whole desktop, see entry 23.36 for that
	# Returns something like ('ATOM', 32, ['_NET_WM_WINDOW_TYPE_DESKTOP'])
	if active.property_get("_NET_WM_WINDOW_TYPE")[-1][0] == '_NET_WM_WINDOW_TYPE_DESKTOP' :
		print False
 
	# Calculate the size of the wm decorations
	relativex, relativey, winw, winh, d = active.get_geometry() 
	w = winw + (relativex*2)
	h = winh + (relativey+relativex)
 
	# Calculate the position of where the wm decorations start (not the window itself)
	screenposx, screenposy = active.get_root_origin()
else:
	print False

puush.screenshot(screenposx, screenposy, w, h)
 
 



# send 
# urllib2.Request('')


# curl --form "media=@es760a1_plot.png" http://f27f2121f28c700b:68ef2876c7d7833d@puush.me/api/tb;echo;echo;

