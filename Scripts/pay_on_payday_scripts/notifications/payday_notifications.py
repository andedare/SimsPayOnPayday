import sims4.log

from pay_on_payday_scripts.modinfo import ModInfo
from sims4communitylib.notifications.common_basic_notification import CommonBasicNotification

logger = sims4.log.Logger('Payday')


class PayDayNotifications:
    """
        A class that holds all mod's notifications.
        This is allows consolidation of visible text towards potential I18N/L10N.
    """

    @staticmethod
    def notify_payday(household_name: str, payout: int) -> None:
        ModInfo.info("Payday has been announced.")
        notification = CommonBasicNotification(
            "It's Payday!",
            "The {} household has earned {} this week.".format(household_name, payout)
        )
        notification.show()
