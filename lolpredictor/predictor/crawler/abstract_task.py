from abc import abstractmethod, abstractproperty, ABCMeta
from lolpredictor.predictor.config import config


class Task(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, retries=config.NR_OF_API_RETRIES):
        self.retries_left = retries

    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def process_failure(self):
        pass

    @abstractmethod
    def process_result(self):
        pass
