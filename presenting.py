

from dataclasses import dataclass
#import asyncio

from fanning import Fan


@dataclass
class Slide:
    name: str
    text: str


class Presentation:

    def __init__(self):
        self.slides = {}
        #self.currently_showing = "initial"
        self.output_fan = Fan()

    def load_from_parts(self, parts: list[str]):
        for i, slide_text in enumerate(parts):
            slide_name = "slide%03i" % (i + 1)
            self.slides[slide_name] = Slide(slide_name, slide_text)

    async def activate(self, slidename: str):
        #self.currently_showing = slidename
        self.output_fan.publish(self.slides[slidename])
