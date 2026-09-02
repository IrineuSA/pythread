import time 
from .scanner import busca_pasta

def benchmark_threads(
    pasta: str,
    tipo_busca: str,
    termo_busca: str,
    n_threads: list[int]
) -> list[dict]:
        resultado = []