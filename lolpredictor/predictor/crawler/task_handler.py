from threading import Thread
from Queue import Queue
from abstract_task import Task
from lolpredictor.predictor.crawler.exceptions import RateLimitExceededError

class TaskHandler(Thread):

    def __init__(self, processing_interval):
        super(TaskHandler, self).__init__()
        self.queue = Queue()
        self.processing_interval = processing_interval
        self.is_running = True

    def enqueue_task(self, task):
        """
        Add a new task to the queue to be executed later
        :type task: Task
        """
        if not isinstance(task, Task):
            raise TypeError('argument of enqueue_task should be of class Task')

        self.queue.put(task)
        return self

    def handle_task(self, task):

        try:
            result = task.execute()
            task.process_result(result)

        except RateLimitExceededError:


        except:
            task.process_failure()
            task.retries_left -= 1
            if task.retries_left:
                self.enqueue_task(task)

    def run(self):
        while self.is_running:
            task = self.queue.get_nowait()
            if task:
                self.handle_task(task)


