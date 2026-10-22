"faz as operações"

from src.logs.log import logger
from pyspark.sql import DataFrame
from pyspark.sql.types import FloatType
import pyspark.sql.functions as f
import numpy as np

from .embendings import Embendings


class SparkOperation(Embendings):

    def __init__(self, df: DataFrame) -> None:
        self.df = df
        super().__init__()


    # Cria uma coluna com a média vetorial dos embeddings
    def mean_emb(self, column: str, output_column: str = "mean") -> "SparkOperation":

        logger.info(f"Calculating mean from column {column}...")

        mean = (
            self.df
            .select(f.posexplode(f.col(column)).alias("position", "value"))
            .groupBy("position")
            .agg(f.avg("value").alias("mean"))
            .orderBy("position")
            .agg(f.collect_list("mean").alias("mean"))
            .first()["mean"]
        )

        self.df = self.df.withColumn(
            output_column,
            f.array(*[f.lit(value) for value in mean])
        )

        logger.success(f"Mean column {output_column} created successfully")

        return self


    # Cria uma coluna com cosine similarity
    def cos_column(
        self,
        column: str,
        check_emb: list[float],
        output_column: str = "similarity"
    ) -> "SparkOperation":

        logger.info(f"Calculating cosine similarity from column {column}...")

        target = np.array(check_emb, dtype=np.float32)

        @f.udf(returnType=FloatType())
        def cos_similarity(emb):

            if emb is None:
                return None

            emb = np.array(emb, dtype=np.float32)

            denominator = np.linalg.norm(emb) * np.linalg.norm(target)

            if denominator == 0:
                return 0.0

            return float(np.dot(emb, target) / denominator)

        self.df = self.df.withColumn(
            output_column,
            cos_similarity(f.col(column))
        )

        logger.success(f"Similarity column {output_column} created successfully")

        return self


    # Retorna o maior valor de uma coluna
    def max_column(self, column: str):

        logger.info(f"Getting max value from column {column}...")

        value = self.df.select(
            f.max(f.col(column))
        ).first()[0]

        logger.success(f"Max value from column {column} obtained successfully")

        return value


    # Retorna o DataFrame atual
    def get_df(self) -> DataFrame:

        return self.df