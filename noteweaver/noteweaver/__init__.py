from .logger import Logger
from logging import Logger as LoggingLogger
from .refine import RefineNote

class App:
    def __init__(self, refiner: RefineNote, logger: LoggingLogger):
        self._refiner = refiner
        self._logger = logger


__all__ = ["Logger", "RefineNote", "App"]
