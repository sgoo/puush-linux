#!/usr/bin/env python

from gtk.gdk import screen_get_default

from puush import screenshot


if __name__ == '__main__':

	# Get the root and active window
	root = screen_get_default()

	if root.supports_net_wm_hint('_NET_ACTIVE_WINDOW') and root.supports_net_wm_hint('_NET_WM_WINDOW_TYPE'):
		# You definitely do not want to take a screen-shot of the whole desktop, see entry 23.36 for that
		# Returns something like ('ATOM', 32, ['_NET_WM_WINDOW_TYPE_DESKTOP'])

		active = root.get_active_window()
		if active.property_get('_NET_WM_WINDOW_TYPE')[-1][0] == '_NET_WM_WINDOW_TYPE_DESKTOP':
			exit(-1)

		# Calculate the size of the WM decorations
		relative_x, relative_y, win_w, win_h, d = active.get_geometry()
		width = win_w + (relative_x - 10)
		height = win_h + (relative_y - 10)

		# Calculate the position of where the WM decorations start (not the window itself)
		screenpos_x, screenpos_y = active.get_root_origin()

	else:
		exit(-1)

	screenshot(screenpos_x, screenpos_y, width, height)
