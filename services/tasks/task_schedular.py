import os
import json
import asyncio
import tempfile
from typing import Any


class PersistentQueue:
    def __init__(self, file_path: str = "tasks.log"):
        self.file_path = file_path
        self.queue: list[Any] = []
        self._load_from_disk()


    def _load_from_disk(self):
        """Load tasks from disk, skipping corrupted or empty lines."""
        if not os.path.exists(self.file_path):
            return


        with open(self.file_path, "r", encoding="utf-8") as f:
            for i, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue  # skip empty lines
                try:
                    task = json.loads(line)
                    self.queue.append(task)
                except json.JSONDecodeError:
                    print(f"⚠️ Skipping corrupted line {i} in {self.file_path!r}: {line!r}")


    def _append_to_disk(self, task: Any):
        """Safely append a single task to the log file."""
        line = json.dumps(task, ensure_ascii=False)
        with open(self.file_path, "a", encoding="utf-8") as f:
            f.write(line + "\n")
            f.flush()                      # flush OS buffer
            os.fsync(f.fileno())


    def _rewrite_disk(self):
        """Rewrite the queue file atomically to prevent corruption."""
        dir_name = os.path.dirname(self.file_path) or "."
        temp_fd, temp_path = tempfile.mkstemp(dir=dir_name, prefix="queue_", suffix=".tmp")
        try:
            with os.fdopen(temp_fd, "w", encoding="utf-8") as tmp_file:
                for task in self.queue:
                    json.dump(task, tmp_file, ensure_ascii=False)
                    tmp_file.write("\n")
                tmp_file.flush()
                os.fsync(tmp_file.fileno())

            # Atomic rename replaces old file instantly and safely
            os.replace(temp_path, self.file_path)
        finally:
            # Clean up temp file if something went wrong
            if os.path.exists(temp_path):
                os.remove(temp_path)


    def enqueue(self, task: Any):
        self.queue.append(task)
        self._append_to_disk(task)


    def dequeue(self):
        if not self.queue:
            return None
        task = self.queue.pop(0)
        self._rewrite_disk()
        return task


    def size(self) -> int:
        """Return number of tasks currently in memory."""
        return len(self.queue)


class AsyncPersistentQueue(PersistentQueue):
    def __init__(self, file_path="tasks.log"):
        super().__init__(file_path)
        self.lock = asyncio.Lock()


    async def enqueue(self, task):
        async with self.lock:
            super().enqueue(task)


    async def dequeue(self):
        async with self.lock:
            return super().dequeue()


    async def size(self) -> int:
        """Async wrapper around size check."""
        async with self.lock:
            return super().size()

