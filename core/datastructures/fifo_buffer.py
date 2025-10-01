from collections import deque

class FIFOBuffer:
    def __init__(self, max_size=1000):
        self.buffer = deque(maxlen=max_size)

    def push(self, item):
        """Add a new item (oldest will be dropped if full)."""
        self.buffer.append(item)

    def pop(self):
        """Remove and return the oldest item."""
        if self.buffer:
            return self.buffer.popleft()
        return None

    def peek(self):
        """See the oldest item without removing it."""
        return self.buffer[0] if self.buffer else None

    def latest(self):
        """See the newest item."""
        return self.buffer[-1] if self.buffer else None

    def __len__(self):
        return len(self.buffer)

    def __iter__(self):
        return iter(self.buffer)
