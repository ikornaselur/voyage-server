"""
Borrowed as is from the takumi core.common.sqla module
"""
from sqlalchemy.ext.mutable import Mutable
from sqlalchemy_utils.types import UUIDType


class UUIDString(UUIDType):
    def process_result_value(self, value, dialect):
        if value is None:
            return value
        return str(value)


class MutableList(Mutable, list):
    def append(self, value):
        list.append(self, value)
        self.changed()

    def remove(self, value):
        list.remove(self, value)
        self.changed()

    @classmethod
    def coerce(cls, key, value):
        if not isinstance(value, MutableList):
            if isinstance(value, list):
                return MutableList(value)
            return Mutable.coerce(key, value)
        else:
            return value

    @classmethod
    def extends(cls, values):
        ret = cls()
        for value in values:
            cls.append(ret, value)

        return ret
