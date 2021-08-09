from pay_on_payday_scripts.modinfo import ModInfo, ModLogger
from sims4communitylib.notifications.common_basic_notification import CommonBasicNotification


class PaydayNotifications:
    """
        A class that holds all mod's notifications.
        This is allows consolidation of visible text towards potential I18N/L10N.
    """

    @staticmethod
    def notify_payday(household_name: str, payout: int) -> None:
        ModLogger.info("Payday has been announced.")
        notification = CommonBasicNotification(
            "It's Payday!",
            "The {} household has earned {} this week.".format(household_name, payout)
        )
        notification.show()

    @staticmethod
    def notify_backpay(household_name: str, payout: int) -> None:
        ModLogger.info("Backpay has been announced.")
        notification = CommonBasicNotification(
            "Bank has rewarded salary back pay",
            "The {} household earned {} last pay period.".format(household_name, payout)
        )
        notification.show()
