from dataclasses import dataclass
from pathlib import Path

from enum import Enum

class EstadoProcesso(Enum):
    NEW = "NEW"
    READY = "READY"
    RUNNING = "RUNNING"
    WAITING = "WAITING"
    TERMINATED = "TERMINATED"

@dataclass
class Processo:
    pid: int
    arquivo: Path
    estado: EstadoProcesso = EstadoProcesso.NEW
    ordem_despacho: int | None = None
    tempo_chegada: float | None = None
    tempo_conclusao: float | None = None

    