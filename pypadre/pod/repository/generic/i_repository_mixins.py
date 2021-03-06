from abc import ABCMeta, abstractmethod

from pypadre.core.util.inheritance import SuperStop


class IStoreableRepository:
    """ This is the interface for all backends being able to store objects onto some kind of persistence storage."""
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @abstractmethod
    def get(self, uid):
        raise NotImplementedError()

    @abstractmethod
    def get_by_hash(self, hash):
        raise NotImplementedError()

    def exists(self, uid):
        # TODO don't load object for better performance
        return self.get(uid) is not None

    def exists_object(self, obj):
        return self.exists(obj.id)

    @abstractmethod
    def put(self, obj, *args, merge=False, allow_overwrite=False, **kwargs):
        raise NotImplementedError()

    @abstractmethod
    def delete_by_id(self, uid):
        raise NotImplementedError()

    @abstractmethod
    def delete(self, obj):
        raise NotImplementedError()

    @abstractmethod
    def put_visualization(self, obj, *args, **kwargs):
        raise NotImplementedError()


class ISearchable:
    """ Interface for backends being searchable. Search on json data, folder name etc. for REST, local etc."""
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @abstractmethod
    def list(self, search: dict, offset=0, size=100) -> list:
        raise NotImplementedError()

    @staticmethod
    def filter(objs: list, search: dict):
        if search is None:
            return objs
        return [o for o in objs if ISearchable.in_search(o, search)]

    @staticmethod
    def in_search(obj, search: dict):
        # TODO Enable more sophisticated search
        return all([hasattr(obj, k) and getattr(obj, k) == v for k, v in search.items()])


class IProgressableRepository(SuperStop):
    """ This is the interface for all backends being able to progress the state of one of their
    currently running processes."""
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, **kwargs):
        super().__init__()

    @abstractmethod
    def put_progress(self, obj, **kwargs):
        raise NotImplementedError()


class ILogRepository(SuperStop):
    """ This is the interface for all backends which are able to log interactions into some kind of log store """
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @abstractmethod
    def log(self, msg):
        raise NotImplementedError()


class IHashProvidingRepository(SuperStop):
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @abstractmethod
    def get_hash(self):
        raise NotImplementedError()


class IRepository:
    """ This is the simple entry implementation of a backend. We define a hierarchical structure
    to the other backends here. """
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, *, backend, **kwargs):
        self._backend = backend
        super().__init__(**kwargs)

    @property
    def backend(self):
        return self._backend
