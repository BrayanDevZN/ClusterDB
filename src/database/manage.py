"junta todos os modulos de database"
from .migrate import MakeMigrate
from .control.module import TablesControl
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, AsyncEngine

class DatabaseControl(MakeMigrate, TablesControl):

    def __init__(self, engine:AsyncEngine, session:async_sessionmaker[AsyncSession])-> None:

        MakeMigrate.__init__(self,engine=engine)
        TablesControl.__init__(self,session_maker=session)
        