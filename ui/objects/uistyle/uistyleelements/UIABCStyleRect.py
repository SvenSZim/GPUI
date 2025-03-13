from abc import ABC, abstractmethod

from ...generic import Rect
from ...idrawer import UISurface
from .UIABCStyleElement import UIABCStyleElement
from .UIStyleColor import UIStyleColor

class UIABCStyleRect(UIABCStyleElement, ABC):
	"""
	UIABCStyleRect is the abstract base class for all UIStyleRects
	"""

	@abstractmethod
	def render(self, surface: UISurface, rect: Rect) -> None:
		"""
		render renders the given rect in the style of the UIStyleRect onto the given surface
		"""
		pass