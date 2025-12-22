

from quart import Quart, render_template


APP = Quart(
    "webapp",
    template_folder="jinja",
)


@APP.route("/")
async def index():
    return await render_template(
        "output.html",
        title="Output 99",
    )


if __name__ == "__main__":
    APP.run()
