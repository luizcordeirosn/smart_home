from abc import ABC, abstractmethod


class Singleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance


class Observer(ABC):
    @abstractmethod
    def update(self, **kwargs):
        pass


class Subject(ABC):
    def __init__(self):
        self.__observers = []

    @property
    def observers(self):
        return self.__observers

    def add_observer(self, observer):
        self.observers.append(observer)

    def remove_observer(self, observer):
        self.observers.remove(observer)

    def notify(self, **kwargs):
        for obs in self.observers:
            obs.update(**kwargs)
