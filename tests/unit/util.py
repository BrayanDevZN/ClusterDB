"Teste de utils"

from src.utils.manage import vector_utils
import asyncio


async def test_util() -> None:

    print("\n=== EMBENDINGS ===")

    emb_utils = vector_utils.embendings()

    emb1 = await emb_utils.encode("Eu gosto de Python")
    emb2 = await emb_utils.encode("Eu gosto de programar")
    emb3 = await emb_utils.encode("Hoje eu comi sushi")

    print(f"Embedding size: {len(emb1)}")

    assert len(emb1) == 384
    assert len(emb2) == 384
    assert len(emb3) == 384


    print("\n=== COSINE SIMILARITY ===")

    similarity = await emb_utils.cos(emb1, emb2)

    print(f"Similarity: {similarity}")

    assert isinstance(similarity, float)
    assert -1.0 <= similarity <= 1.0


    print("\n=== CREATE DATAFRAME ===")

    data = [
        ("python", emb1.tolist()),
        ("programming", emb2.tolist()),
        ("sushi", emb3.tolist())
    ]

    df = vector_utils.session.createDataFrame(data, ["text", "embedding"])

    df.show()

    assert df.count() == 3
    assert "text" in df.columns
    assert "embedding" in df.columns


    print("\n=== SPARK OPERATIONS ===")

    operation = vector_utils.operation(df)

    operation.mean_emb("embedding")
    operation.cos_column("embedding", emb1.tolist())

    result_df = operation.get_df()

    result_df.show()

    assert "mean" in result_df.columns
    assert "similarity" in result_df.columns


    print("\n=== CHECK MEAN ===")

    mean = result_df.select("mean").first()["mean"]

    print(f"Mean size: {len(mean)}")
    print(f"First mean values: {mean[:5]}")

    assert mean is not None
    assert len(mean) == 384


    print("\n=== CHECK SIMILARITY ===")

    rows = result_df.select("text", "similarity").collect()

    for row in rows:
        print(f"{row['text']} -> {row['similarity']}")

    assert len(rows) == 3

    for row in rows:
        assert row["similarity"] is not None
        assert -1.0 <= row["similarity"] <= 1.0


    print("\n=== MAX SIMILARITY ===")

    max_similarity = operation.max_column("similarity")

    print(f"Max similarity: {max_similarity}")

    assert max_similarity is not None
    assert isinstance(max_similarity, float)
    assert max_similarity > 0.99


    print("\n=== CHAIN OPERATIONS ===")

    chained_df = vector_utils.operation(df).mean_emb("embedding", "embedding_mean").cos_column("embedding", emb2.tolist(), "cos_similarity").get_df()

    chained_df.show()

    assert "embedding_mean" in chained_df.columns
    assert "cos_similarity" in chained_df.columns

    chained_max = vector_utils.operation(chained_df).max_column("cos_similarity")

    print(f"Chained max similarity: {chained_max}")

    assert chained_max is not None
    assert chained_max > 0.99


    print("\n=== SPARK FILE ===")

    file1 = vector_utils.file(instance_id="instance_1", environment="test", cluster="test_cluster")
    file2 = vector_utils.file(instance_id="instance_2", environment="test", cluster="test_cluster")
    file3 = vector_utils.file(instance_id="instance_3", environment="test", cluster="test_cluster")

    if file1.BASE_DIR.parent.exists():
        await file1.drop_cluster()

    assert await file1.exists() is False


    print("\n=== WRITE PARQUET ===")

    await file1.write(df)

    assert await file1.exists() is True

    print("Parquet saved successfully")


    print("\n=== READ PARQUET ===")

    loaded_df = await file1.read()

    assert loaded_df is not None
    assert loaded_df.count() == 3
    assert "text" in loaded_df.columns
    assert "embedding" in loaded_df.columns

    loaded_df.show()

    loaded_texts = {row["text"] for row in loaded_df.select("text").collect()}

    assert loaded_texts == {"python", "programming", "sushi"}

    print("Parquet read successfully")


    print("\n=== DROP SINGLE INSTANCE ===")

    await file1.drop_instances()

    assert await file1.exists() is False

    print("Single instance deleted successfully")


    print("\n=== CREATE MULTIPLE INSTANCES ===")

    await file1.write(df)
    await file2.write(df)
    await file3.write(df)

    assert await file1.exists() is True
    assert await file2.exists() is True
    assert await file3.exists() is True

    print("Multiple instances created successfully")


    print("\n=== DROP ALL INSTANCES ===")

    await file1.drop_instances(rm_all=True)

    assert await file1.exists() is False
    assert await file2.exists() is False
    assert await file3.exists() is False
    assert file1.BASE_DIR.parent.exists() is True

    print("All instances deleted successfully")
    print("Cluster directory preserved successfully")


    print("\n=== DROP CLUSTER ===")

    await file1.write(df)
    await file2.write(df)

    assert await file1.exists() is True
    assert await file2.exists() is True
    assert file1.BASE_DIR.parent.exists() is True

    await file1.drop_cluster()

    assert file1.BASE_DIR.parent.exists() is False
    assert await file1.exists() is False
    assert await file2.exists() is False

    print("Cluster deleted successfully")


    print("\n=== GET DF ===")

    operation = vector_utils.operation(df)

    returned_df = operation.get_df()

    assert returned_df is df

    print("DataFrame returned successfully")


    print("\n=== UTILS TEST FINISHED SUCCESSFULLY ===")


if __name__ == "__main__":
    asyncio.run(test_util())