class Maintain:
    def __init__(self, config):
        self.server = config.get_server()
        self.name = config.get_name()

        _ = config.get('label', default='', deprecate=True)

        self.trigger = config.getchoice(
            option='trigger',
            choices=[
                'print_time',
                'filament',
                'time'
            ]
        )
        self.threshold = config.getint('threshold')
        self.message = config.get('message')

    async def test_gcode(self):
        klippy_apis = self.server.lookup_component('klippy_apis')
        result = await klippy_apis.run_gcode('M117 hello!')
        return f'hi{result}'
