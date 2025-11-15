# cm_timer.py

import time
from contextlib import contextmanager


class cm_timer_1:
    """
    基于类的上下文管理器
    """
    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        end = time.time()
        print(f"time: {end - self.start:.3f}")


@contextmanager
def cm_timer_2():
    """
    基于 contextlib 的上下文管理器
    """
    start = time.time()
    try:
        yield
    finally:
        end = time.time()
        print(f"time: {end - start:.3f}")


if __name__ == '__main__':
    from time import sleep

    with cm_timer_1():
        sleep(1.5)

    with cm_timer_2():
        sleep(1.0)
