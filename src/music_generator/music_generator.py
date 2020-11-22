from abc import ABC, abstractmethod


class MusicGenerator(ABC):
    @abstractmethod
    def generate(self, notes_amount: int, file_name: str):
        raise NotImplementedError()
