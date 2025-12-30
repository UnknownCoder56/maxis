"""
Command handlers for Maxis
"""

from typing import TYPE_CHECKING

# Imports are intentionally omitted at runtime to avoid circular imports with bot.main.
# They are only imported for type checkers so __all__ remains accurate for tooling.
if TYPE_CHECKING:  # pragma: no cover
    from bot.commands import basic_commands, currency_commands, mod_commands

__all__ = ["basic_commands", "currency_commands", "mod_commands"]
