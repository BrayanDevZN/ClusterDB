"teste de auth"

from src.auth.manage import auth
import asyncio


async def test_auth() -> None:

    print("\n=== HASH ===")

    password = "123456"

    hashed_password = await auth.encode(password=password)
    print("Hash:", hashed_password)

    valid_password = await auth.check(
        password=password,
        hashed_password=hashed_password
    )
    print("Valid password:", valid_password)

    invalid_password = await auth.check(
        password="senha_errada",
        hashed_password=hashed_password
    )
    print("Invalid password:", invalid_password)


    print("\n=== JWT ===")

    payload = {
        "user_id": 1,
        "user_name": "brayan",
        "role": "admin"
    }

    token = await auth.generate(payload=payload)
    print("Token:", token)

    decoded = await auth.decode(token=token)
    print("Decoded:", decoded)


if __name__ == "__main__":
    asyncio.run(test_auth())