from abc import ABC, abstractmethod


class BaseDTO(ABC):
    @abstractmethod
    def serialize(self):
        pass