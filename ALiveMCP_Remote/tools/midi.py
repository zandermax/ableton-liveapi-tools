"""
MIDI note operations, note selection, and CC/program change.
"""

from .midi_cc import MidiCCMixin
from .midi_notes import MidiNotesMixin


class MidiMixin(MidiNotesMixin, MidiCCMixin):
    pass
