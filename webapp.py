

from quart import Quart, render_template, redirect


APP = Quart(
    "webapp",
    template_folder="jinja",
)


import aguirre.integrations.quart as aguirre_quart
APP.register_blueprint(aguirre_quart.create_blueprint("pkgs"),
                       url_prefix="/pkgs")


@APP.route("/")
async def index():
    return redirect("/output/99/")


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


if __name__ == "__main__":
    APP.run()
