import hashlib
from abc import ABCMeta, abstractmethod


class IBaseContainer:
    __metaclass__ = ABCMeta

    def __init__(self, bin_format, data, attributes):
        self._format = bin_format
        self._attributes = attributes
        if hasattr(data, '__call__'):
            self._data_fn = data
        else:
            self._data = data

    def __hash__(self):
        return hashlib.md5(self._format)

    @abstractmethod
    def convert(self, bin_format):
        pass

    @abstractmethod
    def profile(self, bins=50, check_correlation=True, correlation_threshold=0.8, correlation_overrides=None,
                check_recoded=False):
        pass

    @abstractmethod
    def shape(self):
        pass

    @abstractmethod
    def describe(self):
        pass

    @abstractmethod
    def targets(self):
        pass

    @abstractmethod
    def features(self):
        pass

    @property
    def format(self):
        return self._format

    @property
    def data(self):
        if self._data is not None:
            return self._data
        elif self._data_fn is not None:
            self._data = self._data_fn()
            return self._data
        else:
            raise ValueError("Container %s holds no data." % str(self._format))

    @property
    def attributes(self):
        return self._attributes

    @abstractmethod
    def get_ontology(self):
        pass

    @abstractmethod
    def derive_attributes(self, **args):
        pass

    @abstractmethod
    def validate_attributes(self, **args):
        pass

