import random
from typing import Dict
import time
from collections import deque

class SlidingWindowRateLimiter:
    def __init__(self, window_size: int = 10, max_requests: int = 1):
        self.window_size = window_size
        self.max_requests = max_requests
        self.user_messages: Dict[str, deque] = {}

    def _cleanup_window(self, user_id: str, current_time: float) -> None:
        if user_id not in self.user_messages:
            return

        window = self.user_messages[user_id]

        while window and current_time - window[0] > self.window_size:
            window.popleft()

        if not window:
            del self.user_messages[user_id]

    def can_send_message(self, user_id: str) -> bool:
        current_time = time.time()
        self._cleanup_window(user_id, current_time)

        if user_id not in self.user_messages:
            return True

        return len(self.user_messages[user_id]) < self.max_requests

    def record_message(self, user_id: str) -> bool:
        current_time = time.time()
        allowed = self.can_send_message(user_id)

        if allowed:
            if user_id not in self.user_messages:
                self.user_messages[user_id] = deque()
            self.user_messages[user_id].append(current_time)
            return True
        else:
            return False

    def time_until_next_allowed(self, user_id: str) -> float:
        current_time = time.time()
        self._cleanup_window(user_id, current_time)

        if user_id not in self.user_messages:
            return 0.0

        window = self.user_messages[user_id]
        if len(window) < self.max_requests:
            return 0.0

        oldest_message_time = window[0]
        time_left = self.window_size - (current_time - oldest_message_time)
        return max(0.0, time_left)

def test_rate_limiter():
    limiter = SlidingWindowRateLimiter(window_size=10, max_requests=1)

    print("\n=== Massage flow simulation ===")
    for message_id in range(1, 11):
        user_id = message_id % 5 + 1
        result = limiter.record_message(str(user_id))
        wait_time = limiter.time_until_next_allowed(str(user_id))

        print(f"Massage {message_id:2d} | User {user_id} | "
              f"{'✓' if result else f'x (waiting {wait_time:.1f}sec)'}")

        time.sleep(random.uniform(0.1, 1.0))

    print("\nWairing 4 seconds...")
    time.sleep(4)

    print("\n=== New series of messages after waiting ===")
    for message_id in range(11, 21):
        user_id = message_id % 5 + 1
        result = limiter.record_message(str(user_id))
        wait_time = limiter.time_until_next_allowed(str(user_id))

        print(f"Message {message_id:2d} | User {user_id} | "
              f"{'✓' if result else f'x (waiting {wait_time:.1f}sec)'}")
        time.sleep(random.uniform(0.1, 1.0))

if __name__ == "__main__":
    test_rate_limiter()
