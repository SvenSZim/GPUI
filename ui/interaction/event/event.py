
class Event:
    """
    Event is a container class for Callbacks.
    It is used to create and store events which can be
    triggered or subscribed to.
    When triggered it calls all stored Callables (callbacks).
    """
    
    __l_subscriptions: list[str] # list of the id's of the callbacks to call when triggered

    def __init__(self, name: str) -> None:
        """
        __init__ intializes the instance of Event

        Args:
            name (str): the name of the event
        """
        self.__name = name
        self.__l_subscriptions = []

    def subscribe(self, callback: str) -> None:
        """
        subscribe takes a callback, that should
        be called when the event is triggered. 

        Args:
            callback (str): the callback that should be subscribed to the event
        """
        self.__l_subscriptions.append(callback)

    def unsubscribe(self, id: str) -> bool:
        """
        unsubscribe unsubscribes a callback (by id) from the event.

        Args:
            id (str): the id of the callback to unsubscribe

        Returns (bool): if the unsubscription was successful
        """
        for callback in self.__l_subscriptions:
            if callback == id:
                self.__l_subscriptions.remove(callback)
                return True
        return False


    def trigger(self) -> list[str]:
        """
        trigger returns a list of all callbacks to be triggered when the event
        is called.

        Returns (list[str]): list of the id's of the callbacks to call
        """
        return self.__l_subscriptions.copy()
