
from ..uiobjectbody import UIABCBody
from ..uiobject import UIABCObject
from .UIABCText import UIABCText

class UIText(UIABCText):
	"""
	UIText is the most basic implementation of the UIABCText.
	It is used to store basic textcontainer for rendering.
	"""

	def __init__(self, objectBody: UIABCBody, content: str) -> None:
		"""
		__init__ initializes the UIText instance

		Args:
			objectBody: UIABCBody = the body of the UIText
			content: str = the text-content of the UIText
		"""
		self.body = objectBody
		UIABCObject.update(self) #explicitly calls the update function from UIObject (in case it gets overwritten)

		self.content = content