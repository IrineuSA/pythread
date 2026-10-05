from dataclasses import dataclass
from pathlib import Path

from enum import Enum

class EstadoProcesso(Enum):
    NEW = "NEW"
    READY = "READY"
    RUNNING = "RUNNING"
    TERMINATED = "TERMINATED"

@dataclass
class Processo:
    pid: int
    arquivo: Path
    estado: EstadoProcesso = EstadoProcesso.NEW

    