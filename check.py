from abc import ABC, abstractmethod
from enum import Enum

class CheckProvider(ABC):
    @abstractmethod
    def test(self, directory):
        pass

    @abstractmethod
    def checks(self):
        pass


class Check:
    def __init__(self, id, severity, reason, advice):
        self.id = id
        self.severity = severity
        self.reason = reason
        self.advice = advice


class CheckResult:
    def __init__(self, id, result):
        self.id = id
        self.result = result


class Severity(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 4


class Result(Enum):
    PASSED = 0
    FAILED = 1
    PRE_REQUISITE_CHECK_FAILED = 2
    NOT_APPLICABLE = 3
