import os
from mycroft_bus_client import Message
from ovos_plugin_manager.phal import PHALPlugin


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
        super().__init__(bus=bus, name="ovos-PHAL-plugin-commonIOT", config=config)
        self.port = config.get("port", 36536)

        self.bus.on("iot.register", self.handle_commonIOT_register)

        # trigger register events from commonIOT skills
        self.bus.emit(Message("iot.ping"))

        self.commonIOT_skills = {}

    def handle_commonIOT_register(self, message):
        skill_id = message.data.get("skill_id")
        # TODO - allow skills to provide devices via bus api

    def shutdown(self):
        self.bus.remove("commonIOT.register", self.handle_commonIOT_register)
        super().shutdown()
