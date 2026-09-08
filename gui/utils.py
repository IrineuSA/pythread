import sys
from pathlib import Path


def obter_diretorio_app() -> Path:

    if getattr(sys, "frozen", False):
        return Path(
            sys.executable
        ).resolve().parent

    return (
        Path(__file__)
        .resolve()
        .parent
        .parent
    )