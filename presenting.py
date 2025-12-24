

import asyncio


class Presentation:

    async def output(self, outputnumber: int):
        import datetime
        i = 0
        while True:
            i = i + 1
            yield f"New thing {datetime.datetime.now().isoformat()}"
            await asyncio.sleep(1)
