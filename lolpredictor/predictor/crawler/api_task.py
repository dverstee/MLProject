from abstract_task import Task
import logging
logger = logging.getLogger(__name__)


class ApiTask(Task):

    def execute(self):
        return self.api_method(*self.args)

    def process_result(self, result):
        self.callback(result)

    def process_failure(self):
        logger.error('Task failed')

    def __init__(self, retries, api_method, args, callback):
        super(ApiTask, self).__init__(retries)

        self.api_method = api_method
        self.callback = callback
        self.args = args