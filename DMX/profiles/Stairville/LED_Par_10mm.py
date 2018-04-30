from DMX.profiles.defaults import Fixture


class LED_Par_10mm(Fixture):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._register_channel('red')
        self._register_channel_aliases('red', 'r')
        self._register_channel('green')
        self._register_channel_aliases('green', 'g')
        self._register_channel('blue')
        self._register_channel_aliases('blue', 'b')
        self._register_channel('macro')
        self._register_channel('speed/strobe')
        self._register_channel('mode')
        self._register_channel('dimmer')
        self._register_channel_aliases('dimmer', 'dim', 'd')
