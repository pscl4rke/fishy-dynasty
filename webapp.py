

import logging
LOG = logging.getLogger("fishy")

#import asyncio
from quart import Quart, request, abort, render_template, redirect
from sseing import ServerSentEvent, make_sse_response

import outputting
import presenting
from rendering import render_fragment


APP = Quart(
    "webapp",
    template_folder="jinja",
)
APP.config.from_prefixed_env()


import aguirre.integrations.quart as aguirre_quart
APP.register_blueprint(aguirre_quart.create_blueprint("pkgs"),
                       url_prefix="/pkgs")


PRESENTATION = presenting.Presentation()
import examples
PRESENTATION.load_from_parts(examples.NUNC_NAME, examples.NUNC_PARTS)
PRESENTATION.load_from_parts(examples.CREED_NAME, examples.CREED_PARTS)


@APP.route("/")
async def index():
    return redirect("/dashboard/")


@APP.route("/dashboard/")
async def dashboard():
    return await render_template(
        "dashboard.html",
        slides=PRESENTATION.slides,
        outputs=list(outputting.OUTPUTS),  # just the keys as numbers
    )


@APP.route("/activate/<identifier>/")
async def activate(identifier):
    await PRESENTATION.activate(identifier)
    return "Okay"


@APP.route("/output/<int:outputnumber>/")
async def output(outputnumber):
    output = outputting.OUTPUTS[outputnumber]
    return await render_template(
        "output.html",
        title=f"Output {outputnumber}",
        outputnumber=outputnumber,
        properties=output.properties,
    )


async def output_content_generator(outputnumber):
    with PRESENTATION.output_fan.subscribe() as slide_queue:
        html = await render_fragment("slide.html", slide=PRESENTATION.current_slide)
        yield ServerSentEvent(data=html).encode()
        while True:
            slide = await slide_queue.get()
            html = await render_fragment("slide.html", slide=slide)
            yield ServerSentEvent(data=html).encode()


@APP.route("/output/<int:outputnumber>/content/sse")
async def output_content_sse(outputnumber):
    if "text/event-stream" not in request.accept_mimetypes:
        abort(400)
    return await make_sse_response(output_content_generator(outputnumber))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    #APP.run(host="0.0.0.0")  # needed to allow obs browser to connect from other host
    APP.run()
