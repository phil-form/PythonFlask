from abc import ABC, abstractmethod


class AbstractDTO(ABC):
    @abstractmethod
    def serialize(self):
        pass