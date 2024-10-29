from pyspark.sql import SparkSession

# Specify the log4j configuration file
log4j_conf_path = "file:///C:/Users/AakashMahawar/PycharmProject/pepper_advantage/pyspark_project/sbdl/log4j.properties"

def get_spark_session(env):
    if env == "LOCAL":
        return SparkSession.builder \
            .config("spark.driver.extraJavaOptions", f"-Dlog4j.configuration={log4j_conf_path}") \
            .master("local[2]") \
            .enableHiveSupport() \
            .getOrCreate()
    else:
        return SparkSession.builder \
            .enableHiveSupport() \
            .getOrCreate()

