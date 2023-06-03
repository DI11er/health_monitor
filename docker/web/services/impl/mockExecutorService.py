import random


class MockExecutorService:
    def exec_ping(self, ip, port=None, count=1, timeout=5) -> bool:  
        return random.choice([True, False])