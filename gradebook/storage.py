"""Persistence layer: load and save gradebook data as JSON."""

import json
import logging
import os

logger = logging.getLogger(__name__)

DEFAULT_PATH = "data/gradebook.json"


def load_data(path: str = DEFAULT_PATH) -> dict:
    """Load gradebook data from a JSON file.

    Returns an empty structure if the file does not exist.
    Shows a helpful message if the file is corrupted.
    """
    empty = {"students": [], "courses": [], "enrollments": []}
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            logger.info("Data loaded successfully from %s", path)
            return data
    except FileNotFoundError:
        logger.info("No data file found at %s. Starting fresh.", path)
        return empty
    except json.JSONDecodeError as e:
        logger.error("Could not parse JSON from %s: %s", path, e)
        print(f"  Warning: '{path}' is corrupted and could not be read. Starting fresh.")
        return empty


def save_data(data: dict, path: str = DEFAULT_PATH) -> None:
    """Save gradebook data to a JSON file.

    Creates the directory automatically if it does not exist.
    """
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
            logger.info("Data saved successfully to %s", path)
    except OSError as e:
        logger.error("Failed to save data to %s: %s", path, e)
        print(f"  Error: Could not save data — {e}")