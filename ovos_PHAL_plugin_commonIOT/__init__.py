from os.path import join, dirname

from mycroft_bus_client import Message
from ovos_plugin_manager.phal import PHALPlugin
from ovos_utils.gui import GUIInterface
from ovos_utils.log import LOG

from ovos_PHAL_plugin_commonIOT.devices import Bulb, RGBBulb, RGBWBulb, GenericDevice


class commonIOTPluginValidator:
    @staticmethod
    def validate(config=None):
        """ this method is called before loading the plugin.
        If it returns False the plugin is not loaded.
        This allows a plugin to run platform checks"""
        return True


class commonIOTPlugin(PHALPlugin):
    validator = commonIOTPluginValidator

    def __init__(self, bus=None, config=None):
        """ Initialize the plugin
            Args:
                bus (MycroftBusClient): The Mycroft bus client
                config (dict): The plugin configuration
        """
        super().__init__(bus=bus, name="ovos-PHAL-plugin-iot", config=config)
        self.registered_devices = {}  # device_id: device object
        self.bus = bus
        self.gui = GUIInterface(bus=self.bus, skill_id=self.name)

        self.device_types = {
            "generic": GenericDevice,
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
        self.bus.on("ovos.iot.call.supported.function",
                    self.handle_call_supported_function)

        # GUI EVENTS
        self.bus.on("ovos.iot.home",
                    self.handle_show_dashboard)
        self.bus.on("ovos.iot.close",
                    self.handle_close_dashboard)
        self.bus.on("ovos.iot.show.device.dashboard",
                    self.handle_show_device_dashboard)
        self.bus.on("ovos.iot.update.device.dashboard",
                    self.handle_update_device_dashboard)

        self.bus.on("ovos.iot.get.device.display.model",
                    self.handle_get_device_display_model)
        self.bus.on("ovos.iot.get.device.display.list.model",
                    self.handle_get_device_display_list_model)

    def build_display_dashboard_model(self):
        """ Build the dashboard model """
        device_type_model = []
        for dev_id, device in self.registered_devices.items():
            device_type = device.device_type
            if device_type not in device_type_model:
                device_type_model.append(device_type)

        display_list_model = []
        for device_type in device_type_model:
            device_type_list_model = []
            for dev_id, device in self.registered_devices.items():
                clazz = self.device_types.get(device_type)
                if isinstance(device, clazz):
                    model = {}  # TODO - device.get_device_display_model()
                    device_type_list_model.append(model)
            device_human_readable_type = device_type.replace("_", " ").title()
            display_list_model.append({
                "type": device_type,
                "icon": f"mdi:{device_type}",
                "name": device_human_readable_type,
                "devices": device_type_list_model
            })
        return display_list_model

    def build_display_device_model(self, device_type):
        """ Build the device model
        Args:
            device_type (String): The device type to build the model for
        Returns:
            dict: The device model
        """
        device_type_list_model = []
        for dev_id, device in self.registered_devices.items():
            clazz = self.device_types.get(device_type)
            if isinstance(device, clazz):
                model = {}  # TODO - device.get_device_display_model()
                device_type_list_model.append(model)
        return device_type_list_model

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

    def handle_call_supported_function(self, message):
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
                        response = device.call_function(
                            function_name, function_args)
                    else:
                        response = device.call_function(function_name)
                    self.bus.emit(message.response(data=response))
                    return
        else:
            LOG.error("Device id or function name not provided")

    def handle_get_device_display_model(self, message):
        """ Handle the get device display model message
            Args:
                message (Message): The message object
        """
        device_id = message.data.get("device_id", None)
        if device_id is not None:
            for dev_id, device in self.registered_devices.items():
                if dev_id == device_id:
                    self.bus.emit(message.response(
                        data=device.get_device_display_model()))
                    return
        self.bus.emit(message.response(data={}))

    def handle_get_device_display_list_model(self, message):
        """ Handle the get device display list model message
            Args:
                message (Message): The message object
        """
        # TODO - build_display_list_model missing, also not in HA plugin
        display_list_model = {"items": self.build_display_list_model()}
        self.bus.emit(message.response(data=display_list_model))

    # GUI INTERFACE HANDLERS
    def handle_show_dashboard(self, message):
        """ Handle the show dashboard message
            Args:
                message (Message): The message object
        """
        display_list_model = {"items": self.build_display_dashboard_model()}
        self.gui["dashboardModel"] = display_list_model
        self.gui["instanceAvailable"] = True
        self.gui.send_event("ovos.iot.change.dashboard", {
            "dash_type": "main"})
        page = join(dirname(__file__), "ui", "Dashboard.qml")
        self.gui.show_page(page, override_idle=True)

    def handle_close_dashboard(self, message):
        """ Handle the close dashboard message
            Args:
                message (Message): The message object
        """
        self.gui.release()

    def handle_show_device_dashboard(self, message):
        """ Handle the show device dashboard message
            Args:
                message (Message): The message object
        """
        device_type = message.data.get("device_type", None)
        if device_type is not None:
            self.gui["deviceDashboardModel"] = {
                "items": self.build_display_device_model(device_type)}
            self.gui.send_event("ovos.iot.change.dashboard", {
                "dash_type": "device"})

    def handle_update_device_dashboard(self, message):
        """ Handle the update device dashboard message
            Args:
                message (Message): The message object
        """
        device_type = message.data.get("device_type", None)
        if device_type is not None:
            self.gui["deviceDashboardModel"] = {
                "items": self.build_display_device_model(device_type)}

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
        self.bus.remove("ovos.iot.call.supported.function",
                        self.handle_call_supported_function)

        # GUI EVENTS
        self.bus.remove("ovos.iot.home",
                        self.handle_show_dashboard)
        self.bus.remove("ovos.iot.close",
                        self.handle_close_dashboard)
        self.bus.remove("ovos.iot.show.device.dashboard",
                        self.handle_show_device_dashboard)
        self.bus.remove("ovos.iot.update.device.dashboard",
                        self.handle_update_device_dashboard)

        self.bus.remove("ovos.iot.get.device.display.model",
                        self.handle_get_device_display_model)
        self.bus.remove("ovos.iot.get.device.display.list.model",
                        self.handle_get_device_display_list_model)
        super().shutdown()
