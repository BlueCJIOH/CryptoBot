import logging
import os
from typing import Final


class Env:
    try:
        BOT_TOKEN: Final = os.environ["BOT_TOKEN"]
    except KeyError as err:
        logging.warning(f"Set a valid {err} variable in the environment file!")