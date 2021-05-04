from typing import Dict, Union
from pydantic import BaseModel, ValidationError


class Command(BaseModel):
    """
    Класс команды, которую отправляют клиенты по WebSocket
    """
    cmd: str
    args: Dict[str, Union[int, str]] = None
