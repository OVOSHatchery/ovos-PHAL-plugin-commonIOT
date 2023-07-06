from ovos_plugin_manager.utils import load_plugin, find_plugins
import enum


class PluginTypes(str, enum.Enum):
    IOT = "ovos.plugin.iot"
    IOT_DEVICE = "ovos.plugin.iot.device"


def find_iot_plugins():
    return find_plugins(PluginTypes.IOT)


def load_iot_plugin(module_name):
    """Wrapper function for loading iot plugin.
    Arguments:
        module_name (str): iot module name from config
    Returns:
        class: IOTScannerPlugin plugin class
    """
    return load_plugin(module_name, PluginTypes.IOT)
