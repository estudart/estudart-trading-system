from abc import ABC, abstractmethod


class DataConsumer(ABC):
    @abstractmethod
    def consume_data(self, data: dict):
        pass

    @abstractmethod
    def run(self):
        pass