from ovos_PHAL_plugin_commonIOT.opm.base import IOTCapabilties, IOTDeviceType, Sensor, Plug


class Heater(Plug):
    def __init__(self, device_id, host=None, name="generic_heater",
                 area=None, device_type=IOTDeviceType.HEATER, raw_data=None):
        super().__init__(device_id, host, name, area, device_type, raw_data)

    # only has on/off for now
    # TODO - get temperature


class AirConditioner(Plug):
    def __init__(self, device_id, host=None, name="generic_ac",
                 area=None, device_type=IOTDeviceType.AC, raw_data=None):
        super().__init__(device_id, host, name, area, device_type, raw_data)

    # only has on/off for now
    # TODO - get temperature


class Vent(Plug):
    def __init__(self, device_id, host=None, name="generic_vent",
                 area=None, device_type=IOTDeviceType.VENT, raw_data=None):
        super().__init__(device_id, host, name, area, device_type, raw_data)


class Humidifier(Plug):
    def __init__(self, device_id, host=None, name="generic_humidifier",
                 area=None, device_type=IOTDeviceType.HUMIDIFIER, raw_data=None):
        super().__init__(device_id, host, name, area, device_type, raw_data)


class Vacuum(Plug):
    def __init__(self, device_id, host=None, name="generic_vacuum",
                 area=None, device_type=IOTDeviceType.VACUUM, raw_data=None):
        super().__init__(device_id, host, name, area, device_type, raw_data)

    # only has on/off for now
    # TODO - vacuum stuff


class Camera(Sensor):
    capabilities = Sensor.capabilities + [
        IOTCapabilties.GET_PICTURE
    ]

    def __init__(self, device_id, host=None, name="generic_camera",
                 area=None, device_type=IOTDeviceType.CAMERA, raw_data=None):
        super().__init__(device_id, host, name, area, device_type, raw_data)

    def get_picture(self):
        return NotImplemented
