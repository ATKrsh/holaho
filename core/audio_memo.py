"""
Holaho - Audio Voice Memo Core Utility
Manages quick voice recording files, playback metadata, and memo indexing.
"""

import os
import wave
import struct
import math
import time
import logging
from pathlib import Path
from typing import List, Dict, Any

logger = logging.getLogger("Holaho.AudioMemo")


class AudioMemoManager:
    """Manages audio recording files and playback info for Holaho."""

    def __init__(self, memos_dir: Path):
        self.memos_dir = memos_dir
        self.memos_dir.mkdir(parents=True, exist_ok=True)

    def list_memos(self) -> List[Dict[str, Any]]:
        """Return list of voice memo files sorted by creation time."""
        memos = []
        for file in self.memos_dir.glob("*.wav"):
            stat = file.stat()
            memos.append({
                "name": file.stem,
                "path": str(file),
                "size_kb": round(stat.st_size / 1024, 1),
                "created": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(stat.st_mtime))
            })
        return sorted(memos, key=lambda x: x["created"], reverse=True)

    def create_sample_memo(self, name: str = "VoiceMemo_Sample") -> str:
        """Create a synthetic 1-second sine wave WAV file for testing/demo."""
        filename = f"{name}_{int(time.time())}.wav"
        file_path = self.memos_dir / filename

        sample_rate = 44100
        duration = 1.0  # seconds
        frequency = 440.0  # A4 note

        n_samples = int(sample_rate * duration)

        with wave.open(str(file_path), "w") as wav_file:
            wav_file.setnchannels(1)  # Mono
            wav_file.setsampwidth(2)  # 16-bit
            wav_file.setframerate(sample_rate)

            for i in range(n_samples):
                sample = int(32767.0 * 0.5 * math.sin(2.0 * math.pi * frequency * (i / sample_rate)))
                wav_file.writeframes(struct.pack("<h", sample))

        logger.info(f"Created sample audio memo at {file_path}")
        return str(file_path)

    def delete_memo(self, file_path: str) -> bool:
        """Delete an audio memo file."""
        try:
            p = Path(file_path)
            if p.exists():
                p.unlink()
                logger.info(f"Deleted audio memo: {file_path}")
                return True
        except Exception as e:
            logger.error(f"Error deleting memo {file_path}: {e}")
        return False
