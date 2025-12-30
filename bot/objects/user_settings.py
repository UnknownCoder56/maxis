"""
UserSettings class for storing user preferences
"""


class UserSettings:
    def __init__(
        self, bank_dm_enabled: bool = True, bank_passive_enabled: bool = False
    ):
        self.bank_dm_enabled = bank_dm_enabled
        self.bank_passive_enabled = bank_passive_enabled
