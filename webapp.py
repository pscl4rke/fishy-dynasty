

import logging
LOG = logging.getLogger("fishy")

#import asyncio
from quart import Quart, request, abort, render_template, redirect
from sseing import ServerSentEvent, make_sse_response

import presenting


APP = Quart(
    "webapp",
    template_folder="jinja",
)


import aguirre.integrations.quart as aguirre_quart
APP.register_blueprint(aguirre_quart.create_blueprint("pkgs"),
                       url_prefix="/pkgs")


PRESENTATION = presenting.Presentation()
import examples
PRESENTATION.load_from_parts(examples.PARTS)


@APP.route("/")
async def index():
    return redirect("/dashboard/")


@APP.route("/dashboard/")
async def dashboard():
    return await render_template(
        "dashboard.html",
        slides=PRESENTATION.slides,
    )


@APP.route("/activate/<identifier>/")
async def activate(identifier):
    await PRESENTATION.activate(identifier)
    return "Okay"


@APP.route("/output/<int:outputnumber>/")
async def output(outputnumber):
    return await render_template(
        "output.html",
        title=f"Output {outputnumber}",
        outputnumber=outputnumber,
    )


async def output_content_generator(outputnumber):
    # FIXME when it first connects the current slide needs pushing to it
    with PRESENTATION.output_fan.subscribe() as slide_queue:
        while True:
            slide = await slide_queue.get()
            yield ServerSentEvent(data=slide.text).encode()


@APP.route("/output/<int:outputnumber>/content/sse")
async def output_content_sse(outputnumber):
    if "text/event-stream" not in request.accept_mimetypes:
        abort(400)
    return await make_sse_response(output_content_generator(outputnumber))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    APP.run()
