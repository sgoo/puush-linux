#!/usr/bin/env python

import gtk
from time import sleep
from cairo import OPERATOR_CLEAR, OPERATOR_OVER

from puush import screenshot


class PuushArea:
	def __init__(self):
		self.origin = None
		self.area = [0, 0]
		self.takeSS = False

	def mousePress(self, w, e):
		self.origin = (e.x, e.y)

	def keyPress(self, w, e):
		if e.keyval == gtk.keysyms.Escape:
			gtk.main_quit()

	def mouseMove(self, w, e):
		if not self.origin:
			return

		self.area = (e.x - self.origin[0], e.y - self.origin[1])
		self.updateWindow()

	def mouseRelease(self, w, e):
		self.takeSS = True
		self.window.destroy()

	def updateWindow(self):
		self.drawingArea.window.invalidate_rect((0, 0, self.screenw, self.screenh), True)

	def drawWindow(self, w, e):
		cr = w.window.cairo_create()
		cr.set_operator(OPERATOR_CLEAR)
		cr.rectangle(*e.area)
		cr.fill()
		cr.set_operator(OPERATOR_OVER)

		if self.area and self.origin:
			cr.set_source_rgba(0.7, 0.7, 0.7, 0.1)

			cr.rectangle(self.origin[0], self.origin[1], self.area[0], self.area[1])
			cr.fill()

	def buildWindow(self):
		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.window.connect('destroy', lambda w: gtk.main_quit())

		self.drawingArea = gtk.DrawingArea()
		self.window.add(self.drawingArea)

		self.screenw = gtk.gdk.screen_width()
		self.screenh = gtk.gdk.screen_height()

		self.window.set_flags(gtk.CAN_FOCUS)
		self.window.set_decorated(False)
		self.window.set_has_frame(False)
		# self.window.set_resizable(True);
		self.window.set_type_hint(gtk.gdk.WINDOW_TYPE_HINT_POPUP_MENU)
		self.drawingArea.set_size_request(self.screenw, self.screenh)
		self.window.set_app_paintable(True)

		# This sets the windows color-map, so it supports transparency.
		# This will only work if the WM support alpha channel
		self.window.set_colormap(self.window.get_screen().get_rgba_colormap())

		self.window.add_events(gtk.gdk.KEY_PRESS_MASK | gtk.gdk.BUTTON_PRESS_MASK | gtk.gdk.BUTTON_MOTION_MASK | gtk.gdk.BUTTON_RELEASE_MASK)

		self.window.connect('button_press_event', self.mousePress)
		self.window.connect('button_release_event', self.mouseRelease)
		self.window.connect('key-press-event', self.keyPress)
		self.window.connect('motion-notify-event', self.mouseMove)
		self.drawingArea.connect('expose-event', self.drawWindow)

		self.window.show_all()

		self.drawingArea.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.TCROSS))

	def doPuush(self):
		if self.takeSS:
			# Wait for overlay to disappear
			# There should be a better way to do this...
			sleep(0.5)

			if self.area[0] != 0 and self.area[1] != 0:
				x = int(min(self.origin[0], self.origin[0] + self.area[0]))
				y = int(min(self.origin[1], self.origin[1] + self.area[1]))
				w = int(abs(self.area[0]))
				h = int(abs(self.area[1]))

				screenshot(x, y, w, h)


if __name__ == '__main__':
	pa = PuushArea()
	pa.buildWindow()
	gtk.main()
	pa.doPuush()
