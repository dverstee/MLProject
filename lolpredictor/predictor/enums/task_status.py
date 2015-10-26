from enum import Enum


class TaskStatus(Enum):
    PENDING = 0
    ACTIVE = 1
    FINISHED = 2
    FAILED = 3
