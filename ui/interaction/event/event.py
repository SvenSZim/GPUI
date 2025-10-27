
class Event:
    """
    A container class for managing event callbacks in a priority-based event system.

    Event objects manage a collection of callback subscriptions that can be triggered
    in priority order. When an event is triggered, all subscribed callbacks are
    executed according to their priority levels.

    Features:
    - Maintains ordered list of callback IDs
    - Supports subscription/unsubscription during runtime
    - Returns immutable copy of subscriptions when triggered
    - Thread-safe callback list management

    Example:
        event = Event()
        event.subscribe(callback_id)
        triggered_callbacks = event.trigger()
    """

    __l_subscriptions: list[str]

    def __init__(self) -> None:
        """
        __init__ intializes the instance of Event

        Args:
            name (str): the name of the event
        """
        self.__l_subscriptions = []

    def subscribe(self, id: str) -> None:
        """
        Subscribe a callback to this event.

        Adds a callback ID to the subscription list for this event. The callback
        will be executed when the event is triggered, in order of priority.

        Args:
            id (str): The unique identifier of the callback to subscribe

        Raises:
            TypeError: If id is not a string
            ValueError: If id is empty or already subscribed
        """
        if not isinstance(id, str):
            raise TypeError(f'Callback id must be a string, got {type(id)}')
        if not id:
            raise ValueError('Callback id cannot be empty')
        if id in self.__l_subscriptions:
            raise ValueError(f'Callback {id} is already subscribed')

        self.__l_subscriptions.append(id)

    def unsubscribe(self, id: str) -> bool:
        """
        Remove a callback subscription from this event.

        Attempts to remove the specified callback ID from the subscription list.
        Returns True if the callback was found and removed, False if not found.

        Args:
            id (str): The unique identifier of the callback to unsubscribe

        Returns:
            bool: True if the callback was unsubscribed, False if not found

        Raises:
            TypeError: If id is not a string
            ValueError: If id is empty
        """
        if not isinstance(id, str):
            raise TypeError(f'Callback id must be a string, got {type(id)}')
        if not id:
            raise ValueError('Callback id cannot be empty')

        try:
            self.__l_subscriptions.remove(id)
            return True
        except ValueError:
            return False


    def trigger(self) -> list[str]:
        """
        Get a copy of all callback IDs subscribed to this event.

        Returns a defensive copy of the subscription list to prevent modification
        during iteration. The returned list can be safely used to execute
        callbacks in the correct order.

        Returns:
            list[str]: Immutable copy of subscribed callback IDs in registration order
        """
        return self.__l_subscriptions.copy()
