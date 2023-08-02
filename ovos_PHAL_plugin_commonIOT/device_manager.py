from pprint import pprint

from ovos_PHAL_plugin_commonIOT.opm import find_iot_plugins
from ovos_PHAL_plugin_commonIOT.opm.base import IOTAbstractDevice


class CommonIOTDeviceManager:
    def __init__(self, bus):
        """
            Args:
                bus (MycroftBusClient): The Mycroft bus client
        """
        self.scanners = {}
        self.devices = {}
        self.mappings = {}
        self.bus = bus

        # BUS API
        # self.bus.on("ovos.iot.get.devices", self.handle_get_devices)
        # self.bus.on("ovos.iot.get.device", self.handle_get_device)

        # generic device actions
        # self.bus.on("ovos.iot.device.turn_on", self.handle_turn_on)
        # self.bus.on("ovos.iot.device.turn_off", self.handle_turn_off)
        # self.bus.on("ovos.iot.device.sleep", self.handle_sleep)
        # self.bus.on("ovos.iot.device.wakeup", self.handle_wakeup)
        # self.bus.on("ovos.iot.device.reboot", self.handle_reboot)
        # self.bus.on("ovos.iot.device.get.power.state", self.handle_get_power_state)

        # iot media player actions
        # self.bus.on("ovos.iot.device.get.volume", self.handle_get_volume)
        # self.bus.on("ovos.iot.device.set.volume", self.handle_set_volume)
        # self.bus.on("ovos.iot.device.volume.up",  self.handle_volume_up)
        # self.bus.on("ovos.iot.device.volume.down", self.handle_volume_down)
        # self.bus.on("ovos.iot.device.mute", self.handle_mute)
        # self.bus.on("ovos.iot.device.unmute", self.handle_unmute)

        # iot lights actions
        self.bus.on("ovos.iot.device.get.brightness", self.handle_get_brightness)
        self.bus.on("ovos.iot.device.set.brightness", self.handle_set_brightness)
        self.bus.on("ovos.iot.device.decrease.brightness", self.handle_decrease_brightness)
        self.bus.on("ovos.iot.device.increase.brightness", self.handle_increase_brightness)
        self.bus.on("ovos.iot.device.get.color", self.handle_get_color)
        self.bus.on("ovos.iot.device.set.color", self.handle_set_color)

    # light handlers
    def handle_get_brightness(self, message):
        device = self.search_for_device(message.data.get("device"))
        if device:
            msg = message.response(data={"brightness": device.brightness})
            self.bus.emit(msg)

    def handle_set_brightness(self, message):
        device = self.search_for_device(message.data.get("device"))
        if device:
            try:
                msg = message.response(data={"brightness": device.change_brightness(message.data.get("brightness"))})
            except Exception as e:
                LOG.error(e)
                msg = message.response(data={"brightness": e})
        self.bus.emit(msg)

    def handle_decrease_brightness(self, message):
        device = self.search_for_device(message.data.get("device"))
        if device:
            try:
                amount = int(message.data.get("amount"))
                msg = message.response(data={"brightness": device.change_brightness(device.brightness - amount)})
            except Exception as e:
                LOG.error(e)
                msg = message.response(data={"brightness": e})
        self.bus.emit(msg)

    def handle_increase_brightness(self, message):
        device = self.search_for_device(message.data.get("device"))
        if device:
            try:
                amount = int(message.data.get("amount"))
                msg = message.response(data={"brightness": device.change_brightness(device.brightness + amount)})
            except Exception as e:
                LOG.error(e)
                msg = message.response(data={"brightness": e})
        self.bus.emit(msg)

    def handle_get_color(self, message):
        device = self.search_for_device(message.data.get("device"))
        if device:
            msg = message.response(data={"color": device.color})
        self.bus.emit(msg)

    def handle_set_color(self, message):
        device = self.search_for_device(message.data.get("device"))
        if device:
            try:
                msg = message.response(data={"color": device.change_color(message.data.get("color"))})
            except Exception as e:
                LOG.error(e)
                msg = message.response(data={"color": e})
        self.bus.emit(msg)

    def search_for_device(self, device):
        for d_id, d in self devices.items():
            if device == d_id or device == d.name:
                return d
        return None

    def disambiguate_new_device(self, device: IOTAbstractDevice):
        # check if device with same ip exists
        for dev_id, device2 in self.devices.items():
            if device.host == device2.host:
                print("duplicate device found, same host", device, device2)
                if device.device_id not in self.mappings:
                    self.mappings[device.device_id] = []
                if device2.device_id not in self.mappings[device.device_id]:
                    self.mappings[device.device_id].append(device2.device_id)

                if device2.device_id not in self.mappings:
                    self.mappings[device2.device_id] = []
                if device.device_id not in self.mappings[device2.device_id]:
                    self.mappings[device2.device_id].append(device.device_id)

    def on_new_device(self, device: IOTAbstractDevice):
        self.disambiguate_new_device(device)
        pprint(device.as_dict)
        self.devices[device.device_id] = device

    def on_device_lost(self, device: IOTAbstractDevice):
        pprint(device.as_dict)
        if device.device_id in self.devices:
            self.devices.pop(device.device_id)

    def load_scanners(self):
        for plugin, scanner_clazz in find_iot_plugins().items():
            try:
                scanner = scanner_clazz(self.bus,
                                        new_device_callback=self.on_new_device,
                                        lost_device_callback=self.on_device_lost)
                print(f"loaded {plugin}")
            except:
                print(f"{plugin} failed to load")
                continue
            scanner.start()
            self.scanners[plugin] = scanner

if __name__ == "__main__":
    from ovos_utils.messagebus import FakeBus
    from ovos_utils import wait_for_exit_signal

    d = CommonIOTDeviceManager(FakeBus())
    d.load_scanners()
    wait_for_exit_signal()
    # loaded ovos-iot-plugin-lan
    # loaded ovos-iot-plugin-bluetooth
    # found device: 192.168.1.1:unknown
    # {'area': {'addresses': {'ipv4': '192.168.1.1'},
    #           'hostnames': [{'name': '', 'type': ''}],
    #           'status': {'reason': 'syn-ack', 'state': 'up'},
    #           'vendor': {}},
    #  'device_class': 'LanDevice',
    #  'device_id': '192.168.1.1:unknown',
    #  'device_type': <IOTDeviceType.SENSOR: 'sensor'>,
    #  'host': '192.168.1.1',
    #  'name': 'unknown',
    #  'state': True}
    # found device: Fairphone 4 5G:E8:78:29:C2:E0:1F
    # {'area': None,
    #  'device_class': 'BluetoothDevice',
    #  'device_id': 'Fairphone 4 5G:E8:78:29:C2:E0:1F',
    #  'device_type': <IOTDeviceType.SENSOR: 'sensor'>,
    #  'host': 'E8:78:29:C2:E0:1F',
    #  'name': 'Fairphone 4 5G',
    #  'state': True}
    # lost device: Fairphone 4 5G:E8:78:29:C2:E0:1F
    # {'area': None,
    #  'device_class': 'BluetoothDevice',
    #  'device_id': 'Fairphone 4 5G:E8:78:29:C2:E0:1F',
    #  'device_type': <IOTDeviceType.SENSOR: 'sensor'>,
    #  'host': 'E8:78:29:C2:E0:1F',
    #  'name': 'Fairphone 4 5G',
    #  'state': False}
