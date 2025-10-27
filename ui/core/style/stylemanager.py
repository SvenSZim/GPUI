import xml.etree.ElementTree as ET
from typing import Optional

from ...utility import StyledDefault

class StyleManager:
    """Central registry for UI render styles.

    The StyleManager stores parsed XML style fragments (as ElementTree
    nodes) keyed by a style name. Each style is a mapping from element
    tags (e.g. 'button', 'text') to the XML element that defines the
    default rendering properties for that element.

    Responsibilities:
    - Register named style collections via :meth:`addStyle`
    - Query available styles via :meth:`getAllStyles`
    - Configure a global default style via :meth:`setDefaultStyle`
    - Fetch style nodes for specific element types via
        :meth:`getStyledElementNode` and :meth:`getDefault`

    Notes:
    - Style names are stored as provided (case-sensitive). Callers
        should normalize names if they require case-insensitive lookups.
    - The stored values are ElementTree `ET.Element` nodes and are not
        copied by the manager; consumers should copy them if they will
        mutate the nodes.
    """

    styles: dict[str, dict[str, ET.Element]] = {}

    # Name of the globally active default style (empty = none)
    defaultStyle: str = ''

    @staticmethod
    def addStyle(name: str, styledElements: dict[str, ET.Element]) -> None:
        """Register a named style collection.

        Args:
            name: Style name to register. Existing entries with the same
                name will be overwritten.
            styledElements: Mapping from element tag to an
                ElementTree `ET.Element` describing the style.

        Returns:
            None

        Example:
            StyleManager.addStyle('dark', {'button': button_node})
        """
        StyleManager.styles[name] = styledElements

    @staticmethod
    def getAllStyles() -> list[str]:
        """Return a list of registered style names.

        Returns:
            List of style names currently registered in the manager.
        """
        return list(StyleManager.styles.keys())

    @staticmethod
    def setDefaultStyle(style: str) -> bool:
        """Set the globally active default style.

        Args:
            style: Name of a previously registered style.

        Returns:
            True if the style was set successfully, False if no such
            registered style exists.
        """
        if style in StyleManager.styles:
            StyleManager.defaultStyle = style
            return True
        return False

    @staticmethod
    def getStyledElementNode(element: str, stylename: str) -> Optional[ET.Element]:
        """Retrieve the style node for a specific element type.

        Args:
            element: Element tag name (e.g. 'button', 'text').
            stylename: Registered style name to query.

        Returns:
            The ElementTree node for the requested element in the
            specified style, or None if the style or element is not
            found.

        Notes:
            - This performs an exact (case-sensitive) lookup of the
              style name and element tag.
        """
        if stylename in StyleManager.styles:
            if element in StyleManager.styles[stylename]:
                return StyleManager.styles[stylename][element]
        return None

    @staticmethod
    def getDefault(tag: StyledDefault) -> Optional[ET.Element]:
        """Get the style node for `tag` from the current default style.

        Args:
            tag: A `StyledDefault` enum or similar value used to identify
                the element type.

        Returns:
            The ElementTree node for the tag from the active default
            style, or None if no default style is set or the node is
            not present.
        """
        if StyleManager.defaultStyle in StyleManager.styles:
            return StyleManager.getStyledElementNode(str(tag), StyleManager.defaultStyle)
        return None
