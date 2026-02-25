"""
Device operations, parameters, racks/chains, plugin windows, and utilities.
"""

from .devices_core import DevicesCoreMixin
from .devices_racks import DevicesRacksMixin


class DevicesMixin(DevicesCoreMixin, DevicesRacksMixin):
    pass
