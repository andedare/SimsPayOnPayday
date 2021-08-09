from typing import Any, Tuple

from careers.career_base import CareerBase
from pay_on_payday_scripts.PayControl.payday_alarms import singleton_PDAlarmHandler
from pay_on_payday_scripts.PayControl.payment_handler import PaymentHandler
from pay_on_payday_scripts.notifications.payday_notifications import PaydayNotifications
from pay_on_payday_scripts.modinfo import ModInfo, ModLogger
from sims4communitylib.events.event_handling.common_event_registry import CommonEventRegistry
from sims4communitylib.events.zone_spin.events.zone_late_load import S4CLZoneLateLoadEvent
from sims4communitylib.utils.common_injection_utils import CommonInjectionUtils

from sims4communitylib.utils.common_time_utils import CommonTimeUtils
from sims4communitylib.utils.sims.common_household_utils import CommonHouseholdUtils


class PaydayListeners:
    # ignore daily pay
    @staticmethod
    @CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), CareerBase, CareerBase._collect_rewards.__name__)
    def _pd_collect_rewards(original, *_args, **_kwargs) -> Tuple[float, Any]:
        """
            Listens for Career rewards, undoes the simoleon earnings and stores them on the sim for future payment
            NOTE: This only accounts for salary payments, promotion payments are separately handled.
        """
        ModLogger.info("Salary event was captured. Attempting to clear earnings.")
        from protocolbuffers import Consts_pb2
        (original_pay, pto_delta) = original(*_args, **_kwargs)
        # Store original pay to total, return 0 if not payday else return total and zero total out
        orig_self = _args[0]
        PaymentHandler.withhold_salary(orig_self._get_sim(), CommonTimeUtils.get_current_day(), original_pay)
        return (original_pay, pto_delta)

    @staticmethod
    @CommonEventRegistry.handle_events(ModInfo.get_identity())
    def _show_loaded_notification_when_loaded(event_data: S4CLZoneLateLoadEvent):
        ModLogger.info("successfully loaded.")
        PaydayListeners._pay_unpaid_backpay()
        singleton_PDAlarmHandler.create_payout_check_alarm()

    @staticmethod
    def _pay_unpaid_backpay():
        weekday = CommonTimeUtils.get_day_of_week()
        active_household = CommonHouseholdUtils.get_active_household()
        if PaymentHandler.unpaid_backpay(active_household, weekday):
            reward = PaymentHandler.payout_earned(active_household)
            PaydayNotifications.notify_backpay(active_household.name, reward)