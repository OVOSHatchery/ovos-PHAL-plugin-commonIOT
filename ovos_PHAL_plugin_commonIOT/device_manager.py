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

    def on_new_device(self, device: IOTAbstractDevice):
        pprint(device.as_dict)

    def on_device_lost(self, device: IOTAbstractDevice):
        pprint(device.as_dict)

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
