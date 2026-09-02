"""
Holaho - Configuration & Settings Manager
Persists user options, hotkeys, audio memo paths, and widget geometry.
"""

import os
import json
from pathlib import Path
from typing import Dict, Any

APP_DIR = Path(__file__).parent.resolve()
DATA_DIR = APP_DIR / "data"
MEMOS_DIR = DATA_DIR / "memos"
LOGS_DIR = APP_DIR / "logs"

DATA_DIR.mkdir(parents=True, exist_ok=True)
MEMOS_DIR.mkdir(parents=True, exist_ok=True)
LOGS_DIR.mkdir(parents=True, exist_ok=True)

CONFIG_FILE = DATA_DIR / "holaho_settings.json"

DEFAULT_SETTINGS = {
    "hotkey_widget": "Ctrl+Alt+H",
    "hotkey_mute": "Ctrl+Alt+M",
    "widget_position": [120, 120],
    "always_on_top": True,
    "theme": "vibrant_dark",
    "auto_play_new_memo": True,
    "volume_step": 5,
    "memos_folder": str(MEMOS_DIR)
}


class ConfigManager:
    def __init__(self, config_path: Path = CONFIG_FILE):
        self.config_path = config_path
        self.settings = DEFAULT_SETTINGS.copy()
        self.load()

    def load(self):
        if self.config_path.exists():
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    saved = json.load(f)
                    self.settings.update(saved)
            except Exception as e:
                print(f"[Holaho.Config] Failed to load settings: {e}")

    def save(self):
        try:
            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump(self.settings, f, indent=2)
        except Exception as e:
            print(f"[Holaho.Config] Failed to save settings: {e}")

    def get(self, key: str, default=None):
        return self.settings.get(key, default)

    def set(self, key: str, value: Any):
        self.settings[key] = value
        self.save()
