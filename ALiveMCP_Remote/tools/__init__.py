"""
Domain-specific mixin modules that implement the 220 LiveAPI tools.

Each mixin class provides methods for a related group of operations.
LiveAPITools (in liveapi_tools.py) composes them all via multiple inheritance.

Mixin hierarchy (top-level composites → leaf implementations):
  SessionTransportMixin  ← SessionAutomationMixin
  TracksMixin            ← TracksCoreMixin, TracksRoutingMixin, TracksAdvancedMixin
  ClipsMixin             ← ClipsCoreMixin, ClipsPropertiesMixin, ClipsExtrasMixin
  MidiMixin              ← MidiNotesMixin, MidiCCMixin
  DevicesMixin           ← DevicesCoreMixin, DevicesRacksMixin
  MixingMixin            ← MixingGrooveMixin
  ScenesMixin
  ArrangementMixin       ← ArrangementBrowserMixin
  AutomationMixin
  M4LAndLive12Mixin      ← M4LDevicesMixin, M4LAudioMixin,
                           Live12LanesMixin, Live12PropertiesMixin

All mixins inherit BaseMixin (via LiveAPITools) which provides
self.song, self.c_instance, and log().
"""
