class IoCContainer:
    """
    A simple Inversion of Control (IoC) container to manage service dependencies.
    """

    def __init__(self):
        """
        Initialize the IoC container with an empty dictionary to store services.
        """
        self._services = {}

    def register(self, name, service):
        """
        Register a service with a given name in the IoC container.

        Args:
            name (str): The name to register the service under.
            service (object): The service instance to be registered.
        """
        self._services[name] = service

    def config(self, name):
        """
        Retrieve a service by name from the IoC container.

        Args:
            name (str): The name of the service to retrieve.

        Returns:
            object: The service instance registered under the given name.

        Raises:
            ValueError: If the service with the given name is not found.
        """
        service = self._services.get(name)
        if not service:
            raise ValueError(f"Service '{name}' not found")
        return service