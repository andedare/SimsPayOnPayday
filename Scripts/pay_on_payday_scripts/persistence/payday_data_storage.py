from typing import Dict

from pay_on_payday_scripts.modinfo import ModInfo
from pay_on_payday_scripts.persistence.payday_data_manager import PaydaySimDataManager
from sims.sim_info import SimInfo
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.persistence.common_persisted_sim_data_storage import CommonPersistedSimDataStorage
from sims4communitylib.persistence.data_management.common_data_manager import CommonDataManager


class PaydaySimDataStorage(CommonPersistedSimDataStorage):
    def __init__(self, sim_info: SimInfo) -> None:
        self.__data_manager = None
        super().__init__(sim_info)

    @property
    def _data_manager(self) -> CommonDataManager:
        if self.__data_manager is None:
            self.__data_manager = self._data_manager_registry.locate_data_manager(ModInfo.get_identity(),
                                                                                  identifier=PaydaySimDataManager.IDENTIFIER)
            if self.__data_manager is None:
                raise RuntimeError(
                    'Failed to locate a data manager for {} Sim Data, maybe you forgot to register one?'.format(
                        self.mod_identity.name))
        return self.__data_manager

    @classmethod
    def get_mod_identity(cls) -> CommonModIdentity:
        return ModInfo.get_identity()

    @classmethod
    def get_log_identifier(cls) -> str:
        return 'payday_sim_data'

    @property
    def weekday_payments(self) -> Dict[int, int]:
        """ Simoleons earned by sim day. """
        return self.get_data(default=dict())

    @weekday_payments.setter
    def weekday_payments(self, value: Dict[int, int]):
        self.set_data(value)

    def add_weekday_payment(self, day: int, value: int):
        """ Support for adding just one day's work. """
        # noinspection PyAttributeOutsideInit
        self.weekday_payments[day] = value
