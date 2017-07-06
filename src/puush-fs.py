#!/usr/bin/env python

from gtk.gdk import screen_width, screen_height

from puush import screenshot


screenshot(0, 0, screen_width(), screen_height())
