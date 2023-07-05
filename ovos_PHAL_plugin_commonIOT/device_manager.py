
class CommonIOTDeviceManager:
    def __init__(self, bus):
        """
            Args:
                bus (MycroftBusClient): The Mycroft bus client
        """
        self.registered_devices = {}  # device_id: device object
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
