from typing import List
from app.src.logger import logger
from app.src.core.manager import logic_test, convert_numbers
import pytest


@pytest.mark.functions
def test_logic_base():

    logger.debug("test logic base con messaggio")
    message = "Ciao!"
    message = logic_test(message)
    assert message == "CIAO!"


@pytest.mark.core
def test_entities():

    logger.debug("test entities base con lista di numeri")
    numbers = [1, 2, 3, 4, 5]
    result = convert_numbers(numbers)
    assert result is List
    assert result == [25]


if __name__ == "__main__":
    logger.info("test di esempio")

    test_logic_base()
    test_entities()
