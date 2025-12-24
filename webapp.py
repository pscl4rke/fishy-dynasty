

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


@APP.route("/")
async def index():
    return redirect("/dashboard/")


@APP.route("/dashboard/")
async def dashboard():
    return await render_template("dashboard.html")


@APP.route("/activate/<slidename>/")
async def activate(slidename):
    await PRESENTATION.activate(slidename)
    return "Okay"


@APP.route("/output/<int:outputnumber>/")
async def output(outputnumber):
    return await render_template(
        "output.html",
        title=f"Output {outputnumber}",
        outputnumber=outputnumber,
    )


@APP.route("/output/<int:outputnumber>/content/poll")
async def output_content_poll(outputnumber):
    import datetime
    return f"New thing {datetime.datetime.now().isoformat()}"


async def output_content_generator(outputnumber):
    async for data in PRESENTATION.output(outputnumber):
        yield ServerSentEvent(data=data).encode()


@APP.route("/output/<int:outputnumber>/content/sse")
async def output_content_sse(outputnumber):
    if "text/event-stream" not in request.accept_mimetypes:
        abort(400)
    return await make_sse_response(output_content_generator(outputnumber))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    APP.run()
