"Junta tudo"

from pathlib import Path
import os
import logging

LOG4J_PATH = Path("log4j2.properties").resolve()

os.environ["PYSPARK_SUBMIT_ARGS"] = f"--conf spark.driver.extraJavaOptions=-Dlog4j2.configurationFile={LOG4J_PATH} --conf spark.executor.extraJavaOptions=-Dlog4j2.configurationFile={LOG4J_PATH} pyspark-shell"

for name in ["py4j", "py4j.clientserver", "py4j.java_gateway"]:
    log = logging.getLogger(name)
    log.setLevel(logging.CRITICAL)
    log.propagate = False

from pyspark.sql import SparkSession, DataFrame
from .file import SparkFile
from .operation import SparkOperation
from .embendings import Embendings


class VectorUtils:

    def __init__(self):
        self.session = SparkSession.builder.appName("ClusterDb").master("local[*]").config("spark.ui.showConsoleProgress", 
                                                                                           "false").getOrCreate()
        self.session.sparkContext.setLogLevel("FATAL")

    #Retorna o objeto de SparkFile
    def file(self, instance_id:str, environment:str, cluster:str) -> SparkFile:
        path = f"data/clusters/{environment}/{cluster}/{instance_id}"
        return SparkFile(path=path, session=self.session)

    #Retorna SparkOperation
    def operation(self, df:DataFrame) -> SparkOperation:
        return SparkOperation(df=df)

    #Retorna o objeto de embendings
    def embendings(self) -> Embendings:
        return Embendings()


vector_utils = VectorUtils()