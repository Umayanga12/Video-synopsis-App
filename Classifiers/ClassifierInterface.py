from abc import ABC, abstractmethod


class ClassifierInterface(ABC):
    @abstractmethod
    def tagLayer(self, layers):
        pass
