import enum
import time
from threading import Thread
from time import sleep

from ovos_config import Configuration
from ovos_utils import camel_case_split
from ovos_utils.log import LOG
from ovos_utils.messagebus import get_mycroft_bus


class IOTDeviceType(str, enum.Enum):
    """ recognized device types handled by commonIOT"""
    SENSOR = "sensor"
    PLUG = "plug"
    SWITCH = "switch"
    BULB = "bulb"
    RGB_BULB = "bulbRGB"
    RGBW_BULB = "bulbRGBW"
    TV = "tv"
    RADIO = "radio"
    HEATER = "heater"
    AC = "ac"
    VENT = "vent"
    HUMIDIFIER = "humidifier"
    CAMERA = "camera"
    MEDIA_PLAYER = "media_player"
    VACUUM = "vacuum"


class IOTCapabilties(enum.Enum):
    """ actions recognized by commonIOT and exposed by voice intents """
    REPORT_STATUS = enum.auto()
    TURN_ON = enum.auto()
    TURN_OFF = enum.auto()
    BLINK_LIGHT = enum.auto()
    BEACON_LIGHT = enum.auto()
    REPORT_COLOR = enum.auto()
    CHANGE_COLOR = enum.auto()
    REPORT_BRIGHTNESS = enum.auto()
    CHANGE_BRIGHTNESS = enum.auto()
    GET_PICTURE = enum.auto()
    PAUSE_PLAYBACK = enum.auto()
    RESUME_PLAYBACK = enum.auto()
    STOP_PLAYBACK = enum.auto()
    NEXT_PLAYBACK = enum.auto()
    PREV_PLAYBACK = enum.auto()


class IOTScannerPlugin(Thread):
    """ this class is loaded by CommonIOT and yields IOTDevices"""

    def __init__(self, bus=None, name="", config=None,
                 new_device_callback=None,
                 lost_device_callback=None,
                 aliases=None):
        super().__init__(daemon=True)
        self.config_core = Configuration()
        name = name or camel_case_split(self.__class__.__name__).replace(" ", "-").lower()
        self.config = config or {}
        self.bus = bus or get_mycroft_bus()
        self.log = LOG
        self.name = name
        self.new_device_callback = new_device_callback
        self.lost_device_callback = lost_device_callback
        self.timestamps = {}
        self.aliases = aliases or {}
        self.ttl = 30  # if not seen for 30 seconds, consider device lost
        self.time_between_checks = 3  # seconds between scans

    def run(self):
        while True:
            for dev in self.scan():
                dev._raw["last_seen"] = time.time()
                if dev.device_id not in self.timestamps:
                    print(f"found device: {dev.device_id}")
                    if self.new_device_callback:
                        self.new_device_callback(dev)
                self.timestamps[dev.device_id] = dev  # update last seen

            for device_id, dev in dict(self.timestamps).items():
                if time.time() - dev.raw_data.get("last_seen", 0) > self.ttl:
                    # based on last_seen timestamp
                    print(f"lost device: {device_id}")
                    self.timestamps.pop(device_id)
                    if self.lost_device_callback:
                        self.lost_device_callback(dev)

            sleep(self.time_between_checks)

    def scan(self):
        raise NotImplemented("scan method must be implemented by subclasses")

    def get_device(self, ip):
        for device in self.scan():
            if device.host == ip:
                return device
        return None


class IOTAbstractDevice:
    capabilities = []

    def __init__(self, device_id, host=None, name="abstract_device",
                 area=None, device_type=IOTDeviceType.SENSOR, raw_data=None):
        # everything is a sensor, as least a binary one  (available/not available)
        self._device_type = device_type
        self._device_id = device_id
        self._name = name or self.__class__.__name__
        self._host = host
        self._area = area
        self._raw = raw_data or {
            "name": name, "host": host,
            "area": area, "device_id": device_id}
        self.mode = ""
        self._timer = None

    @property
    def as_dict(self):
        return {
            "host": self.host,
            "name": self.name,
            "device_id": self.device_id,
            "area": self.device_area,
            "device_type": self.device_type,
            "device_class": self.__class__.__name__,
            "state": self.is_on
        }

    @property
    def device_id(self):
        return self._device_id or self.raw_data.get("device_id")

    @property
    def device_type(self):
        return self._device_type

    @property
    def host(self):
        return self._host

    @property
    def name(self):
        return self._name

    @property
    def raw_data(self):
        return self._raw

    @property
    def is_online(self):
        return True

    @property
    def is_on(self):
        return True

    @property
    def is_off(self):
        return not self.is_on

    @property
    def device_display_model(self):
        # for usage in GUI, TODO document format
        return {}

    @property
    def device_area(self):
        # TODO document format
        return self._area

    def __repr__(self):
        return self.name + ":" + self.host


class Sensor(IOTAbstractDevice):
    capabilities = [
        IOTCapabilties.REPORT_STATUS
    ]

    def __init__(self, device_id, host=None, name="generic_sensor",
                 area=None, device_type=IOTDeviceType.SENSOR, raw_data=None):
        super().__init__(device_id, host, name, area, device_type, raw_data)


class Switch(Sensor):
    capabilities = Sensor.capabilities + [
        IOTCapabilties.TURN_ON,
        IOTCapabilties.TURN_OFF
    ]

    def __init__(self, device_id, host=None, name="generic_switch",
                 area=None, device_type=IOTDeviceType.SWITCH, raw_data=None):
        super().__init__(device_id, host, name, area, device_type, raw_data)

    def reset(self):
        self.mode = ""
        self._timer = None
        self.turn_on()

    # status change
    def turn_on(self):
        pass

    def turn_off(self):
        raise NotImplementedError

    def toggle(self):
        if self.is_off:
            self.turn_on()
        else:
            self.turn_off()

    def __repr__(self):
        return self.name + ":" + self.host


class Plug(Switch):
    # Switch is binary, Plug maybe not
    # usually provides power consumption etc,
    def __init__(self, device_id, host=None, name="generic_plug",
                 area=None, device_type=IOTDeviceType.PLUG, raw_data=None):
        super().__init__(device_id, host, name, area, device_type, raw_data)
