import sims4
from sims4.log import Logger
from sims4communitylib.mod_support.common_mod_info import CommonModInfo

# TODO: this should be a member, but I'm not willing to figure that out at the moment
ModLogger = sims4.log.Logger('pay_on_payday')


class ModInfo(CommonModInfo):
    """ Career Pay on Payday. """
    # To create a Mod Identity for this mod, simply do ModInfo.get_identity().
    # Please refrain from using the ModInfo of The Sims 4 Community Library in your own mod and instead use yours!
    _FILE_PATH: str = str(__file__)

    def __init__(self):
        super().__init__()

    @property
    def _name(self) -> str:
        # This is the name that'll be used whenever a Messages.txt or Exceptions.txt file is created
        # <_name>_Messages.txt and <_name>_Exceptions.txt.
        return 'pay_on_payday'

    @property
    def _author(self) -> str:
        return 'Andedare'

    @property
    def _base_namespace(self) -> str:
        # This is the name of the root package
        return 'pay_on_payday_scripts'

    @property
    def _file_path(self) -> str:
        # This is simply a file path that you do not need to change.
        return ModInfo._FILE_PATH

