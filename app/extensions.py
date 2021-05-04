# import redis
from .mpdservice import MPDService

from app import settings
# from smbus2 import SMBus

# bus = SMBus(1)  # Open i2c bus for read and write
mpd_client = MPDService(settings.MPD_HOST, settings.MPD_PORT)  # Init MPD client
# redis_client = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)
