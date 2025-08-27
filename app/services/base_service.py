from abc import ABC, abstractmethod

from app.forms.users.user_register_form import UserRegisterForm


class BaseService(ABC):
    @abstractmethod
    def find_all(self):
        pass

    @abstractmethod
    def find_one(self, id):
        pass

    @abstractmethod
    def insert(self, form):
        pass

    @abstractmethod
    def update(self, id, form):
        pass

    @abstractmethod
    def delete(self, id):
        pass