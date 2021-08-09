from typing import Dict, Any

from pay_on_payday_scripts.persistence.payday_data_manager import PaydaySimDataManager
from pay_on_payday_scripts.modinfo import ModInfo
from sims4.commands import CommandType, CheatOutput, Command
from sims4communitylib.persistence.data_management.common_data_manager_registry import CommonDataManagerRegistry
from sims4communitylib.services.common_service import CommonService
from sims4communitylib.utils.common_log_registry import CommonLogRegistry


class PaydaySimDataManagerUtils(CommonService):
    """ Utilities for accessing Sim data stores """
    def __init__(self) -> None:
        self._data_manager: PaydaySimDataManager = None

    @property
    def data_manager(self) -> PaydaySimDataManager:
        """ The data manager containing data. """
        if self._data_manager is None:
            # noinspection PyTypeChecker
            self._data_manager: PaydaySimDataManager = CommonDataManagerRegistry().locate_data_manager(ModInfo.get_identity(),
                                                                                                       identifier=PaydaySimDataManager.IDENTIFIER)
        return self._data_manager

    def get_all_data(self) -> Dict[str, Dict[str, Any]]:
        """ Get all data. """
        return self.data_manager._data_store_data

    def save(self) -> bool:
        """ Save data. """
        return self.data_manager.save()

    def reset(self, prevent_save: bool=False) -> bool:
        """ Reset data. """
        return self.data_manager.remove_all_data(prevent_save=prevent_save)


log = CommonLogRegistry().register_log(ModInfo.get_identity(), 'pop.print_mod_sim_data')


@Command('pop.print_mod_sim_data', command_type=CommandType.Live)
def _pop_command_print_mod_sim_data(_connection: int=None):
    output = CheatOutput(_connection)
    output('Printing Payday Mod Sim Data to Messages.txt file. This may take a little bit, be patient.')
    log.enable()
    log.format(data_store_data=PaydaySimDataManagerUtils().get_all_data())
    log.disable()
    output('Done')

