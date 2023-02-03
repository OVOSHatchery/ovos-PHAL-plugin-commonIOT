from mycroft_bus_client import Message
from os.path import join, dirname
from ovos_plugin_manager.phal import PHALPlugin
from ovos_plugin_manager.templates.iot import IOTDevicePlugin, IOTScannerPlugin, Bulb, RGBBulb, RGBWBulb
from ovos_utils.gui import GUIInterface
from ovos_utils.log import LOG
from ovos_PHAL_plugin_commonIOT.device_manager import CommonIOTDeviceManager


class CommonIOTPluginValidator:
    @staticmethod
    def validate(config=None):
        """ this method is called before loading the plugin.
        If it returns False the plugin is not loaded.
        This allows a plugin to run platform checks"""
        return True


class CommonIOTPlugin(PHALPlugin):
    validator = CommonIOTPluginValidator

    def __init__(self, bus=None, config=None):
        """ Initialize the plugin
            Args:
                bus (MycroftBusClient): The Mycroft bus client
                config (dict): The plugin configuration
        """
        super().__init__(bus=bus, name="ovos-PHAL-plugin-iot", config=config)
        self.bus = bus
        self.gui = GUIInterface(bus=self.bus, skill_id=self.name)

        self.device_manager = CommonIOTDeviceManager(self.bus)
