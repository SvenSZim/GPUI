
from ..uiobjectbody import UIABCBody
from .UIABCText import UIABCText

class UIText(UIABCText):
	"""
	UIText is the most basic implementation of the UIABCText.
	It is used to store basic textcontainer for rendering.
	"""

	def __init__(self, body: UIABCBody, content: str, ) -> None:
		"""
		__init__ initializes the UIText instance

		Args:
			content: str = the text-content of the UIText
			body: UIABCBody = the body of the UIText
		"""
		super().__init__(body, content)
