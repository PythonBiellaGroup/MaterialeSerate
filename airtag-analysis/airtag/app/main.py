from app.src.logger import logger
from app.src.config import APP_NAME
from app.src.core.manager import logic_test, convert_numbers

if __name__ == "__main__":
    logger.info(f"Welcome to: {APP_NAME}")

    message = "Ciao!"
    numbers = [1, 2, 3, 4, 5, 6]

    new_message = logic_test(message)
    result = convert_numbers(numbers)
    logger.info(f"Message: {new_message}, with numbers: {numbers}")
