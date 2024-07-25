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

        # TODO: register GCode commands
        self.gcode.register_mux_command('CHECK_MAINTENANCE', 'LABEL', self.label, self.cmd_CHECK_MAINTENANCE, desc=self.cmd_CHECK_MAINTENANCE_help)
    
    def get_remaining(self):
        return self.threshold

    cmd_CHECK_MAINTENANCE_help = 'Check maintenance'
    def cmd_CHECK_MAINTENANCE(self, gcmd):
        gcmd.respond_info(f'''
        Maintenance {self.label} Status:
        Next maintenance in {self.get_remaining()}{self.units}
        Maintenance message: {self.message}
        '''.strip())