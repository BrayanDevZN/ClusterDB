"teste do banco"

from src.database.manage import DatabaseControl
from src.infra.manage import make_connection
import asyncio


async def test_table() -> None:

    control_db = DatabaseControl(
        engine=make_connection.engine,
        session=make_connection.session
    )


    print("\n=== CREATE TABLES ===")

    print(await control_db.create_tables())


    print("\n=== USERS ===")

    user = await control_db.users.create(
        user_name="brayan",
        email="brayan@email.com",
        password="123456",
        role="admin"
    )
    print(user)

    user_id = user["id"]
    user_public_id = user["public_id"]

    print(await control_db.users.get_by_id(user_id))
    print(await control_db.users.get_by_public_id(user_public_id))
    print(await control_db.users.get_by_username("brayan"))
    print(await control_db.users.get_by_email("brayan@email.com"))
    print(await control_db.users.get_all())

    print(await control_db.users.update(
        user_id,
        user_name="brayan_updated"
    ))


    print("\n=== KEYS ===")

    key = await control_db.keys.create(
        user_id=user_id,
        permission_db="all",
        permission_actions="all",
        environment="test"
    )
    print(key)

    key_id = key["id"]
    key_value = key["key"]

    print(await control_db.keys.get_by_id(key_id))
    print(await control_db.keys.get_by_key(key_value))
    print(await control_db.keys.get_by_user_id(user_id))
    print(await control_db.keys.get_by_environment("test"))
    print(await control_db.keys.get_all())

    print(await control_db.keys.update(
        key_id,
        environment="develop"
    ))


    print("\n=== CLUSTERS ===")

    cluster = await control_db.clusters.create(
        cluster_name="test_cluster",
        instance_limit=10,
        created_key=key_id
    )
    print(cluster)

    cluster_id = cluster["id"]
    cluster_public_id = cluster["public_id"]

    print(await control_db.clusters.get_by_id(cluster_id))
    print(await control_db.clusters.get_by_public_id(cluster_public_id))
    print(await control_db.clusters.get_by_name("test_cluster"))
    print(await control_db.clusters.get_by_created_key(key_id))
    print(await control_db.clusters.get_all())

    print(await control_db.clusters.update(
        cluster_id,
        instance_limit=20
    ))


    print("\n=== INSTANCES ===")

    instance = await control_db.instances.create(
        cluster_id=cluster_id
    )
    print(instance)

    instance_id = instance["id"]


    print("\n=== CREATE CENTRAL ===")

    mean = [0.12, 0.34, 0.56, 0.78]

    central = await control_db.instances.create_central(
        instance_id=instance_id,
        mean=mean
    )
    print(central)


    print("\n=== GET INSTANCES WITH MEAN ===")

    print(await control_db.instances.get_by_id(instance_id))
    print(await control_db.instances.get_by_cluster_id(cluster_id))
    print(await control_db.instances.get_all())


    print("\n=== UPDATE INSTANCE ===")

    print(await control_db.instances.update(
        instance_id,
        cluster_id=cluster_id
    ))


    print("\n=== UPDATE MEAN ===")

    new_mean = [0.20, 0.40, 0.60, 0.80]

    print(await control_db.instances.update(
        instance_id,
        mean=new_mean
    ))


    print("\n=== GET UPDATED INSTANCE ===")

    updated_instance = await control_db.instances.get_by_id(instance_id)
    print(updated_instance)

    assert updated_instance is not None
    assert updated_instance["mean"] == new_mean


    print("\n=== DELETE RECORDS ===")

    print(await control_db.instances.delete(instance_id))
    print(await control_db.clusters.delete(cluster_id))
    print(await control_db.keys.delete(key_id))
    print(await control_db.users.delete(user_id))


    print("\n=== DELETE TABLES ===")

    print(await control_db.delete_tables())


if __name__ == "__main__":
    asyncio.run(test_table())