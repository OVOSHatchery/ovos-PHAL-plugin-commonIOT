from mycroft_bus_client import Message
from os.path import join, dirname
from ovos_plugin_manager.phal import PHALPlugin
from ovos_plugin_manager.templates.iot import IOTDevicePlugin, IOTScannerPlugin, Bulb, RGBBulb, RGBWBulb
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
        self.device_types = {
            "generic": IOTDevicePlugin,
            "bulb": Bulb,
            "bulbRGB": RGBBulb,
            "bulbRGBW": RGBWBulb
        }

        # BUS API
        self.bus.on("ovos.iot.get.devices",
                    self.handle_get_devices)
        self.bus.on("ovos.iot.get.device",
                    self.handle_get_device)
        self.bus.on("ovos.iot.device.turn_on",
                    self.handle_turn_on)
        self.bus.on("ovos.iot.device.turn_off",
                    self.handle_turn_off)
        self.bus.on("ovos.iot.call.function",
                    self.handle_call_function)

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

    def handle_call_function(self, message):
        """ Handle the call supported function message
        Args:
            message (Message): The message object
        """
        device_id = message.data.get("device_id", None)
        function_name = message.data.get("function_name", None)
        function_args = message.data.get("function_args", None)
        if device_id is not None and function_name is not None:
            for dev_id, device in self.registered_devices.items():
                if dev_id == device_id:
                    if function_args is not None:
                        response = device.call_function(function_name, function_args)
                    else:
                        response = device.call_function(function_name)
                    self.bus.emit(message.response(data=response))
                    return
        else:
            LOG.error("Device id or function name not provided")

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

        super().shutdown()
