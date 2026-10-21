"junta os modulos"

from .path import get_paths
from .connection.manage import makeConnect
import asyncio
url = get_paths()

make_connection = makeConnect(url=url)
asyncio.run(make_connection.get_engine())
asyncio.run(make_connection.get_session())