import logging
import redis
from .mpdservice import MPDService

from app import config


# from smbus2 import SMBus

# bus = SMBus(1)  # Open i2c bus for read and write

mpd_client = MPDService(config.MPD_HOST, config.MPD_PORT)  # Init MPD client

# Подключение к Redis и проверка соединения
redis_client = redis.Redis(host=config.REDIS_HOST, port=config.REDIS_PORT, db=0)
try:
    redis_client.set("init", "test")
except redis.exceptions.ConnectionError:
    logging.error("Connection to Redis failed")
    exit()
