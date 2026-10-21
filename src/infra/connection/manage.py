"junta os modulos de conexão"
from .connect import Connect
from .session import get_session

class makeConnect(Connect):
    def __init__(self, url):

        super().__init__(url)

    async def get_engine(self):

        await self.run()
        


    async def get_session(self):
        self.session =  get_session(engine=self.engine)

        
        




