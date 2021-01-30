from pyaudio import PyAudio


class SounderDevices(PyAudio):
    """ Display recording devices """

    def __init__(self, *args, **kwargs):
        super().__init__()

    def getdevices(self):
        """ Get all devices available for recording. """
        api_count = self.get_host_api_count();
        output = {}
        # iterate over the apis
        for i in range(api_count):
            info = self.get_host_api_info_by_index(i)
            numdevices = info.get('deviceCount')
            devices = {}
            for d in range(numdevices):
                if (self.get_device_info_by_host_api_device_index(i, d).get('maxInputChannels')) > 0:
                    device_name = self.get_device_info_by_host_api_device_index(i, d).get('name')
                    devices[device_name] = d

            output[f"{i}"] = devices

        return output