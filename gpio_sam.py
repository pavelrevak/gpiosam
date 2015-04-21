import os
import mmap
import struct


""" Control GPIO ports on Atmel SAM (AT91SAM) MCUs
This class need root privileges
"""

class Gpio(object):
    _PIO_ENABLE = 0x000
    _PIO_DISABLE = 0x004
    _PIO_STATUS = 0x008
    _OUTPUT_ENABLE = 0x010
    _OUTPUT_DISABLE = 0x014
    _OUTPUT_STATUS = 0x018
    _FILTER_ENABLE = 0x020
    _FILTER_DISABLE = 0x024
    _FILTER_STATUS = 0x028
    _OUTPUT_DATA_SET = 0x030
    _OUTPUT_DATA_CLEAR = 0x034
    _OUTPUT_DATA_STATUS = 0x038
    _PIN_DATA_STATUS = 0x03c
    _MULTI_DRIVER_ENABLE = 0x050
    _MULTI_DRIVER_DISABLE = 0x054
    _MULTI_DRIVER_STATUS = 0x058
    _PULL_UP_DISABLE = 0x060
    _PULL_UP_ENABLE = 0x064
    _PULL_UP_STATUS = 0x068
    _PULL_DOWN_DISABLE = 0x090
    _PULL_DOWN_ENABLE = 0x094
    _PULL_DOWN_STATUS = 0x098

    _mf = None
    _mm = None

    @classmethod
    def _reg_init(cls, offset, size):
        if cls._mm is None:
            cls._mf = os.open("/dev/mem", os.O_RDWR | os.O_SYNC)
            cls._mm = mmap.mmap(cls._mf, size, offset=offset)

    def _reg_get(self, register):
        return struct.unpack('<L', Gpio._mm[self._addr + register:self._addr + register + 4])[0]

    def _reg_set(self, register, data):
        Gpio._mm[self._addr + register:self._addr + register + 4] = struct.pack('<L', data)

    def __init__(self, port, pin):
        if not isinstance(port, int):
            port = ord(port.upper()) - ord('A')
        Gpio._reg_init(0xfffff000, 0x1000)
        self._port = port
        self._pin = pin
        self._addr = 0x400 + 0x200 * port
        self._bitval = 1 << pin

    @property
    def enable(self):
        return (self._reg_get(Gpio._PIO_STATUS) & self._bitval) > 0
    @enable.setter
    def enable(self, value):
        self._reg_set(Gpio._PIO_ENABLE if value else Gpio._PIO_DISABLE, self._bitval)

    @property
    def output_mode(self):
        return (self._reg_get(Gpio._OUTPUT_STATUS) & self._bitval) > 0
    @output_mode.setter
    def output_mode(self, value):
        self._reg_set(Gpio._OUTPUT_ENABLE if value else Gpio._OUTPUT_DISABLE, self._bitval)

    @property
    def open_drain(self):
        return (self._reg_get(Gpio._MULTI_DRIVER_STATUS) & self._bitval) > 0
    @open_drain.setter
    def open_drain(self, value):
        self._reg_set(Gpio._MULTI_DRIVER_ENABLE if value else Gpio._MULTI_DRIVER_DISABLE, self._bitval)

    @property
    def pull_up(self):
        return (self._reg_get(Gpio._PULL_UP_STATUS) & self._bitval) > 0
    @pull_up.setter
    def pull_up(self, value):
        self._reg_set(Gpio._PULL_UP_ENABLE if value else Gpio._PULL_UP_DISABLE, self._bitval)

    @property
    def pull_down(self):
        return (self._reg_get(Gpio._PULL_DOWN_STATUS) & self._bitval) > 0
    @pull_down.setter
    def pull_down(self, value):
        self._reg_set(Gpio._PULL_DOWN_ENABLE if value else Gpio._PULL_DOWN_DISABLE, self._bitval)

    @property
    def output(self):
        return (self._reg_get(Gpio._OUTPUT_DATA_STATUS) & self._bitval) > 0
    @output.setter
    def output(self, value):
        self._reg_set(Gpio._OUTPUT_DATA_SET if value else Gpio._OUTPUT_DATA_CLEAR, self._bitval)

    @property
    def input(self):
        return (self._reg_get(Gpio._PIN_DATA_STATUS) & self._bitval) > 0
