

from dataclasses import dataclass
from enum import Enum

#import asyncio
import hashlib

from fanning import Fan


class Speaker(Enum):
    CONGREGATION = "congregation"
    LEADER = "leader"


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

    def add_section(self, title: str, document: str) -> None:
        document = document + "\n\n"  # emit last slide!
        section = Section(title, [])
        speaker = Speaker.CONGREGATION
        stanzas_on_slide, emit_slide = [], False
        for line in document.splitlines():
            line = line.rstrip()
            if line == "":
                emit_slide = True
            elif line.startswith("[") and line.endswith("]"):
                speaker_name = line[1:-1].lower()
                speaker = {
                    "all": Speaker.CONGREGATION,
                    "ldr": Speaker.LEADER,
                }.get(speaker_name, Speaker.CONGREGATION)
            else:
                stanzas_on_slide.append(Stanza(speaker, line))
            if emit_slide and stanzas_on_slide:
                #identifier = str(uuid.uuid4())  # autoreload gives a random id each time!
                identifier = hashlib.md5(repr(stanzas_on_slide).encode()).hexdigest()
                section.slides.append(Slide(identifier, stanzas_on_slide, title))
                stanzas_on_slide, emit_slide = [], False
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
