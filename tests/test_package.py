"""
Tests for core package behaviour: version format and the base logging mixin.
"""

from unittest.mock import MagicMock

from ALiveMCP_Remote import __version__
from ALiveMCP_Remote.tools.base import BaseMixin


def test_version_is_semver():
    """__version__ must be a three-part numeric semver string e.g. '1.2.3'."""
    parts = __version__.split(".")
    assert len(parts) == 3, f"Expected 3 version parts, got: {__version__!r}"
    assert all(p.isdigit() for p in parts), f"Non-numeric version part in: {__version__!r}"


def test_base_mixin_log_formats_message():
    """BaseMixin.log should prefix messages with '[LiveAPITools]' and delegate to c_instance."""
    mock_instance = MagicMock()
    mixin = BaseMixin(song=MagicMock(), c_instance=mock_instance)

    mixin.log("hello world")

    mock_instance.log_message.assert_called_once_with("[LiveAPITools] hello world")
