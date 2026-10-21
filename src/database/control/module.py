"junta todos os modulos de control"
from src.database.control.users import UserControl
from src.database.control.keys import KeyControl
from src.database.control.clusters import ClusterControl
from src.database.control.instances import InstanceControl

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker


class TablesControl(UserControl, KeyControl, ClusterControl, InstanceControl):

    def __init__(self, session_maker: async_sessionmaker[AsyncSession]) -> None:

        self.users = UserControl(session_maker=session_maker)
        self.keys = KeyControl(session_maker=session_maker)
        self.clusters = ClusterControl(session_maker=session_maker)
        self.instances = InstanceControl(session_maker=session_maker)
        