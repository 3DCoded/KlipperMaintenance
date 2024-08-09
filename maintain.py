from pathlib import Path

CONFIG_DIR = Path.home() / 'printer_data' / 'config'


class ConfigError(Exception):
    pass


class Maintain:
    def __init__(self, config):
        self.server = config.get_server()
        self.name = config.get_name()

        self.config_path = CONFIG_DIR / \
            config.get('config_path', 'maintain.conf')

        self.items = []

        self.server.register_endpoint(
            '/server/maintain/settings', ['GET'], self.maintain_settings)

    async def run_gcode(self, gcode):
        klippy_apis = self.server.lookup_component('klippy_apis')
        for line in gcode:
            await klippy_apis.run_gcode(line)

    async def maintain_settings(self, request):
        result = []
        for item in self.items:
            result.append({
                'name': item.name,
                'trigger': item.trigger,
                'threshold': item.threshold,
                'message': item.message
            })
        return result


class MaintainItem:
    def __init__(self, config, section):
        self.trigger = config.get(section, 'trigger', fallback='print_time')
        if self.trigger not in ['print_time', 'filament', 'time']:
            raise ConfigError('Invalid trigger type')
        self.threshold = config.getint(section, 'threshold')
        if self.threshold <= 0:
            raise ConfigError('Invalid threshold')
        self.message = config.get(section, 'message', fallback='No message')


def load_component(config):
    return Maintain(config)
