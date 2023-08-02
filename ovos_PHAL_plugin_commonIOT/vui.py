from ovos_workshop.app import OVOSAbstractApplication
from ovos_workshop.decorators import intent_handler
from ovos_bus_client import Message
from ovos_utils.log import LOG

class IOTVoiceInterface(OVOSAbstractApplication):
    def __init__(self, bus=None):
        super().__init__(skill_id="ovos.iot", bus=bus)
        # TODO - pretend this is a skill and implement intents

    @intent_handler("light.get.brightness.intent")
    def light_get_brightness_intent(self, message):
        device = message.data.get("device")
        response = self.bus.wait_for_response(Message("ovos.iot.device.get.brightness", data={"device": device}))
        if not response:
            self.speak_dialog("device.not.found.dialog", data={"device": message.data.device.get("name", "unknown")})
        else:
            self.speak_dialog("light.current.brightness.dialog", data={"device": message.data.device.get("name")},
                                                                       "brightness": response.data.get("brightness")})
    @intent_handler("light.set.brightness.intent")
    def light_set_brightness_intent(self, message):
        device = message.data.get("device")
        brightness = message.data.get("brightness")
        response = self.bus.wait_for_response(Message("ovos.iot.device.set.brightness", data={"device": device,
                                                                                 "brightness": brightness}))
        if not response:
            self.speak_dialog("device.not.found.dialog", data="device": device.get("name", "unknown"))
        elif isinstance(response.brightness, Exception):
            self.speak_dialog("light.set.brightness.error.dialog", data={"device": device.get("name", "unknown")})
        else:
            self.speak_dialog("light.set.brightness.dialog", data={"device": device.get("name"),
                                                                       "brightness": response.brightness})

    @intent_handler("light.decrease.brightness.intent")
    def light_decrease_brightness_intent(self, message):
        device = message.get("device")
        amount = message.get("amount", 10)
        response = self.bus.wait_for_response(Message("ovos.iot.device.decrease.brightness", data={"device": device,
                                                                                      "amount": amount}))
        if not response:
            self.speak_dialog("device.not.found.dialog", data="device": device.get("name", "unknown"))
        elif isinstance(response.brightness, Exception):
            self.speak_dialog("light.set.brightness.error.dialog", data={"device": device.get("name", "unknown")})
        else:
            self.speak_dialog("light.set.brightness.dialog", data={"device": device.get("name"),
                                                                       "brightness": response.brightness})

    @intent_handler("light.increase.brightness.intent")
    def light_increase_brightness_intent(self, message):
        device = message.get("device")
        amount = message.get("amount", 10)
        response = self.bus.wait_for_response(Message("ovos.iot.device.increase.brightness", data={"device": device,
                                                                                      "amount": amount}))
        if not response:
            self.speak_dialog("device.not.found.dialog", data="device": device.get("name", "unknown"))
        elif isinstance(response.brightness, Exception):
            self.speak_dialog("light.set.brightness.error.dialog", data={"device": device.get("name", "unknown")})
        else:
            self.speak_dialog("light.set.brightness.dialog", data={"device": device.get("name"),
                                                                       "brightness": response.brightness})

    @intent_handler("light.get.color.intent")
    def light_get_color_intent(self, message):
        device = message.get("device")
        response = self.bus.wait_for_response(Message("ovos.iot.device.get.color", data={"device": device}))
        if not response:
            self.speak_dialog("device.not.found.dialog", data={"device": device.get("name", "unknown")})
        else:
            self.speak_dialog("light.current.color.dialog", data={"device": device.get("name"), "color": response.color})

    @intent_handler("light.set.color.intent")
    def light_set_color_intent(self, message):
        device = message.get("device")
        color = message.get("color")
        response = self.bus.wait_for_response(Message("ovos.iot.device.set.color", data={"device": device,
                                                                            "color": color}))
        if not response:
            self.speak_dialog("device.not.found.dialog", data="device": device.get("name", "unknown"))
        elif isinstance(response.color, Exception):
            self.speak_dialog("light.set.color.error.dialog", data={"device": device.get("name", "unknown")})
        else:
            self.speak_dialog("light.set.color.dialog", data={"device": device.get("name"),
                                                                       "color": response.color})

