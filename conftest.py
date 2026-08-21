import logging
import os

import pytest


@pytest.fixture(autouse=True)
def test_logging(request):
    test_name = request.node.name

    safe_name = test_name.replace("[", "_").replace("]", "").replace("/", "_")

    os.makedirs("logs", exist_ok=True)

    log_file = f"logs/{safe_name}.log"

    logger = logging.getLogger("framework.k8")

    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    yield

    logger.removeHandler(file_handler)
    file_handler.close()
