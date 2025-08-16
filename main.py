import logging
import time
from typing import Generator

import json
import os

from dotenv import load_dotenv

from src.client import MochiClient
from src.dataclasses import Word


logging.basicConfig(level=logging.INFO)
load_dotenv()


logger = logging.getLogger(__name__)


def main() -> None:
    api_key: str = os.environ["MOCHI_API_KEY"]
    client = MochiClient(api_key)

    deck_id = client.create_deck("Arabic (Dataset)")

    words = load_dataset()
    for word in words:
        client.create_card(word, deck_id)
        time.sleep(2)

    client.close()


def load_dataset() -> Generator[Word, None, None]:
    with open("arabic.json") as f:
        words: list[dict] = json.load(f)

    yield from (Word(**word) for word in words)


if __name__ == "__main__":
    main()
