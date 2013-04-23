#!/usr/bin/env python
import gtk.gdk
import puush

# Calculate the size of the whole screen
screenw = gtk.gdk.screen_width()
screenh = gtk.gdk.screen_height()

puush.screenshot(0, 0, screenw, screenh)