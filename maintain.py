import json
import os
import urllib.request as requests

API_URL = 'http://localhost:7125/server/history/totals'
HOME_DIR = os.path.expanduser('~')

class Maintain:
    def __init__(self, config):
        self.config = config
        self.printer = config.get_printer()
        self.gcode = self.printer.lookup_object('gcode')

        # get name
        self.name = config.get_name().split()[1]

        # get config options
        self.label = config.get('label')

        self.trigger = config.getchoice('trigger', ['print_time', 'filament'])
        if self.trigger == 'print_time':
            self.units = 'h'
        elif self.trigger == 'filament':
            self.units = 'm'

        self.threshold = config.getint('threshold')
        self.message = config.get('message')

        self.init_db()

        # register GCode commands
        self.gcode.register_mux_command('CHECK_MAINTENANCE', 'NAME', self.name, self.cmd_CHECK_MAINTENANCE, desc=self.cmd_CHECK_MAINTENANCE_help)
        self.gcode.register_mux_command('UPDATE_MAINTENANCE', 'NAME', self.name, self.cmd_UPDATE_MAINTENANCE, desc=self.cmd_UPDATE_MAINTENANCE_help)
    
    def fetch_history(self):
        resp = requests.urlopen(API_URL) # fetch data from Moonraker History API
        try:
            json_data = json.loads(resp.read())
        except Exception:
            self.gcode.respond_info(f'Data {resp.read()}')
            return {
                'print_time': 0,
                'filament': 0
            }

        job_totals = json_data['result']['job_totals'] # get job totals from JSON response
        return {
            'print_time': job_totals['total_time']/3600,
            'filament': job_totals['total_filament_used']/1000,
        }

    def init_db(self):
        data = self.fetch_db()
        if data is None:
            data = self.fetch_history()
            self.update_db(data)

    def fetch_db(self):
        path = os.path.join(HOME_DIR, f'maintain-db/{self.name}')
        if os.path.exists(path):
            with open(path, 'r') as file:
                try:
                    data = json.load(file)
                except:
                    data = {'print_time': 0, 'filament': 0}
                return data
    
    def update_db(self, new):
        path = os.path.join(HOME_DIR, f'maintain-db/{self.name}')
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w+') as file:
            try:
                data = json.load(file)
            except:
                data = {'print_time': 0, 'filament': 0}
            data.update(new)
            json.dump(data, file)
        return data

    def get_remaining(self):
        last = self.fetch_db()[self.trigger]
        now = self.fetch_history()[self.trigger]
        return self.threshold - (now - last)

    cmd_CHECK_MAINTENANCE_help = 'Check maintenance'
    def cmd_CHECK_MAINTENANCE(self, gcmd):
        gcmd.respond_info(f'''
        Maintenance {self.label} Status:
        Next maintenance in {self.get_remaining()}{self.units}
        Maintenance message: {self.message}
        '''.strip())
    
    cmd_UPDATE_MAINTENANCE_help = 'Update maintenance'
    def cmd_UPDATE_MAINTENANCE(self, gcmd):
        self.update_db(self.fetch_history())

def load_config_prefix(config):
    return Maintain(config)