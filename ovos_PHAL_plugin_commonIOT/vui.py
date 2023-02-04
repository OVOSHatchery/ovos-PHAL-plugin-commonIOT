import asyncio
from mycroft_bus_client.message import Message
from ovos_utils.log import LOG
from ovos_utils.parse import fuzzy_match
from ovos_workshop.app import OVOSAbstractApplication


class IOTVoiceInterface(OVOSAbstractApplication):
    def __init__(self, bus=None):
        super().__init__(skill_id="ovos.iot", bus=bus)
        self.devices_list = None

    def initialize(self):
        self.build_device_list()
        self.bus.on(
            "ovos.iot.get.devices.response", self.handle_device_list)
        self.bus.on("ovos.iot.device.state.updated",
                    self.handle_device_state_update)

    def build_device_list(self):
        self.bus.emit(Message("ovos.iot.get.devices"))

    def handle_device_list(self, message):
        self.devices_list = message.data

    def handle_device_state_update(self, message):
        self.build_device_list()

    #@intent_handler("turn.on.intent")
    def handle_turn_on_intent(self, message):
        device = message.data.get("device")
        LOG.info(f"Device: {device}")
        device_id = self.get_device_id(device)
        LOG.info(f"Device ID: {device_id}")
        if device:
            self.bus.emit(Message("ovos.iot.device.turn_on", {
                "device_id": device_id}))
        else:
            self.speak_dialog("device.not.found", data={"device": device})

    #@intent_handler("turn.off.intent")
    def handle_turn_off_intent(self, message):
        device = message.data.get("device")
        device_id = self.get_device_id(device)
        if device:
            self.bus.emit(Message("ovos.iot.device.turn_off", {
                "device_id": device_id}))
        else:
            self.speak_dialog("device.not.found", data={"device": device})

    #@intent_handler("open.dashboard.intent")
    def handle_open_dashboard_intent(self, message):
        self.bus.emit(Message("ovos-PHAL-plugin-homeassistant.home"))

    #@intent_handler("close.dashboard.intent")
    def handle_close_dashboard_intent(self, message):
        self.bus.emit(Message("ovos-PHAL-plugin-homeassistant.close"))

    #@intent_handler("lights.get.brightness.intent")
    def handle_get_brightness_intent(self, message):
        device = message.data.get("device")
        device_id = self.get_device_id(device)
        if device_id:
            for dev in self.devices_list:
                if dev["id"] == device_id:
                    brightness = dev["attributes"].get("brightness")
                    if brightness:
                        self.speak_dialog("lights.current.brightness", data={
                            "brightness": round(brightness / 255 * 100), "device": device})
                    else:
                        self.speak_dialog("lights.status.not.available", data={
                            "device": device, "status": "brightness"})

    #@intent_handler("lights.set.brightness.intent")
    def handle_set_brightness_intent(self, message):
        device = message.data.get("device")
        brightness = message.data.get("brightness")
        device_id = self.get_device_id(device)
        if device_id:
            call_data = {
                "device_id": device_id,
                "function_name": "turn_on",
                "data": {
                    "brightness": round(brightness / 100 * 255)
                }
            }
            self.bus.emit(
                Message("ovos.iot.call.supported.function", call_data))
        else:
            self.speak_dialog("device.not.found", data={"device": device})

    #@intent_handler("lights.increase.brightness.intent")
    def handle_increase_brightness_intent(self, message):
        device = message.data.get("device")
        device_id = self.get_device_id(device)
        if device_id:
            for device in self.devices_list:
                if device["id"] == device_id:
                    brightness = device["attributes"].get("brightness")
                    break

            brightness = round(brightness / 255 * 100) + 10
            self.handle_set_brightness_intent(
                {"device": device, "brightness": brightness})

    #@intent_handler("lights.decrease.brightness.intent")
    def handle_decrease_brightness_intent(self, message):
        device = message.data.get("device")
        device_id = self.get_device_id(device)
        if device_id:
            for device in self.devices_list:
                if device["id"] == device_id:
                    brightness = device["attributes"].get("brightness")
                    break

            brightness = max(round(brightness / 255 * 100) - 10, 0)
            self.handle_set_brightness_intent(
                {"device": device, "brightness": brightness})

    #@intent_handler("lights.get.color.intent")
    def handle_get_color_intent(self, message):
        device = message.data.get("device")
        device_id = self.get_device_id(device)
        if device_id:
            for dev in self.devices_list:
                if dev["id"] == device_id:
                    color = dev["attributes"].get("rgb_color")
                    if color:
                        self.speak_dialog("lights.current.color",
                                          data={"color": color, "device": device})
                    else:
                        self.speak_dialog("lights.status.not.available", data={
                            "device": device, "status": "color"})

    #@intent_handler("lights.set.color.intent")
    def handle_set_color_intent(self, message):
        device = message.data.get("device")
        color = message.data.get("color")
        device_id = self.get_device_id(device)
        if device_id:
            for device in self.devices_list:
                if device["id"] == device_id:
                    brightness = device["attributes"].get("brightness")
                    break

            call_data = {
                "device_id": device_id,
                "function_name": "turn_on",
                "data": {
                    "brightness": brightness,
                    "rgb_color": color
                }
            }
            self.bus.emit(
                Message("ovos.iot.call.supported.function", call_data))
        else:
            self.speak_dialog("device.not.found", data={"device": device})

    def get_device_id(self, spoken_name):
        device_names = []

        if not self.devices_list:
            return None

        for device in self.devices_list:
            if device['attributes'].get('friendly_name'):
                device_names.append(
                    device['attributes']['friendly_name'].lower())
            else:
                device_names.append(device['name'].lower())
        spoken_name = spoken_name.lower()
        if spoken_name in device_names:
            return self.devices_list[device_names.index(spoken_name)]['id']
        else:
            fuzzy_result = self.fuzzy_match_name(spoken_name, device_names)
            return fuzzy_result if fuzzy_result else None

    def fuzzy_match_name(self, spoken_name, device_names):
        result = asyncio.run(fuzzy_match(spoken_name, device_names))
        if result:
            return self.devices_list[device_names.index(result[0])]['id']
        else:
            return None
