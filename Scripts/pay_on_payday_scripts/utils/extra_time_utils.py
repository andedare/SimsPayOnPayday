DAY_NAMES = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']


class ExtraTimeUtils:
    """
        Just a couple silly functions for fetching days actual string names.
        Will obviously collapse on I18N. (There *should* be string table entries, but I'm too lazy to look for them
        at the moment.)
    """
    @staticmethod
    def get_dayname_from_weekday(weekday: int) -> str:
        return DAY_NAMES[weekday]

    @staticmethod
    def get_dayname_from_simday(simday: int) -> str:
        return DAY_NAMES[simday % 7]

    @staticmethod
    def get_dayname_from_weekday_localized(weekday: int) -> str:
        raise RuntimeError("Localization not implemented.")

    @staticmethod
    def get_dayname_from_simday_localized(simday: int) -> str:
        raise RuntimeError("Localization not implemented.")
