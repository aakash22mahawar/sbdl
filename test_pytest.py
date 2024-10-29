import pytest
from lib.utils import get_spark_session


# Fixture to create a Spark session
@pytest.fixture(scope='session')
def spark():
    return get_spark_session("LOCAL")


def test_spark_version(spark):
    # Get the Spark version
    spark_version = spark.version
    print(f"Spark version: {spark_version}")

    # Assert the version (replace '3.5.1' with your expected version)
    assert spark_version == "3.5.1"
