"""
 *  Profile for Blizzard Pixellicious LED Matrix
 *  Product page: https://www.blizzardpro.com/products/pixellicious
 *  Information based on Pixellicious User Manual Rev. B
"""

from ..defaults import Fixture, Vdim


class Pixellicious_8Ch(Vdim):

    def __init__(self, *args, **kwargs):
        """
        These models can be configured to use 8, 35, or 480 DMX channels.
        Use this class for the 8 channel configuration.
        """
        super().__init__(*args, **kwargs)

        self._register_channel('dimmer', vdim=True)
        self._register_channel_aliases('dimmer', 'd')
        self._register_channel('strobe', vdim=True)
        self._register_channel_aliases('strobe', 's')
        self._register_channel('red', vdim=True)
        self._register_channel_aliases('red', 'r')
        self._register_channel('green', vdim=True)
        self._register_channel_aliases('green', 'g')
        self._register_channel('blue', vdim=True)
        self._register_channel_aliases('blue', 'b')
        self._register_channel('program1', vdim=True)
        self._register_channel_aliases('program1', 'p1')
        self._register_channel('program2', vdim=True)
        self._register_channel_aliases('program2', 'p2')
        self._register_channel('program_speed', vdim=True)
        self._register_channel_aliases('program_speed', 'ps')


class Pixellicious(Fixture):

    def __init__(self, mode: int, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if mode == 8:
            new = Pixellicious_8Ch(*args, **kwargs)
        else:
            raise ValueError('Number of channels (mode) has to be '
                             f'8, 35, or 480. You passed {mode}.')

        self.__dict__ = new.__dict__
