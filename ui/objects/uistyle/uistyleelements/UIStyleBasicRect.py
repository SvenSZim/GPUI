from typing import override

from ...idrawer import UISurface, UISurfaceDrawer
from ...generic import Rect
from .UIABCStyleRect import UIABCStyleRect

class UIStyleBasicRect(UIABCStyleRect):

	@override
	def render(self, drawer: UISurfaceDrawer, surface: UISurface, rect: Rect) -> None:
		"""
		render renders the given rect in the style of the UIStyleRect onto the given surface
		"""
		drawer.drawrect(surface, rect, 'white', fill=False)
		drawer.drawrect(surface, Rect((rect.left - 5, rect.top - 5), (rect.width + 10, rect.height + 10)), 'white', fill=False)