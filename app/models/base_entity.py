from datetime import datetime
from sqlalchemy.sql import func

from app import db


class BaseEntity:
    createdate = db.Column(db.DateTime, default=func.now(), nullable=True)
    updatedate = db.Column(db.DateTime, default=None, onupdate=func.now())
    deletedate = db.Column(db.DateTime)
    __active = db.Column(db.Boolean, name="active", default=True, nullable=False)

    @property
    def active(self):
        return self.__active

    @active.setter
    def active(self, value):
        if not value:
            self.deletedate = datetime.now()

        self.__active = value