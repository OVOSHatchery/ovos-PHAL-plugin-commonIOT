from ovos_workshop.app import OVOSAbstractApplication
from ovos_workshop.decorators import intent_handler
from ovos_utils.log import LOG

class IOTVoiceInterface(OVOSAbstractApplication):
    def __init__(self, bus=None):
        super().__init__(skill_id="ovos.iot", bus=bus)
        # TODO - pretend this is a skill and implement intents
        
    @intent_handler("light.get.brightness.intent")
    def light_get_brightness_intent(self, message):
        device = message.data.get("device")
        self.bus.emit("ovos.iot.device.get.brightness", {"device": device})
        
    @intent_handler("light.set.brightness.intent")
    def light_set_brightness_intent(self, message):
        device = message.data.get("device")
        amount = message.data.get("amount")
        self.bus.emit("ovos.iot.device.set.brightness", {"device": device,
                                                  "amount": amount})
        
    @intent_handler("light.decrease.brightness.intent")
    def light_decrease_brightness_intent(self, message):
        device = message.data.get("device")
        amount = message.data.get("amount", 10)
        self.bus.emit("ovos.iot.device.decrease.brightness", {"device": device,
                                                   "amount": amount})

    @intent_handler("light.increase.brightness.intent")
    def light_increase_brightness_intent(self, message):
        device = message.data.get("device")
        amount = message.data.get("amount", 10)
        self.bus.emit("ovos.iot.device.increase.brightness", {"device": device,
                                                   "amount": amount})
        
    @intent_handler("light.get.color.intent")
    def light_get_color_intent(self, message):
        device = message.data.get("device")
        self.bus.emit("ovos.iot.device.get.color", {"device": device})
        
    @intent_handler("light.set.color.intent")
    def light_set_color_intent(self, message):
        device = message.data.get("device")
        color = message.data.get("color")
        self.bus.emit("ovos.iot.device.set.color", {"device": device,
                                             "color": color})
        
