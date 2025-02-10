"""
This module contains helper functions for the bot.
"""
import json
import os


def load_jsonl(file_path, default_value):
    """
    Loads JSON data from a file and returns it.
    """
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            try:
                if isinstance(default_value, list):
                    return list({item for line in f for item in json.loads(line)})
                elif isinstance(default_value, dict):
                    return {k: v for line in f for k, v in json.loads(line).items()}
            except json.JSONDecodeError:
                return default_value
    
    return default_value
