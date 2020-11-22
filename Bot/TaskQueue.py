import logging

from collections import deque

from parser import TaskListPage

logger = logging.getLogger(__name__)


class TaskQueue:
    def __init__(self):
        self.cursor = TaskListPage()
        self.queue = deque(self.cursor.get_last_10_tasks())

    def update(self):
        articles = self.cursor.get_last_10_tasks()
        shift = 0
        for i in range(len(articles)):
            if self.queue[0] == articles[i]:
                break
            shift += 1

        if not shift:
            return None

        new_tasks = articles[:shift]
        for i in range(shift):
            self.queue.pop()
        for i in range(shift):
            self.queue.appendleft(new_tasks[shift-i-1])

        logger.info('len queue = ', len(self.queue))
        return new_tasks
