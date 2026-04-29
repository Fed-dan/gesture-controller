from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL

class VolumeController:
    def __init__(self, inc_step: int = 10, dec_step: int = 10):
        device = AudioUtilities.GetSpeakers()
        interface = device._dev.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        self.volume = cast(interface, POINTER(IAudioEndpointVolume))

        self.inc_step, self.dec_step = inc_step/100, dec_step/100

    def increase(self):
        current = self.volume.GetMasterVolumeLevelScalar()

        if current + self.inc_step < 1.0:
            self.volume.SetMasterVolumeLevelScalar(current + self.inc_step, None)

    def set_volume(self, volume: float):
        clamped = max(0.0, min(1.0, volume))
        self.volume.SetMasterVolumeLevelScalar(clamped, None)

    def decrease(self):
        current = self.volume.GetMasterVolumeLevelScalar()

        if current - self.dec_step > 0.0:
            self.volume.SetMasterVolumeLevelScalar(current - self.dec_step, None)

    def toggle_mute(self):
        self.volume.SetMute(not self.volume.GetMute(), None)