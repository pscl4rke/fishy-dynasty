

from quart import Quart, render_template, redirect


APP = Quart(
    "webapp",
    template_folder="jinja",
)


@APP.route("/")
async def index():
    return redirect("/output/99/")


@APP.route("/output/<int:outputnumber>/")
async def output(outputnumber):
    return await render_template(
        "output.html",
        title=f"Output {outputnumber}",
    )


if __name__ == "__main__":
    APP.run()
