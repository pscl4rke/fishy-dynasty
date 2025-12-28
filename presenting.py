

from dataclasses import dataclass
#import asyncio
import hashlib

from fanning import Fan


@dataclass
class Slide:
    identifier: str
    text: str
    footer: str


BLANK = Slide("99000000000000000000000000000001", "", "")


class Presentation:

    def __init__(self):
        self.slides = []
        self.current_slide = BLANK
        self.output_fan = Fan()

    def load_from_parts(self, parts: list[str]):
        for i, slide_text in enumerate(parts):
            #identifier = str(uuid.uuid4())  # autoreload gives a random id each time!
            identifier = hashlib.md5(slide_text.encode()).hexdigest()
            slide_footer = "I am a footer"
            self.slides.append(Slide(identifier, slide_text, slide_footer))

    async def activate(self, identifier: str):
        for slide in self.slides:
            if slide.identifier == identifier:
                self.current_slide = slide
                self.output_fan.publish(slide)
                return
        raise KeyError(f"No slide with identifier {identifier!r}")
