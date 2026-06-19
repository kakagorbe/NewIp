import asyncio

class Backpressure:
    def __init__(self, queue, threshold):
        self.queue = queue
        self.threshold = threshold

    async def wait(self):
        if self.queue.qsize() > self.queue.maxsize * self.threshold:
            await asyncio.sleep(0.01)
