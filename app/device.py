import json
import platform
import netifaces
from app.extensions import redis_client, mpd_client


def _update_mac(interface):
    mac_address = netifaces.ifaddresses(interface)[netifaces.AF_LINK][0]['addr']
    redis_client.set("mac_address", mac_address)


def _update_ip(interface):
    ip_address = netifaces.ifaddresses(interface)[netifaces.AF_INET][0]['addr']
    redis_client.set("ip_address", ip_address)


def _update_device_name():
    try:
        with open("device.name", "r") as f:
            device_name = f.read()
            redis_client.set("device_name", device_name)
    except FileNotFoundError:
        with open("device.name", "w") as f:
            device_name = platform.node()
            f.write(device_name)
            redis_client.set("device_name", device_name)


def init_device():
    # Получение имени устройства
    _update_device_name()
    # Получение стандартного интерфейса подключения к сети
    default_interface = netifaces.gateways()['default'][netifaces.AF_INET][1]
    # Получение MAC адреса устройства
    _update_mac(default_interface)
    # Получнение IP адреса устройства
    _update_ip(default_interface)


async def device_information():
    """
    Возвращает полную информацию об устройстве
    TODO Добавить текущий профиль устройства когда прикрутится
    """
    device_name = redis_client.get("device_name")
    mpd_information = await mpd_client.stats()

    mpd_information["device_name"] = device_name

    return json.dumps(mpd_information)
