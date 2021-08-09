from typing import Tuple

from pay_on_payday_scripts.modinfo import ModInfo
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.persistence.data_management.common_data_manager import CommonDataManager
from sims4communitylib.persistence.data_management.common_data_manager_registry import CommonDataManagerRegistry
from sims4communitylib.persistence.persistence_services.common_file_persistence_service import \
    CommonFilePersistenceService
from sims4communitylib.persistence.persistence_services.common_persistence_service import CommonPersistenceService

@CommonDataManagerRegistry.common_data_manager(identifier='sim_data')
class PaydaySimDataManager(CommonDataManager):
    IDENTIFIER = 'sim_data'

    @property
    def mod_identity(self) -> CommonModIdentity:
        return ModInfo.get_identity()

    @property
    def log_identifier(self) -> str:
        return 'payday_sim_data_manager'

    @property
    def persistence_services(self) -> Tuple[CommonPersistenceService]:
        result: Tuple[CommonPersistenceService] = (CommonFilePersistenceService(per_save=True),)
        return result
