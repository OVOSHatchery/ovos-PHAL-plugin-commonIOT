from ovos_PHAL_plugin_commonIOT.opm.base import IOTCapabilties, IOTDeviceType, Plug


class MediaPlayer(Plug):
    capabilities = Plug.capabilities + [
        IOTCapabilties.PAUSE_PLAYBACK,
        IOTCapabilties.RESUME_PLAYBACK,
        IOTCapabilties.STOP_PLAYBACK,
        IOTCapabilties.NEXT_PLAYBACK,
        IOTCapabilties.PREV_PLAYBACK
    ]

    def __init__(self, device_id, host=None, name="generic_media_player",
                 area=None, device_type=IOTDeviceType.MEDIA_PLAYER, raw_data=None):
        super().__init__(device_id, host, name, area, device_type, raw_data)

    def resume(self):
        raise NotImplemented

    def stop(self):
        raise NotImplemented

    def pause(self):
        raise NotImplemented

    def play_next(self):
        raise NotImplemented

    def play_prev(self):
        raise NotImplemented


class Radio(MediaPlayer):
    def __init__(self, device_id, host=None, name="generic_radio",
                 area=None, device_type=IOTDeviceType.RADIO, raw_data=None):
        super().__init__(device_id, host, name, area, device_type, raw_data)

    # TODO - basic radio actions, change_station etc
    def resume(self):
        raise NotImplemented

    def stop(self):
        raise NotImplemented

    def pause(self):
        raise NotImplemented

    def play_next(self):
        raise NotImplemented

    def play_prev(self):
        raise NotImplemented


class TV(MediaPlayer):
    def __init__(self, device_id, host=None, name="generic_tv",
                 area=None, device_type=IOTDeviceType.TV, raw_data=None):
        super().__init__(device_id, host, name, area, device_type, raw_data)

    # TODO - basic tv actions, change_channel etc
    def resume(self):
        raise NotImplemented

    def stop(self):
        raise NotImplemented

    def pause(self):
        raise NotImplemented

    def play_next(self):
        raise NotImplemented

    def play_prev(self):
        raise NotImplemented
