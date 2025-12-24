

#import asyncio

from fanning import Fan


class Presentation:

    def __init__(self):
        self.currently_showing = "initial"
        self.output_fan = Fan()

    async def activate(self, slidename: str):
        self.currently_showing = slidename
        self.output_fan.publish(slidename)
