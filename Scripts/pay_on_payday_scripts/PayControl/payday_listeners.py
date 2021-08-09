from typing import Optional, Any, Tuple

import services
from careers.career_base import CareerBase
from pay_on_payday_scripts.PayControl.payday_alarms import singleton_PDAlarmHandler
from pay_on_payday_scripts.persistence.payday_data_storage import PaydaySimDataStorage
from pay_on_payday_scripts.modinfo import ModInfo, ModLogger
from pay_on_payday_scripts.utils.extra_time_utils import ExtraTimeUtils
from sims4communitylib.events.event_handling.common_event_registry import CommonEventRegistry
from sims4communitylib.events.zone_spin.events.zone_late_load import S4CLZoneLateLoadEvent
from sims4communitylib.utils.common_injection_utils import CommonInjectionUtils
from string import Template

from sims4communitylib.utils.common_time_utils import CommonTimeUtils

"""
Logic:

1. Search if there is already a valid romance; ignore
2. Search if there is available romance ( has_positive_romantic_combo_relationship_bit_with, :
    * if relationship high enough, trigger relationship bit
3. otherwise,
    * search change relationship up/down 
"""


class PaydayListeners:
    # ignore daily pay
    @staticmethod
    @CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), CareerBase, CareerBase._collect_rewards.__name__)
    def _pd_collect_rewards(original, *_args, **_kwargs) -> Tuple[float, Any]:
        """
            Listens for Career rewards, undoes the simoleon earnings and stores them on the sim for future payment
            NOTE: This only accounts for salary payments, promotion payments are separately handled.
        """
        from protocolbuffers import Consts_pb2
        (original_pay, pto_delta) = original(*_args, **_kwargs)
        # Store original pay to total, return 0 if not payday else return total and zero total out
        orig_self = _args[0]
        orig_self._sim_info.household.funds.try_remove(
            original_pay,
            Consts_pb2.TELEMETRY_MONEY_CAREER,
            orig_self._get_sim())
        cur_day = CommonTimeUtils.get_current_day()
        cur_day_name = ExtraTimeUtils.get_dayname_from_simday(CommonTimeUtils.get_current_day())
        sim_info = orig_self._sim_info
        sim_storage: Optional[PaydaySimDataStorage] = PaydaySimDataStorage(sim_info)
        if sim_storage is None:
            raise RuntimeError('Failed to locate a data manager for {} Sim Data')
        ModLogger.info(Template("Payday ate $money_amount simoleons for $sim_name on $day.").substitute(
            money_amount=original_pay,
            sim_name=sim_info.full_name,
            day=cur_day_name
        ))
        sim_storage.add_weekday_payment(cur_day, original_pay)

        return (original_pay, pto_delta)

    @staticmethod
    @CommonEventRegistry.handle_events(ModInfo.get_identity())
    def _show_loaded_notification_when_loaded(event_data: S4CLZoneLateLoadEvent):
        ModLogger.info("successfully loaded.")
        singleton_PDAlarmHandler.create_payout_check_alarm()
