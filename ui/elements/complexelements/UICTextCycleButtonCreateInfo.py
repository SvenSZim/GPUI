
from .UIABCComplexCreateInfo import UIABCComplexCreateInfo

@dataclass
class UICTextCycleButtonCreateInfo(UIABCComplexCreateInfo):
	contents: list[str]