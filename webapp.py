

import logging
LOG = logging.getLogger("fishy")

import argparse

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


@APP.route("/")
async def index():
    return redirect("/dashboard/")


@APP.route("/dashboard/")
async def dashboard():
    return await render_template(
        "dashboard.html",
        sections=PRESENTATION.sections,
        outputs=list(outputting.OUTPUTS),  # just the keys as numbers
    )


@APP.route("/doc/append/", methods=["POST"])
async def doc_append():
    #LOG.info(request)
    #LOG.info(dir(request))
    #LOG.info(repr(request.body))
    #LOG.info(dir(request.body))
    #LOG.info(await request.get_data())
    #LOG.info(await request.form)  # filename ends up here if <form enctype=...> not set
    #LOG.info(await request.files)
    file = (await request.files)["file"]
    #LOG.info(file)
    #LOG.info(dir(file))
    #LOG.info(file.stream)
    #LOG.info(dir(file.stream))
    content = file.stream.read().decode("utf8")
    #LOG.info(content)
    if content != "":
        PRESENTATION.add_document(content)
    return redirect("/dashboard/")


@APP.route("/activate/<identifier>/")
async def activate(identifier):
    await PRESENTATION.activate(identifier)
    return "Okay"


async def status_generator():
    with PRESENTATION.output_fan.subscribe() as slide_queue:
        html = await render_fragment("status.html", slide=PRESENTATION.current_slide)
        yield ServerSentEvent(data=html).encode()
        while True:
            slide = await slide_queue.get()
            html = await render_fragment("status.html", slide=slide)
            yield ServerSentEvent(data=html).encode()


@APP.route("/status/sse")
async def status_sse():
    return await make_sse_response(status_generator())


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
    # Hmm... how very interesting.  HTMX 4.0.0-alpha8 sends "text/html"
    # for this.  I wonder if they'll fix that?
    #if "text/event-stream" not in request.accept_mimetypes:
    #    abort(400)
    return await make_sse_response(output_content_generator(outputnumber))


def argument_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("documents", nargs="*")
    return parser


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    args = argument_parser().parse_args()
    for filename in args.documents:
        with open(filename) as document_file:
            PRESENTATION.add_document(document_file.read())
    #APP.run(host="0.0.0.0")  # needed to allow obs browser to connect from other host
    APP.run()
