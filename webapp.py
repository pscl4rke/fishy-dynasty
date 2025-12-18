

from quart import Quart


APP = Quart("webapp")


@APP.route("/")
async def index():
    return "Hello World"


if __name__ == "__main__":
    APP.run()
