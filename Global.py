from abc import ABC, abstractmethod


class Global(ABC):
    def __int__(self, option_type, engine):
        self.option_type = option_type
        self.engine = engine
