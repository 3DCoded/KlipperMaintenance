import json
import os
import time
import urllib.request as requests

API_URL = 'http://localhost:7125/server/history/totals'
HOME_DIR = os.path.expanduser('~')

class Maintenance:
    def __init__(self, config):
        self.config = config
        self.printer = config.get_printer()
        self.reactor = self.printer.get_reactor()
        self.gcode = self.printer.lookup_object('gcode')
        
        self.interval = config.getint('interval', 60)

        self.gcode.register_command('MAINTAIN_STATUS', self.cmd_MAINTAIN_STATUS, desc=self.cmd_MAINTAIN_STATUS_help)

        if self.interval > 0:
            self.timer_handler = None
            self.inside_timer = self.repeat = False
            self.printer.register_event_handler("klippy:ready", self._handle_ready)

    def _handle_ready(self):
        waketime = self.reactor.monotonic() + self.interval
        self.timer_handler = self.reactor.register_timer(
            self._gcode_timer_event, waketime)
        
    def _gcode_timer_event(self, eventtime):
        self.inside_timer = True
        self.check_maintenance()
        nextwake = eventtime + self.interval
        self.inside_timer = self.repeat = False
        return nextwake

    def check_maintenance(self):
        objs = self.printer.lookup_objects('maintain')
        for obj in objs:
            obj = obj[1]
            if not isinstance(obj, Maintain):
                continue
            if obj.get_remaining() < 0:
                obj.expired_func()
    
    cmd_MAINTAIN_STATUS_help = 'Check status of maintenance'
    def cmd_MAINTAIN_STATUS(self, gcmd):
        objs = self.printer.lookup_objects('maintain')
        for obj in objs:
            obj = obj[1]
            if not isinstance(obj, Maintain):
                continue
            remain = obj.get_remaining()
            if remain < 0:
                self.gcode.respond_info(f'Maintenance "{obj.label}" Expired!\n{obj.message}')
            self.gcode.respond_info(f'{obj.label}: {obj.get_remaining()}{obj.units} remaining')

class Maintain:
    def __init__(self, config):
        self.config = config
        self.printer = config.get_printer()
        self.gcode = self.printer.lookup_object('gcode')

        # get name
        self.name = config.get_name().split()[1]

        # get config options
        self.label = config.get('label', default='')

        self.trigger = config.getchoice('trigger', ['print_time', 'filament', 'time'])
        if self.trigger == 'print_time':
            self.units = 'h'
        elif self.trigger == 'filament':
            self.units = 'm'
        elif self.trigger == 'time':
            self.units = 'h'

        self.threshold = config.getfloat('threshold')
        self.message = config.get('message', default='')

        gcode_macro = self.printer.load_object(config, 'gcode_macro')
        if config.get('expired_gcode', None) is not None:
            self.expired_gcode = gcode_macro.load_template(config, 'expired_gcode', '')
            self.expired_func = lambda: self.gcode.run_script(self.expired_gcode.render())
        else:
            self.expired_func = self.default_expired_func

        self.init_db()

        # register GCode commands
        self.gcode.register_mux_command('CHECK_MAINTENANCE', 'NAME', self.name, self.cmd_CHECK_MAINTENANCE, desc=self.cmd_CHECK_MAINTENANCE_help)
        self.gcode.register_mux_command('UPDATE_MAINTENANCE', 'NAME', self.name, self.cmd_UPDATE_MAINTENANCE, desc=self.cmd_UPDATE_MAINTENANCE_help)
    
    def default_expired_func(self):
        self.gcode.respond_info(f'Maintenance Expired!\nMaintenance "{self.name}" expired!\n{self.message}')

    def fetch_history(self):
        resp = requests.urlopen(API_URL) # fetch data from Moonraker History API
        try:
            json_data = json.loads(resp.read())
        except Exception:
            self.gcode.respond_info(f'Data {resp.read()}')
            return {
                'print_time': 0,
                'filament': 0,
                'time': time.time()/3600
            }

        job_totals = json_data['result']['job_totals'] # get job totals from JSON response
        return {
            'print_time': job_totals['total_time']/3600,
            'filament': job_totals['total_filament_used']/1000,
            'time': time.time()/3600
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
                    data = {'print_time': 0, 'filament': 0, 'time': time.time()/3600}
                return data
    
    def update_db(self, new):
        path = os.path.join(HOME_DIR, f'maintain-db/{self.name}')
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w+') as file:
            try:
                data = json.load(file)
            except:
                data = {'print_time': 0, 'filament': 0, 'time': time.time()/3600}
            data.update(new)
            json.dump(data, file)
        return data

    def get_remaining(self):
        last = self.fetch_db()[self.trigger]
        now = self.fetch_history()[self.trigger]
        return round(self.threshold - (now - last), 2)

    cmd_CHECK_MAINTENANCE_help = 'Check maintenance'
    def cmd_CHECK_MAINTENANCE(self, gcmd):
        gcmd.respond_info(f'''
Maintenance {self.label} Status:
Next maintenance in {self.get_remaining()}{self.units}
Maintenance message: {self.message}
        '''.strip())
    
    cmd_UPDATE_MAINTENANCE_help = 'Update maintenance'
    def cmd_UPDATE_MAINTENANCE(self, gcmd):
        data = self.fetch_history()

        hours = gcmd.get_int('HOURS', -1)
        if hours > -1 and hours < self.threshold:
            new = self.fetch_history()[self.trigger] - hours
            data[self.trigger] = new

        self.update_db(data)

def load_config(config):
    return Maintenance(config)

def load_config_prefix(config):
    return Maintain(config)