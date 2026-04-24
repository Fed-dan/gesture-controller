from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL

class VolumeController:
    def __init__(self):
        device = AudioUtilities.GetSpeakers()
        interface = device._dev.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        self.volume = cast(interface, POINTER(IAudioEndpointVolume))
    def increase(self, step: float = 0.1):
        current = self.volume.GetMasterVolumeLevelScalar()

        if current + step < 1.0:
            self.volume.SetMasterVolumeLevelScalar(current + step, None)

    def decrease(self, step: float = 0.1):
        current = self.volume.GetMasterVolumeLevelScalar()

        if current - step > 0.0:
            self.volume.SetMasterVolumeLevelScalar(current - step, None)

    def toggle_mute(self):
        self.volume.SetMute(not self.volume.GetMute(), None)