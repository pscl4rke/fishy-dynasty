

# as per https://quart.palletsprojects.com/en/latest/how_to_guides/server_sent_events/


from dataclasses import dataclass
from typing import Iterator
from quart.typing import ResponseTypes


@dataclass
class ServerSentEvent:
    data: str
    event: str | None = None
    id: int | None = None
    retry: int | None = None

    def encode(self) -> bytes:
        message = f"data: {self.data}"
        if self.event is not None:
            message = f"{message}\nevent: {self.event}"
        if self.id is not None:
            message = f"{message}\nid: {self.id}"
        if self.retry is not None:
            message = f"{message}\nretry: {self.retry}"
        message = f"{message}\n\n"
        return message.encode('utf-8')


from quart import abort, make_response, request


#@app.get("/sse")
async def sse():
    if "text/event-stream" not in request.accept_mimetypes:
        abort(400)

    async def send_events():
        while True:
            data = ...  # Up to you where the events are from
            event = ServerSentEvent(data)
            yield event.encode()

    response = await make_response(
        send_events(),
        {
            'Content-Type': 'text/event-stream',
            'Cache-Control': 'no-cache',
            'Transfer-Encoding': 'chunked',
        },
    )
    response.timeout = None
    return response


async def make_sse_response(source: Iterator[ServerSentEvent]) -> ResponseTypes:
    response = await make_response(
        source,
        {
            'Content-Type': 'text/event-stream',
            'Cache-Control': 'no-cache',
            'Transfer-Encoding': 'chunked',
        },
    )
    response.timeout = None
    return response
