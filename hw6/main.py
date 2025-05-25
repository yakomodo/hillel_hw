import time
import logging

class TimerContext:
    def enter(self):
        self.start = time.time()
        return self


    def exit(self, exc_type, exc_val, exc_tb):
        elapsed = time.time() - self.start
        logging.info(f"Elapsed: {elapsed:.2f} seconds")


    logging.basicConfig(level=logging.INFO)

with TimerContext():
    sum([i for i in range(10000000)])