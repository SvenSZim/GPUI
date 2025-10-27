from abc import ABC

from ...utility import Parsable

class ElementData(Parsable, ABC):
    """ElementData - Abstract base for UI element render data
    
    This class defines the interface for storing and parsing render-specific 
    attributes of UI elements (colors, borders, backgrounds, etc).

    Implementation Requirements:
    1. Subclasses must implement parseFromArgs() to validate and parse their
       specific render attributes from XML/dict input
    2. Use validateRequiredArgs() to check required parameters
    3. Store only render-related data - other state belongs in ElementCore
    4. Provide type hints and validation for all attributes
    5. Include clear error messages for invalid input
    6. Keep render properties private with appropriate getters/setters

    Example Implementation:
        @dataclass
        class CustomData(ElementData):
            color: str = 'black'
            border_width: int = 1

            @staticmethod
            def parseFromArgs(args: dict[str, Any]) -> 'CustomData':
                CustomData.validateRequiredArgs(args, ['color'])
                return CustomData(
                    color=args['color'],
                    border_width=int(args.get('border', 1))
                )
                
    See Also:
        ElementCore: Handles non-render element data and layout
        Parsable: Base class for XML parsing capabilities
    """
    pass
