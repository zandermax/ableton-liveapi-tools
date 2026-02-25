"""
Max for Live, audio clips, sample/simpler, take lanes, application methods,
and miscellaneous track/clip/scene property operations.
"""

from .live12_lanes import Live12LanesMixin
from .live12_properties import Live12PropertiesMixin
from .m4l_audio import M4LAudioMixin
from .m4l_devices import M4LDevicesMixin


class M4LAndLive12Mixin(M4LDevicesMixin, M4LAudioMixin, Live12LanesMixin, Live12PropertiesMixin):
    pass
