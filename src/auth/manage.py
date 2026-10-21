"junta os modulos"
from .hash import Hash
from .token import JWT
from .secret import generate_secret

class AuthManage(Hash, JWT):

    def __init__(self)-> None:

        secret = generate_secret()

        JWT.__init__(self, secret=secret)


auth = AuthManage()