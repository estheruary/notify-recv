import click

from notify_recv.monitor import NotifyMonitor
from notify_recv.formatters import FormatPlugins

class CLI(object):

    def __init__(self):
        self.format_plugins = FormatPlugins()

    def run(self, format):
        self.plugin = self.format_plugins.get_plugin(format)
        self.monitor = NotifyMonitor(self.plugin)
        self.monitor.start()

    @staticmethod
    @click.command(context_settings={'help_option_names': ['-h', '--help']})
    @click.option('-f', '--format', default='plain',
            help='How to format the output. See docs for information about format plugins.')
    def start(format):
        cli = CLI()
        cli.run(format)
