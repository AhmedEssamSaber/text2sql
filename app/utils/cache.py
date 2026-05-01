import time


class SimpleCache:
    def __init__(self, ttl: int = 300):
        """
        ttl = time to live (seconds)
        """
        self.store = {}
        self.ttl = ttl

    def get(self, key: str):
        if key in self.store:
            value, timestamp = self.store[key]

            # check expiration
            if time.time() - timestamp < self.ttl:
                return value
            else:
                del self.store[key]

        return None

    def set(self, key: str, value):
        self.store[key] = (value, time.time())