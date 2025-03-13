from abc import ABC
from typing import Union

from ...generic import Color
from .UIABCStyleElement import UIABCStyleElement

class UIStyleColor(UIABCStyleElement):
	"""
	UIStyleColor is a wrapper class for color as styling element
	"""

	color: Color

	def __init__(self, color: Union[str, tuple[int, int, int], Color]) -> None:
		"""
		__init__ initializes the UIStyleColor instance

		Args:
			color: Color = the color of the UIStyleColor
		"""
		if not isinstance(color, Color):
			color = Color(color)
		self.color = color

	def getColor(self) -> Color:
		"""
		getColor returns the color value of the UIStyleColor

		Returns:
			Color = color value of the UIStyleColor
		"""
		return self.color