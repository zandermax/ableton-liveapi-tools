"""
Base mixin providing shared state and helpers for all LiveAPI tool mixins.
"""


class BaseMixin(object):
    """
    Provides __init__ and logging used by all other mixins.
    Must appear first in the MRO so self.song and self.c_instance
    are available to every mixin method.
    """

    def __init__(self, song, c_instance):
        self.song = song
        self.c_instance = c_instance

    def log(self, message):
        """Log message to Ableton's Log.txt"""
        self.c_instance.log_message("[LiveAPITools] " + str(message))
