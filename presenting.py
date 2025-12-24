

import asyncio


class Presentation:

    def __init__(self):
        self.currently_showing = "initial"

    async def activate(self, slidename: str):
        self.currently_showing = slidename

    async def output(self, outputnumber: int):
        import datetime
        i = 0
        while True:
            i = i + 1
            yield f"Showing {self.currently_showing} as of {datetime.datetime.now().isoformat()}"
            await asyncio.sleep(1)
