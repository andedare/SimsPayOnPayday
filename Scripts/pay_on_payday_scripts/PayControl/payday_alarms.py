from string import Template

from pay_on_payday_scripts.modinfo import ModInfo, ModLogger
from pay_on_payday_scripts.persistence.payday_data_storage import PaydaySimDataStorage
from pay_on_payday_scripts.utils.common_alarm_handle import CommonAlarmHandle
from pay_on_payday_scripts.utils.common_alarm_utils import SSCommonAlarmUtils
from pay_on_payday_scripts.utils.extra_time_utils import ExtraTimeUtils
from protocolbuffers import Consts_pb2
from sims4communitylib.notifications.common_basic_notification import CommonBasicNotification
from sims4communitylib.utils.common_time_utils import CommonTimeUtils
from sims4communitylib.utils.sims.common_household_utils import CommonHouseholdUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils


class PDAlarmHandler:
    alarm_handle = None

    def create_payout_check_alarm(self) -> None:
        """ Setup the payout checker (runs each day at 5 am) """
        # we cancel the previous as household swapping might cause alarms to never trigger?
        # TODO: Find a way to fix household swapping
        if self.alarm_handle is not None:
            self.alarm_handle.cancel()
        self.alarm_handle = SSCommonAlarmUtils.schedule_daily_alarm(
            self,
            5,
            0,
            PDAlarmHandler.payout_all_earned,
            persist_across_zone_loads=True
        )

    @staticmethod
    def payout_all_earned(alarm_handle: CommonAlarmHandle) -> None:
        """ For active household, fetch and payout all earned salary checks IFF current weekday is Friday"""
        cur_day = ExtraTimeUtils.get_dayname_from_simday(CommonTimeUtils.get_day_of_week())
        ModLogger.info("Running should payout check on {}.".format(cur_day))
        if cur_day != 'Fri':
            return
        active_sim_info = CommonSimUtils.get_active_sim_info()
        active_household = CommonHouseholdUtils.get_active_household()
        total_payout = 0
        for sim in active_household.get_humans_gen():
            sim_paydayinfo = PaydaySimDataStorage(sim)
            if sim_paydayinfo is not None:
                total_payout += sum(sim_paydayinfo.weekday_payments.values())
                sim_paydayinfo.weekday_payments = dict()
        # TODO: iterate through all stored sims, group by household, then payout by household
        # currently only pays out active household, rotational play would be an issue.
        ModLogger.info(Template("Total to date: $total").substitute(
            total=total_payout
        ))
        active_household.funds.add(
            total_payout,
            Consts_pb2.TELEMETRY_MONEY_CAREER,
            active_sim_info)
        notification = CommonBasicNotification(
            "It's Payday!",
            "The {} household has earned {} this week.".format(active_household.name, total_payout)
        )
        notification.show()

# I imagine I might need to solve the case of something like "Manage Households", singleton should help me here
singleton_PDAlarmHandler = PDAlarmHandler()

