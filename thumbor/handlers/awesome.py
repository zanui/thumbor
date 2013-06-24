import re

from tornado import gen
import tornado.web

from thumbor.handlers import ContextHandler


PARTS_REGEX = re.compile(r'(\w+):(.+?)(?=/\w+:|$)')

PLUGINS = [
    'img',
    'rs'
]


class ThumborPlugin(object):

    def __init__(self, context):
        self.context = context


class LoaderPlugin(ThumborPlugin):

    @gen.engine
    def run(self, params, callback):
        img_buffer = yield gen.Task(self.context.modules.loader.load, self.context, params)
        engine = self.context.modules.engine
        engine.load(img_buffer, '.jpg')
        callback()


class ResizePlugin(ThumborPlugin):

    def run(self, params, callback):
        engine = self.context.modules.engine
        source_width, source_height = engine.size
        target_width, target_height = params.split('x')

        if target_width == source_width and target_height == source_height:
            return
        engine.resize(target_width, target_height)
        callback()


MAPPED_PLUGINS = {
    'rs': ResizePlugin,
    'img': LoaderPlugin
}


class AwesomeHandler(ContextHandler):

    @tornado.web.asynchronous
    @gen.coroutine
    def get(self, unparsed_path):
        parts = PARTS_REGEX.findall(unparsed_path)
        parts_map = {part[0]: part[1] for part in parts}

        for plugin_name in PLUGINS:
            plugin_param = parts_map[plugin_name]
            if not plugin_param:
                continue
            plugin_class = MAPPED_PLUGINS.get(plugin_name, None)
            if not plugin_class:
                continue
            plugin_instance = plugin_class(self.context)
            yield gen.Task(plugin_instance.run, plugin_param)

        results = self.context.modules.engine.read('.jpg', 80)
        self.set_header('Content-Type', 'image/jpeg')
        self.write(results)
        self.finish()
