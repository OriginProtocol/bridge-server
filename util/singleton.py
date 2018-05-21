import threading


class Singleton():
    """
    Multi-thread safe singleton base class.
    Usage example:
      class Foo(Singleton):
         pass
      f = Foo.instance()
    """
    __lock = threading.Lock()
    __instance = None

    @classmethod
    def instance(cls, client=None):
        """
        Implement the singleton pattern.
        """
        if not cls.__instance:
            with cls.__lock:
                if not cls.__instance:
                    cls.__instance = cls(client=client)
        return cls.__instance
