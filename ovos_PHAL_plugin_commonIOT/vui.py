from ovos_workshop.app import OVOSAbstractApplication


class IOTVoiceInterface(OVOSAbstractApplication):
    def __init__(self, bus=None):
        super().__init__(skill_id="ovos.iot", bus=bus)
        # TODO - pretend this is a skill and implement intents
