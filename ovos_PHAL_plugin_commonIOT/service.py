from ovos_utils import classproperty
from ovos_utils.process_utils import RuntimeRequirements

from ovos_PHAL_plugin_commonIOT.device_manager import CommonIOTDeviceManager
from ovos_PHAL_plugin_commonIOT.vui import IOTVoiceInterface
from ovos_plugin_manager.phal import PHALPlugin


class CommonIOTPluginValidator:
    @staticmethod
    def validate(config=None):
        """ this method is called before loading the plugin.
        If it returns False the plugin is not loaded.
        This allows a plugin to run platform checks"""
        return True


class CommonIOTService(PHALPlugin):
    validator = CommonIOTPluginValidator

    def __init__(self, bus=None, config=None):
        """ Initialize the plugin
            Args:
                bus (MycroftBusClient): The Mycroft bus client
                config (dict): The plugin configuration
        """
        super().__init__(bus=bus, name="ovos-PHAL-plugin-iot", config=config)
        self.bus = bus
        self.vui = IOTVoiceInterface(self.bus)
        self.device_manager = CommonIOTDeviceManager(self.bus)
        self.device_manager.load_scanners()

    @classproperty
    def runtime_requirements(self):
        return RuntimeRequirements(internet_before_load=False,
                                   network_before_load=True,
                                   requires_internet=False,
                                   requires_network=True,
                                   no_internet_fallback=False,
                                   no_network_fallback=False)
