

from dataclasses import dataclass
from enum import Enum

#import asyncio
import hashlib

from fanning import Fan


class Speaker(Enum):
    CONGREGATION = "congregation"
    LEADER = "leader"
    SCRIPTURE = "scripture"
    HEADING = "heading"
    SUBHEADING = "subheading"


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
    title: str | None
    byline: str | None
    slides: list[Slide]

    def guess_title(self):
        if self.title:
            return self.title
        if self.slides:
            full = " ".join(stanza.text for stanza in self.slides[0].stanzas)
            return full[:30] + "..."
        return "(unknown)"


BLANK = Slide("99000000000000000000000000000001", [], "")


class Presentation:

    def __init__(self):
        self.sections = []
        self.current_slide = BLANK
        self.output_fan = Fan()

    def add_document(self, document: str) -> None:
        # What you see here is a phenomenally crude line-orientated parser which really
        # could and should be done better, but it evolved over time without a clear idea
        # of what the file format would actually look like!
        document = document + "\n\n===============\n\n"  # emit last slide/section!
        title, byline, slides_in_section = None, None, []
        speaker = Speaker.CONGREGATION
        stanzas_on_slide, emit_slide, emit_section = [], False, False
        for line in document.splitlines():
            line = line.rstrip()
            if line == "":
                emit_slide = True
            elif line.strip("=") == "" and len(line) > 5:
                emit_section = True
            elif line.startswith("%%title:"):
                title = line[8:].strip()
            elif line.startswith("%%byline:"):
                byline = line[9:].strip()
            elif line.startswith("[") and line.endswith("]"):
                speaker_name = line[1:-1].lower()
                speaker = {
                    "all": Speaker.CONGREGATION,
                    "ldr": Speaker.LEADER,
                    "scripture": Speaker.SCRIPTURE,
                    "heading": Speaker.HEADING,
                    "subheading": Speaker.SUBHEADING,
                }.get(speaker_name, Speaker.CONGREGATION)
            else:
                stanzas_on_slide.append(Stanza(speaker, line))
            if emit_slide:
                emit_slide = False
                if stanzas_on_slide:
                    #identifier = str(uuid.uuid4())  # autoreload gives a random id each time!
                    identifier = hashlib.md5(repr(stanzas_on_slide).encode()).hexdigest()
                    footer = f"{title or ''}\n{byline or ''}"
                    slides_in_section.append(Slide(identifier, stanzas_on_slide, footer))
                    stanzas_on_slide = []
            if emit_section:
                emit_section = False
                section = Section(title, byline, slides_in_section)
                self.sections.append(section)
                title, byline, slides_in_section = None, None, []

    def slide_list(self):
        # A list of all slides, ignoring the separation into sections
        return [slide for section in self.sections for slide in section.slides]

    def get_slide_by_identifier(self, identifier: str) -> Slide | None:
        # Return None if the slide shouldn't change
        if identifier == "@blank":
            return BLANK
        if identifier in ("@previous", "@next"):
            try:
                index = self.slide_list().index(self.current_slide)
            except ValueError:
                return None
            if identifier == "@previous":
                previous = index - 1
                return None if (previous < 0) else self.slide_list()[previous]
            else:
                nxt = index + 1
                return None if (nxt >= len(self.slide_list())) else self.slide_list()[nxt]
        for slide in self.slide_list():
            if slide.identifier == identifier:
                return slide
        raise KeyError(f"No slide with identifier {identifier!r}")

    async def activate(self, identifier: str):
        slide = self.get_slide_by_identifier(identifier)
        if slide is None:
            return
        self.current_slide = slide
        self.output_fan.publish(slide)
        return
