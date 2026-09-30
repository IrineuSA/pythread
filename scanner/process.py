from dataclasses import dataclass
from pathlib import Path

@dataclass
class Processo:
    pid: int
    arquivo: Path
    estado: str = "NEW"