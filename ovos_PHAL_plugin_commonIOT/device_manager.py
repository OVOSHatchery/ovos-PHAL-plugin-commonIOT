from mycroft_bus_client import Message
from os.path import join, dirname
from ovos_plugin_manager.phal import PHALPlugin
from ovos_plugin_manager.templates.iot import IOTDevicePlugin, IOTScannerPlugin, Bulb, RGBBulb, RGBWBulb, DEVICE_TYPES
from ovos_utils.gui import GUIInterface
from ovos_utils.log import LOG


class CommonIOTDeviceManager:
    def __init__(self, bus=None):
        """
            Args:
                bus (MycroftBusClient): The Mycroft bus client
        """
        self.registered_devices = {}  # device_id: device object
        self.bus = bus

        # BUS API
        self.bus.on("ovos.iot.get.devices",
                    self.handle_get_devices)
        self.bus.on("ovos.iot.get.device",
                    self.handle_get_device)
        self.bus.on("ovos.iot.device.turn_on",
                    self.handle_turn_on)
        self.bus.on("ovos.iot.device.turn_off",
                    self.handle_turn_off)
        self.bus.on("ovos.iot.device.sleep",
                    self.handle_sleep)
        self.bus.on("ovos.iot.device.wakeup",
                    self.handle_wakeup)
        self.bus.on("ovos.iot.device.reboot",
                    self.handle_reboot)
        self.bus.on("ovos.iot.device.get.power.state",
                    self.handle_get_power_state)
        self.bus.on("ovos.iot.device.get.volume",
                    self.handle_get_volume)
        self.bus.on("ovos.iot.device.set.volume",
                    self.handle_set_volume)
        self.bus.on("ovos.iot.device.volume.up",
                    self.handle_volume_up)
        self.bus.on("ovos.iot.device.volume.down",
                    self.handle_volume_down)
        self.bus.on("ovos.iot.device.mute",
                    self.handle_mute)
        self.bus.on("ovos.iot.device.unmute",
                    self.handle_unmute)
        self.bus.on("ovos.iot.device.get.channel",
                    self.handle_get_channel)
        self.bus.on("ovos.iot.device.set.channel",
                    self.handle_set_channel)
        self.bus.on("ovos.iot.device.channel.up",
                    self.handle_channel_up)
        self.bus.on("ovos.iot.device.channel.down",
                    self.handle_channel_down)
        self.bus.on("ovos.iot.device.get.apps",
                    self.handle_get_apps)
        self.bus.on("ovos.iot.device.get.active.app",
                    self.handle_get_active_app)
        self.bus.on("ovos.iot.device.set.active.app",
                    self.handle_set_active_app)

    # BUS API HANDLERS
    def handle_get_devices(self, message):
        """ Handle the get devices message
            Args:
                message (Message): The message object
        """
        self.bus.emit(message.response(data=self.registered_devices))

    def handle_get_device(self, message):
        device_id = message.data.get("device_id", None)
        if device_id is not None:
            for dev_id, device in self.registered_devices.items():
                if dev_id == device_id:
                    self.bus.emit(message.response(data=device))
                    return
        self.bus.emit(message.response(data=None))

    def handle_turn_on(self, message):
        """ Handle the turn on message
            Args:
                message (Message): The message object
        """
        device_id = message.data.get("device_id", None)
        if device_id is not None:
            for dev_id, device in self.registered_devices.items():
                if dev_id == device_id:
                    response = device.turn_on()
                    self.bus.emit(message.response(data=response))
                    return
        else:
            LOG.warning("No device id provided")

    def handle_turn_off(self, message):
        """ Handle the turn off message
            Args:
                message (Message): The message object
        """
        device_id = message.data.get("device_id", None)
        if device_id is not None:
            for dev_id, device in self.registered_devices.items():
                if dev_id == device_id:
                    response = device.turn_off()
                    self.bus.emit(message.response(data=response))
                    return
        else:
            LOG.error("No device id provided")

    def handle_sleep(self, message):
        """ Handle the sleep message
            Args:
                message (Message): The message object
        """
        device_id = message.data.get("device_id", None)
        if device_id is not None:
            for dev_id, device in self.registered_devices.items():
                if dev_id == device_id:
                    response = device.sleep()
                    self.bus.emit(message.response(data=response))
                    return
        else:
            LOG.error("No device id provided")

    def handle_wakeup(self, message):
        """ Handle the wakeup message
            Args:
                message (Message): The message object
        """
        device_id = message.data.get("device_id", None)
        if device_id is not None:
            for dev_id, device in self.registered_devices.items():
                if dev_id == device_id:
                    response = device.wakeup()
                    self.bus.emit(message.response(data=response))
                    return
        else:
            LOG.error("No device id provided")

    def handle_reboot(self, message):
        """ Handle the reboot message
            Args:
                message (Message): The message object
        """
        device_id = message.data.get("device_id", None)
        if device_id is not None:
            for dev_id, device in self.registered_devices.items():
                if dev_id == device_id:
                    response = device.reboot()
                    self.bus.emit(message.response(data=response))
                    return
        else:
            LOG.error("No device id provided")

    def handle_get_power_state, message):
        """ Handle the power state message
            Args:
                message (Message): The message object
        """
        device_id = message.data.get("device_id", None)
        if device_id is not None:
            for dev_id, device in self.registered_devices.items():
                if dev_id == device_id:
                    response = device.power_state()
                    self.bus.emit(message.response(data=response))
                    return
        else:
            LOG.error("No device id provided")

    def handle_get_volume(self, message):
        """ Handle the get volume message
            Args:
                message (Message): The message object
        """
        device_id = message.data.get("device_id", None)
        if device_id is not None:
            for dev_id, device in self.registered_devices.items():
                if dev_id == device_id:
                    response = device.get_volume()
                    self.bus.emit(message.response(data=response))
                    return
        else:
            LOG.error("No device id provided")

    def handle_set_volume(self, message):
        """ Handle the set volume message
            Args:
                message (Message): The message object
        """
        device_id = message.data.get("device_id", None)
        volume = message.data.get("volume", None)
        if device_id is not None and volume is not None:
            for dev_id, device in self.registered_devices.items():
                if dev_id == device_id:
                    response = device.set_volume(volume)
                    self.bus.emit(message.response(data=response))
                    return
        else:
            LOG.error("No device id provided")

    def handle_volume_up(self, message):
        """ Handle the volume up message
            Args:
                message (Message): The message object
        """
        device_id = message.data.get("device_id", None)
        if device_id is not None:
            for dev_id, device in self.registered_devices.items():
                if dev_id == device_id:
                    response = device.volume_up()
                    self.bus.emit(message.response(data=response))
                    return
        else:
            LOG.error("No device id provided")

    def handle_volume_down(self, message):
        """ Handle the volume down message
            Args:
                message (Message): The message object
        """
        device_id = message.data.get("device_id", None)
        if device_id is not None:
            for dev_id, device in self.registered_devices.items():
                if dev_id == device_id:
                    response = device.volume_down()
                    self.bus.emit(message.response(data=response))
                    return
        else:
            LOG.error("No device id provided")

    def handle_mute(self, message):
        """ Handle the mute message
            Args:
                message (Message): The message object
        """
        device_id = message.data.get("device_id", None)
        if device_id is not None:
            for dev_id, device in self.registered_devices.items():
                if dev_id == device_id:
                    response = device.mute()
                    self.bus.emit(message.response(data=response))
                    return
        else:
            LOG.error("No device id provided")

    def handle_unmute(self, message):
        """ Handle the unmute message
            Args:
                message (Message): The message object
        """
        device_id = message.data.get("device_id", None)
        if device_id is not None:
            for dev_id, device in self.registered_devices.items():
                if dev_id == device_id:
                    response = device.unmute()
                    self.bus.emit(message.response(data=response))
                    return
        else:
            LOG.error("No device id provided")

    def handle_get_channel(self, message):
        """ Handle the get channel message
            Args:
                message (Message): The message object
        """
        device_id = message.data.get("device_id", None)
        if device_id is not None:
            for dev_id, device in self.registered_devices.items():
                if dev_id == device_id:
                    response = device.get_channel()
                    self.bus.emit(message.response(data=response))
                    return
        else:
            LOG.error("No device id provided")

    def handle_set_channel(self, message):
        """ Handle the sleep message
            Args:
                message (Message): The message object
        """
        device_id = message.data.get("device_id", None)
        channel = message.data.get("channel", None)
        if device_id is not None and channel is not None:
            for dev_id, device in self.registered_devices.items():
                if dev_id == device_id:
                    response = device.set_channel(channel)
                    self.bus.emit(message.response(data=response))
                    return
        else:
            LOG.error("No device id provided")

    def handle_channel_up(self, message):
        """ Handle the channel up message
            Args:
                message (Message): The message object
        """
        device_id = message.data.get("device_id", None)
        if device_id is not None:
            for dev_id, device in self.registered_devices.items():
                if dev_id == device_id:
                    response = device.channel_up()
                    self.bus.emit(message.response(data=response))
                    return
        else:
            LOG.error("No device id provided")

    def handle_channel_down(self, message):
        """ Handle the channel down message
            Args:
                message (Message): The message object
        """
        device_id = message.data.get("device_id", None)
        if device_id is not None:
            for dev_id, device in self.registered_devices.items():
                if dev_id == device_id:
                    response = device.channel_down()
                    self.bus.emit(message.response(data=response))
                    return
        else:
            LOG.error("No device id provided")

    def handle_get_apps(self, message):
        """ Handle the get apps message
            Args:
                message (Message): The message object
        """
        device_id = message.data.get("device_id", None)
        if device_id is not None:
            for dev_id, device in self.registered_devices.items():
                if dev_id == device_id:
                    response = device.get_apps()
                    self.bus.emit(message.response(data=response))
                    return
        else:
            LOG.error("No device id provided")

    def handle_set_active_app(self, message):
        """ Handle the set active app message
            Args:
                message (Message): The message object
        """
        device_id = message.data.get("device_id", None)
        app = message.data.get("app", None)
        if device_id is not None and app is not None:
            for dev_id, device in self.registered_devices.items():
                if dev_id == device_id:
                    response = device.set_app(app)
                    self.bus.emit(message.response(data=response))
                    return
        else:
            LOG.error("No device id provided")

    def shutdown(self):
        # BUS API
        self.bus.remove("ovos.iot.get.devices",
                        self.handle_get_devices)
        self.bus.remove("ovos.iot.get.device",
                        self.handle_get_device)
        self.bus.remove("ovos.iot.device.turn_on",
                        self.handle_turn_on)
        self.bus.remove("ovos.iot.device.turn_off",
                        self.handle_turn_off)
        self.bus.remove("ovos.iot.call.function",
                        self.handle_call_function)
        self.bus.remove("ovos.iot.device.sleep",
                    self.handle_sleep)
        self.bus.remove("ovos.iot.device.wakeup",
                    self.handle_wakeup)
        self.bus.remove("ovos.iot.device.reboot",
                    self.handle_reboot)
        self.bus.remove("ovos.iot.device.get.power.state",
                    self.handle_get_power_state)
        self.bus.remove("ovos.iot.device.get.volume",
                    self.handle_get_volume)
        self.bus.remove("ovos.iot.device.set.volume",
                    self.handle_set_volume)
        self.bus.remove("ovos.iot.device.volume.up",
                    self.handle_volume_up)
        self.bus.remove("ovos.iot.device.volume.down",
                    self.handle_volume_down)
        self.bus.remove("ovos.iot.device.mute",
                    self.handle_mute)
        self.bus.remove("ovos.iot.device.unmute",
                    self.handle_unmute)
        self.bus.remove("ovos.iot.device.get.channel",
                    self.handle_get_channel)
        self.bus.remove("ovos.iot.device.set.channel",
                    self.handle_set_channel)
        self.bus.remove("ovos.iot.device.channel.up",
                    self.handle_channel_up)
        self.bus.remove("ovos.iot.device.channel.down",
                    self.handle_channel_down)
        self.bus.remove("ovos.iot.device.get.apps",
                    self.handle_get_apps)
        self.bus.remove("ovos.iot.device.get.active.app",
                    self.handle_get_active_app)
        self.bus.remove("ovos.iot.device.set.active.app",
                    self.handle_set_active_app)

        super().shutdown()
