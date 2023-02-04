from mycroft_bus_client import Message
from os.path import join, dirname
from ovos_plugin_manager.phal import PHALPlugin
from ovos_plugin_manager.templates.iot import IOTDevicePlugin, IOTScannerPlugin, Bulb, RGBBulb, RGBWBulb
from ovos_utils.gui import GUIInterface
from ovos_utils.log import LOG
from ovos_utils import classproperty
from ovos_utils.network_utils import NetworkRequirements
from ovos_PHAL_plugin_commonIOT.device_manager import CommonIOTDeviceManager
from ovos_PHAL_plugin_commonIOT.vui import IOTVoiceInterface
from ovos_PHAL_plugin_commonIOT.gui import CommonIOTDashboard


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
        self.gui = CommonIOTDashboard(self.bus)
        self.vui = IOTVoiceInterface(self.bus)
        self.device_manager = CommonIOTDeviceManager(self.bus)

    @classproperty
    def network_requirements(self):
        """ developers should override this if they do not require connectivity
         some examples:
         IOT plugin that controls devices via LAN could return:
            scans_on_init = True
            NetworkRequirements(internet_before_load=False,
                                 network_before_load=scans_on_init,
                                 requires_internet=False,
                                 requires_network=True,
                                 no_internet_fallback=True,
                                 no_network_fallback=False)
         online search plugin with a local cache:
            has_cache = False
            NetworkRequirements(internet_before_load=not has_cache,
                                 network_before_load=not has_cache,
                                 requires_internet=True,
                                 requires_network=True,
                                 no_internet_fallback=True,
                                 no_network_fallback=True)
         a fully offline plugin:
            NetworkRequirements(internet_before_load=False,
                                 network_before_load=False,
                                 requires_internet=False,
                                 requires_network=False,
                                 no_internet_fallback=True,
                                 no_network_fallback=True)
        """
        return NetworkRequirements(internet_before_load=False,
                                   network_before_load=True,
                                   requires_internet=False,
                                   requires_network=True,
                                   no_internet_fallback=False,
                                   no_network_fallback=False)
