"testes da camada infra"
from src.infra.manage import make_connection

def test_infra() -> None:

    print(type(make_connection.session), type(make_connection.engine))




if __name__ == "__main__":
    test_infra()