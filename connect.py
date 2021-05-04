"""
Процесс, отдающий клиентам данные, необходимые для подключения

Статус: вроде готово, но пока не запускал ни разу
"""
import redis
import socket
import json

from app.settings import REDIS_HOST, REDIS_PORT

redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT
)

broadcast_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
broadcast_server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
broadcast_server.bind(("", 65000))


def _get_information():
    """
    Подготовка информации об устройстве для отправки клиенту
    """
    device_name = redis_client.get("device_name")
    mac_addr = redis_client.get("mac_address")
    ip_addr = redis_client.get("ip_address")

    device_data = json.dumps({
        "device_name": device_name,
        "mac_addr": mac_addr,
        "ip_addr": ip_addr
    })

    return device_data.encode()


while True:
    data, addr = broadcast_server.recvfrom(1024)
    data = _get_information()
    broadcast_server.sendto(data, addr)



