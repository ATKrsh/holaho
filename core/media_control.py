"""
Holaho - Media Control & System Volume Helper
Simulates Win32 media key events for system-wide playback and volume control.
"""

import sys
import ctypes
import logging

logger = logging.getLogger("Holaho.MediaControl")

VK_MEDIA_NEXT_TRACK = 0xB0
VK_MEDIA_PREV_TRACK = 0xB1
VK_MEDIA_STOP = 0xB2
VK_MEDIA_PLAY_PAUSE = 0xCD
VK_VOLUME_MUTE = 0xAD
VK_VOLUME_DOWN = 0xAE
VK_VOLUME_UP = 0xAF

KEYEVENTF_KEYUP = 0x0002


class MediaController:
    """Sends Win32 keybd_event calls for global media control."""

    @staticmethod
    def _send_key(vk_code: int):
        if sys.platform == "win32":
            try:
                ctypes.windll.user32.keybd_event(vk_code, 0, 0, 0)
                ctypes.windll.user32.keybd_event(vk_code, 0, KEYEVENTF_KEYUP, 0)
            except Exception as e:
                logger.error(f"Error sending VK key {hex(vk_code)}: {e}")

    @classmethod
    def play_pause(cls):
        logger.info("Triggered Media Play/Pause")
        cls._send_key(VK_MEDIA_PLAY_PAUSE)

    @classmethod
    def next_track(cls):
        logger.info("Triggered Media Next Track")
        cls._send_key(VK_MEDIA_NEXT_TRACK)

    @classmethod
    def prev_track(cls):
        logger.info("Triggered Media Previous Track")
        cls._send_key(VK_MEDIA_PREV_TRACK)

    @classmethod
    def toggle_mute(cls):
        logger.info("Triggered Volume Mute")
        cls._send_key(VK_VOLUME_MUTE)

    @classmethod
    def volume_up(cls):
        logger.info("Triggered Volume Up")
        cls._send_key(VK_VOLUME_UP)

    @classmethod
    def volume_down(cls):
        logger.info("Triggered Volume Down")
        cls._send_key(VK_VOLUME_DOWN)
