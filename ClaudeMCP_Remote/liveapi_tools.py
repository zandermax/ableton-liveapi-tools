"""
LiveAPI Tools Implementation for ClaudeMCP Remote Script
Implements all LiveAPI operations for controlling Ableton Live

Composed from domain-specific mixin modules in the tools/ sub-package.

Author: Claude Code
License: MIT
"""

from .tools.arrangement import ArrangementMixin
from .tools.automation import AutomationMixin
from .tools.base import BaseMixin
from .tools.clips import ClipsMixin
from .tools.devices import DevicesMixin
from .tools.m4l_and_live12 import M4LAndLive12Mixin
from .tools.midi import MidiMixin
from .tools.mixing import MixingMixin
from .tools.registry import AVAILABLE_TOOLS
from .tools.scenes import ScenesMixin
from .tools.session_transport import SessionTransportMixin
from .tools.tracks import TracksMixin


class LiveAPITools(
    BaseMixin,
    SessionTransportMixin,
    TracksMixin,
    ClipsMixin,
    MidiMixin,
    DevicesMixin,
    MixingMixin,
    ScenesMixin,
    ArrangementMixin,
    AutomationMixin,
    M4LAndLive12Mixin,
):
    """
    Comprehensive implementation of LiveAPI operations.

    Composed from domain-specific mixins:
    - SessionTransportMixin: play/stop/record/tempo/transport/automation/metronome
    - TracksMixin: create/delete/arm/solo/mute/routing/groups/freeze/annotations
    - ClipsMixin: create/delete/launch/stop/looping/color/fades/follow actions
    - MidiMixin: add/remove/select notes, CC, program change
    - DevicesMixin: add/remove/parameters/racks/chains/plugin windows
    - MixingMixin: sends/master/return/crossfader/groove/quantization
    - ScenesMixin: create/delete/launch/color
    - ArrangementMixin: project/arrangement/view/loop/locator/browser/color
    - AutomationMixin: clip automation envelopes
    - M4LAndLive12Mixin: Max for Live/audio clips/take lanes/application
    """

    def get_available_tools(self):
        """Get list of all available tool names"""
        return AVAILABLE_TOOLS
