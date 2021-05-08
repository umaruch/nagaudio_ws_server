import json
import os
from app.extensions import mpd_client, redis_client


async def device_information():
    """
    Возвращает полную информацию об устройстве
    """
    device_name = redis_client.get("device_name")
    mpd_information = await mpd_client.stats()

    mpd_information["device_name"] = device_name

    return json.dumps(mpd_information)


async def update_device_name(args_dict):
    """
    Функция принимает имя устройства и обновляет файл и данные в редис
    """
    name = args_dict["name"]
    with open("device.name", "w") as f:
        f.write(name)

    redis_client.set("device_name", name)


async def reboot_device(args_dict=None):
    """
    Перезагрузка устройства
    """
    # os.system("sudo reboot") Для начала надо дать превилегии, будет лучше так как система корректно
    # закроет запущенные процессы
    os.system("systemctl reboot -i")  # Временное решение
