

# I can't use quart.render_template
# because I get the error
# RuntimeError: Not within an app context
# if I use it within an SSE coroutine.


async def render_fragment(template_path, **ctx):
    #from quart.globals import _cv_app
    #print(_cv_app)
    #print(_cv_app.get("i-am-unset"))
    from webapp import APP as current_app
    template = current_app.jinja_env.get_or_select_template(template_path)
    from quart.templating import _render
    return await _render(template, ctx, current_app)
    #return "FIXME"
