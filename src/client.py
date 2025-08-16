import logging
import os

import httpx

from src.dataclasses import Word


MOCHI_API_KEY: str = os.environ["MOCHI_API_KEY"]
MOCHI_TEMPLATE_ID = "2bjhxPxY"

logger = logging.getLogger(__name__)


class MochiClient:
    BASE_URL = "https://app.mochi.cards/api/"

    def __init__(self, api_key: str) -> None:
        self.api_key = api_key

        auth = httpx.BasicAuth(username=self.api_key, password="")

        self._client = httpx.Client(
            base_url=self.BASE_URL,
            auth=auth,
            headers={"Content-Type": "application/json", "Accept": "application/json"},
        )

    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> "MochiClient":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()

    def create_deck(self, deck_name: str) -> str:
        response = self._client.post("/decks", json={"name": deck_name})

        response.raise_for_status()
        return response.json()["id"]

    def create_card(self, word: Word, deck_id: str) -> dict:
        response = self._client.post(
            "/cards",
            json={
                "deck-id": deck_id,
                "content": word.root_word,
                "template-id": MOCHI_TEMPLATE_ID,
                "fields": {
                    "name": {
                        "id": "name",
                        "value": word.root_word,
                    },
                    "zEcruI99": {
                        "id": "zEcruI99",
                        "value": word.english_translation,
                    },
                    "vMpbVk0R": {
                        "id": "vMpbVk0R",
                        "value": word.romanization,
                    },
                    "3KahNdeW": {
                        "id": "3KahNdeW",
                        "value": word.cefr_level,
                    },
                    "BKn8g7Px": {
                        "id": "BKn8g7Px",
                        "value": str(word.word_frequency),
                    },
                },
            },
        )

        if response.status_code == 200:
            logger.info("Created new card '%s'", word.root_word)
        else:
            logger.error(
                "Failed to create card '%s': %s", word.root_word, response.text
            )

        return response.json()
