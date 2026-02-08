from abc import ABC, abstractmethod
from dataclasses import dataclass


class Reconnector(ABC):
    @abstractmethod
    def get_interval(self, attempt: int | None=None) -> int:
        """Return interval in seconds"""
        pass

@dataclass
class FixedDelay(Reconnector):
    interval: int
    
    def get_interval(self, attempt: int | None = None) -> int:
        return self.interval
    
@dataclass
class LinearBackoff(Reconnector):
    base_interval: int
    max_interval: int
    
    def get_interval(self, attempt: int | None = None) -> int:
        assert attempt is not None, "attempt can't be None"
        interval = attempt * self.base_interval
        return min([self.max_interval, interval])

@dataclass
class ExponentialBackoff(Reconnector):
    base_interval: int
    max_interval: int
    
    def get_interval(self, attempt: int | None = None) -> int:
        assert attempt is not None, "attempt can't be None"
        interval = self.base_interval ** attempt
        return min([self.max_interval, interval])