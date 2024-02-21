from abc import ABC, abstractmethod
from enum import Enum
from typing import Optional


class SQLAction(Enum):
    ADD = 1
    REMOVE = 2


class SQLResult(ABC):
    def __init__(self, action: SQLAction, success: bool, err_message: Optional[str] = None):
        self.action = action
        self.succeed = success
        self.err_message = err_message

    @staticmethod
    @abstractmethod
    def success():
        pass

    @staticmethod
    @abstractmethod
    def error(message):
        pass


class AdditionResult(SQLResult):
    @staticmethod
    def success():
        return AdditionResult(SQLAction.ADD, True)

    @staticmethod
    def error(message):
        return AdditionResult(SQLAction.ADD, False, message)


class RemovingResult(SQLResult):
    @staticmethod
    def success():
        return RemovingResult(SQLAction.REMOVE, True)

    @staticmethod
    def error(message):
        return RemovingResult(SQLAction.REMOVE, False, message)
