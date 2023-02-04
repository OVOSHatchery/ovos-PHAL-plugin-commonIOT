import uuid
from mycroft_bus_client.message import Message
from os.path import dirname, join
from ovos_config.config import update_mycroft_config
from ovos_plugin_manager.iot import DEVICE_TYPES
from ovos_utils.gui import GUIInterface
from ovos_utils.log import LOG


class CommonIOTDashboard:
    def __init__(self, bus=None):
        """

            Args:
                bus (MycroftBusClient): The Mycroft bus client
        """
        self.name = "ovos.iot"
        self.registered_devices = []  # IOTDevice from OPM
        self.bus = bus
        self.gui = GUIInterface(bus=self.bus, skill_id=self.name)

        # GUI EVENTS
        self.bus.on("ovos.iot.home",
                    self.handle_show_dashboard)
        self.bus.on("ovos.iot.close",
                    self.handle_close_dashboard)
        self.bus.on("ovos.iot.show.device.dashboard",
                    self.handle_show_device_dashboard)
        self.bus.on("ovos.iot.show.area.dashboard",
                    self.handle_show_area_dashboard)
        self.bus.on("ovos.iot.update.device.dashboard",
                    self.handle_update_device_dashboard)
        self.bus.on("ovos.iot.update.area.dashboard",
                    self.handle_update_area_dashboard)
        self.bus.on("ovos.iot.set.group.display.settings",
                    self.handle_set_group_display_settings)

    def build_display_dashboard_device_model(self):
        """ Build the dashboard model """
        device_type_model = []
        for device in self.registered_devices:
            device_type = device.device_type
            if device_type not in device_type_model:
                device_type_model.append(device_type)

        display_list_model = []
        for device_type in device_type_model:
            device_type_list_model = []
            for device in self.registered_devices:
                if device.device_type == device_type:
                    device_type_list_model.append(
                        device.device_display_model)
            device_human_readable_type = device_type.replace("_", " ").title()
            display_list_model.append({
                "type": device_type,
                "icon": f"mdi:{device_type}",
                "name": device_human_readable_type,
                "devices": device_type_list_model
            })
        return display_list_model

    def build_display_dashboard_area_model(self):
        """ Build the display model by area """
        unknown_area_devices = []
        area_model = []
        display_list_model = []
        for device in self.registered_devices:
            if device.device_area is not None:
                if device.device_area not in area_model:
                    area_model.append(device.device_area)
            else:
                unknown_area_devices.append(device)

        display_list_model.append({
            "type": "unknown",
            "icon": "mdi:ungrouped",
            "name": "Unknown Location",
            "devices": [device.device_display_model
                        for device in unknown_area_devices]
        })

        for area in area_model:
            area_list_model = []
            for device in self.registered_devices:
                if device.device_area == area:
                    area_list_model.append(device.device_display_model)

            display_list_model.append({
                "type": area,
                "icon": "mdi:grouped",
                "name": area.replace("_", " ").title(),
                "devices": area_list_model
            })

        return display_list_model

    def build_display_device_type_devices_model(self, device_type):
        """ Build the devices model based on the device type

        Args:
            device_type (String): The device type to build the model for

        Returns:
            dict: The device model
        """
        device_type_list_model = []
        for device in self.registered_devices:
            if device.device_type == device_type:
                device_type_list_model.append(
                    device.device_display_model)
        return device_type_list_model

    def build_display_area_devices_model(self, area):
        """ Build the devices model based on the area

        Args:
            area (String): The area to build the model for

        Returns:
            dict: The device model
        """
        area_list_model = []
        for device in self.registered_devices:
            if device.device_area == area:
                area_list_model.append(device.device_display_model)
            if device.device_area is None and area == "unknown":
                area_list_model.append(device.device_display_model)

        return area_list_model

    # BUS API HANDLERS
    def handle_get_devices(self, message):
        """ Handle the get devices message

            Args:
                message (Message): The message object
        """
        # build a plain list of devices
        device_list = []
        for device in self.registered_devices:
            device_list.append(device.device_display_model)

        self.bus.emit(message.response(data=device_list))

    def handle_get_device(self, message):
        device_id = message.data.get("device_id", None)
        if device_id is not None:
            for device in self.registered_devices:
                if device.device_id == device_id:
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
            for device in self.registered_devices:
                if device.device_id == device_id:
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
            for device in self.registered_devices:
                if device.device_id == device_id:
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
        # TODO - add this to OPM
        device_id = message.data.get("device_id", None)
        function_name = message.data.get("function_name", None)
        function_args = message.data.get("function_args", None)
        if device_id is not None and function_name is not None:
            for device in self.registered_devices:
                if device.device_id == device_id:
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
            for device in self.registered_devices:
                if device.device_id == device_id:
                    self.bus.emit(message.response(
                        data=device.device_display_model))
                    return
        self.bus.emit(message.response(data=None))

    def handle_get_device_display_list_model(self, message):
        """ Handle the get device display list model message

            Args:
                message (Message): The message object
        """
        display_list_model = []
        for device in self.registered_devices:
            display_list_model.append(device.device_display_model)
        self.bus.emit(message.response(data=display_list_model))

    # GUI INTERFACE HANDLERS
    def handle_show_dashboard(self, message=None):
        """ Handle the show dashboard message

            Args:
                message (Message): The message object
        """
        if self.instance_available:
            self.gui["use_websocket"] = self.use_ws
            if not self.config.get("use_group_display"):
                display_list_model = {
                    "items": self.build_display_dashboard_device_model()}
            else:
                display_list_model = {
                    "items": self.build_display_dashboard_area_model()}

            self.gui["dashboardModel"] = display_list_model
            self.gui["instanceAvailable"] = True
            self.gui.send_event("ovos.iot.change.dashboard", {
                "dash_type": "main"})
            page = join(dirname(__file__), "ui", "Dashboard.qml")
            self.gui["use_group_display"] = self.config.get("use_group_display", False)
            self.gui.show_page(page, override_idle=True)
        else:
            self.gui["dashboardModel"] = {"items": []}
            self.gui["instanceAvailable"] = False
            self.gui.send_event("ovos.iot.change.dashboard", {
                "dash_type": "main"})
            page = join(dirname(__file__), "ui", "Dashboard.qml")
            self.gui["use_group_display"] = self.config.get("use_group_display", False)
            self.gui.show_page(page, override_idle=True)

        if self.enable_debug:
            LOG.debug("Using group display")
            LOG.debug(self.config["use_group_display"])

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
                "items": self.build_display_device_type_devices_model(device_type)}
            self.gui.send_event("ovos.iot.change.dashboard", {
                "dash_type": "device"})

    def handle_show_area_dashboard(self, message):
        """ Handle the show area dashboard message

            Args:
                message (Message): The message object
        """
        area = message.data.get("area", None)
        if area is not None:
            self.gui["areaDashboardModel"] = {
                "items": self.build_display_area_devices_model(area)}
            self.gui.send_event("ovos.iot.change.dashboard", {
                "dash_type": "area"})

    def handle_update_device_dashboard(self, message):
        """ Handle the update device dashboard message

            Args:
                message (Message): The message object
        """
        device_type = message.data.get("device_type", None)
        if device_type is not None:
            self.gui["deviceDashboardModel"] = {
                "items": self.build_display_device_type_devices_model(device_type)}

    def handle_update_area_dashboard(self, message):
        """ Handle the update area dashboard message

            Args:
                message (Message): The message object
        """
        area = message.data.get("area_type", None)
        if area is not None:
            self.gui["areaDashboardModel"] = {
                "items": self.build_display_area_devices_model(area)}

    def handle_set_group_display_settings(self, message):
        """ Handle the set group display settings message

            Args:
                message (Message): The message object
        """
        group_settings = message.data.get("use_group_display", None)
        if group_settings is not None:
            if group_settings == True:
                use_group_display = True
                self.config["use_group_display"] = use_group_display
            else:
                use_group_display = False
                self.config["use_group_display"] = use_group_display

            config_patch = {
                "PHAL": {
                    "ovos-PHAL-plugin-commonIOT": {
                        "use_group_display": use_group_display
                    }
                }
            }
            update_mycroft_config(config=config_patch, bus=self.bus)
            self.gui["use_group_display"] = self.config.get("use_group_display")
            self.handle_show_dashboard()

    # EVENT SIGNAL ON DEVICE UPDATE
    def device_updated(self, device_id):
        """Send a device updated signal to the GUI.
        It can request a new display model once it receives this signal.

        Args:
            device (dict): The device that was updated.
        """
        # GUI only event as we don't want to flood the GUI bus
        self.gui.send_event("ovos.iot.device.updated", {"device_id": device_id})
        self.bus.emit(Message("ovos.iot.device.state.updated"))
