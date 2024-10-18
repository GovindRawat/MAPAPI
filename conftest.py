import pytest
import logging
from framework.config import load_config
from framework.db_manager import DBManager
from framework.api_client import APIClient


# Setup logger
def setup_logger():
    logger = logging.getLogger("api_test_logger")
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler("logs/api_test.log")
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


@pytest.fixture(scope="session")
def logger():
    return setup_logger()


@pytest.fixture(scope="session")
def config():
    return load_config()


@pytest.fixture(scope="session")
def db_manager(config):
    db = DBManager(config)
    yield db
    db.close()


@pytest.fixture(scope="session")
def api_client(config):
    return APIClient(config['api']['base_url'])
