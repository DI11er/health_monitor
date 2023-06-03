import config

from services.impl.pingExecutorService import PingExecutorService
from services.impl.mockExecutorService import MockExecutorService


class ExecutorService:

    @classmethod
    def get_instance(cls, *args, **kwargs):
        if config.IMPL == 'PingExecutorService':
            return PingExecutorService()
        if config.IMPL == 'MockExecutorService':
            return MockExecutorService()


