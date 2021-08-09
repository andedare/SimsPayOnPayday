from typing import Optional

from string import Template
from pay_on_payday_scripts.modinfo import ModLogger
from pay_on_payday_scripts.persistence.payday_data_storage import PaydaySimDataStorage
from pay_on_payday_scripts.utils.extra_time_utils import ExtraTimeUtils
from protocolbuffers import Consts_pb2
from sims.household import Household
from sims.sim_info import SimInfo
from sims4communitylib.utils.common_time_utils import CommonTimeUtils


class PaymentHandler:
    @staticmethod
    def payout_earned(household: Household):
        total_payout: int = 0
        any_household_sim: SimInfo = None
        for sim in household.get_humans_gen():
            sim_paydayinfo = PaydaySimDataStorage(sim)
            if sim_paydayinfo is not None:
                any_household_sim = sim
                total_payout += sum(sim_paydayinfo.weekday_payments.values())
                sim_paydayinfo.weekday_payments = dict()
        ModLogger.info(Template("Total to date: $total").substitute(
            total=total_payout
        ))
        if total_payout > 0:
            household.funds.add(
                total_payout,
                Consts_pb2.TELEMETRY_MONEY_CAREER,
                any_household_sim)
        elif total_payout < 0:
            household.funds.try_remove(
                total_payout,
                Consts_pb2.TELEMETRY_MONEY_CAREER,
                any_household_sim)

        return total_payout

    @staticmethod
    def withhold_salary(sim: SimInfo, day: int, pay_amount: int):
        """
        Removes <pay_amount> in simoleons from <sim> and adds to storage keyed to <day>
        :param sim: sim to withhold salary from
        :param day: day to attach salary to
        :param pay_amount:
        :return:
        """
        # Store original pay to total, return 0 if not payday else return total and zero total out
        sim.household.funds.try_remove(
            pay_amount,
            Consts_pb2.TELEMETRY_MONEY_CAREER,
            sim)
        cur_day = CommonTimeUtils.get_current_day()
        cur_day_name = ExtraTimeUtils.get_dayname_from_simday(day)
        sim_storage: Optional[PaydaySimDataStorage] = PaydaySimDataStorage(sim)
        if sim_storage is None:
            raise RuntimeError('Failed to locate a data manager for {} Sim Data')
        ModLogger.info(Template("Payday ate $money_amount simoleons for $sim_name on $day.").substitute(
            money_amount=pay_amount,
            sim_name=sim.full_name,
            day=cur_day_name
        ))
        sim_storage.add_weekday_payment(cur_day, pay_amount)

    @staticmethod
    def unpaid_backpay(household: Household, current_day: int):
        """
        Checks if <household> has any payments in storage to be considered "backpay"
        In essence, did household not receive payment over previous pay period (household missed Friday rollover)
        :param household:
        :param current_day:
        :return:
        """
        for sim in household.get_humans_gen():
            sim_paydayinfo: PaydaySimDataStorage = PaydaySimDataStorage(sim)
            if sim_paydayinfo is not None:
                # we mod 6 as we pay on Friday, so we don't care if we never care if we haven't paid Saturday's
                if len(sim_paydayinfo.weekday_payments.keys()) > 0 and\
                        (max(map(int, sim_paydayinfo.weekday_payments.keys())) % 6) > current_day:
                    return True
        return False
