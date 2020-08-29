from abc import ABC, abstractmethod


class TaskQueue(ABC):
    @abstractmethod
    def push(self, value):
        pass

    @abstractmethod
    def pop(self):
        pass
