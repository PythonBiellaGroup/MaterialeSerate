from typing import List
from app.src.logger import logger


def logic_test(message: str = None) -> str:
    """Logic test function.

    This is a simple example how to write functions in Python

    Args:
        message (str, optional): A message you want to use. Defaults to None.

    Raises:
        Exception: If it's impossible to compose the message

    Returns:
        str: The elaborated message by the function
    """
    logger.debug("Test logic function")

    try:
        message = message.upper()
    except Exception as e:
        logger.error(f"Impossible to compose the message: {message}, because: {e}")
        logger.exception(f"Error: {e}")
        raise Exception(e)

    logger.debug(f"Message modified: {message}")

    return message


def convert_numbers(numbers: List[int]) -> int:
    """Convert and sum all elements in a list

    Args:
        numbers (List[int]): List of integers to sum

    Returns:
        int: the result of the sum
    """

    result = sum(numbers)

    return result


def name_parsing(name: str = None) -> str:
    """Ester egg spaghetti

    Args:
        name (str, optional): the name you want to pass. Defaults to None.

    Returns:
        str: the result string
    """

    if name is None:
        logger.error(f"Name: {name} not valid, please retry..")
        logger.exception("Name not valid..")

    logger.info(f"Hello: {name.strip().lower()}, welcome here!")
    logger.debug("So do you like spaghetti right?")

    return name
