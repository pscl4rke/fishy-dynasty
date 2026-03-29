

from dataclasses import dataclass
from enum import Enum

#import asyncio
import hashlib

from fanning import Fan


class Speaker(Enum):
    CONGREGATION = "Congregation"


@dataclass
class Stanza:
    speaker: Speaker
    text: str


@dataclass
class Slide:
    identifier: str
    stanzas: list[Stanza]
    footer: str


@dataclass
class Section:
    title: str
    slides: list[Slide]


BLANK = Slide("99000000000000000000000000000001", [], "")


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
            stanzas = [Stanza(Speaker.CONGREGATION, slide_text)]
            section.slides.append(Slide(identifier, stanzas, title))
        self.sections.append(section)

    def slide_list(self):
        # A list of all slides, ignoring the separation into sections
        return [slide for section in self.sections for slide in section.slides]

    async def activate(self, identifier: str):
        for slide in self.slide_list():
            if slide.identifier == identifier:
                self.current_slide = slide
                self.output_fan.publish(slide)
                return
        raise KeyError(f"No slide with identifier {identifier!r}")
