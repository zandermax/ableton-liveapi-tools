"""
Clip operations, extras, color, annotations, fades, RAM mode, and follow actions.
"""

from .clips_core import ClipsCoreMixin
from .clips_extras import ClipsExtrasMixin
from .clips_properties import ClipsPropertiesMixin


class ClipsMixin(ClipsCoreMixin, ClipsPropertiesMixin, ClipsExtrasMixin):
    pass
