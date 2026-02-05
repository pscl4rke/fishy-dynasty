

from dataclasses import dataclass
#import asyncio
import hashlib

from fanning import Fan


@dataclass
class Slide:
    identifier: str
    text: str
    footer: str


@dataclass
class Section:
    title: str
    slides: list[Slide]


BLANK = Slide("99000000000000000000000000000001", "", "")


class Presentation:

    def __init__(self):
        self.sections = []
        self.current_slide = BLANK
        self.output_fan = Fan()

    def add_section(self, title, parts: list[str]):
        section = Section(title, [])
        for i, slide_text in enumerate(parts):
            #identifier = str(uuid.uuid4())  # autoreload gives a random id each time!
            identifier = hashlib.md5(slide_text.encode()).hexdigest()
            section.slides.append(Slide(identifier, slide_text, title))
        self.sections.append(section)

    async def activate(self, identifier: str):
        for section in self.sections:
            for slide in section.slides:
                if slide.identifier == identifier:
                    self.current_slide = slide
                    self.output_fan.publish(slide)
                    return
        raise KeyError(f"No slide with identifier {identifier!r}")
