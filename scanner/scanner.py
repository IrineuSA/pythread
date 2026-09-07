from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from .worker import busca_arq

def busca_pasta(
    pasta: str,
    tipo_busca: str,
    termo_busca: str,
    n_threads: int
) -> dict:
    arquivos = [
        caminho
        for caminho in Path(pasta).rglob("*")
        if caminho.is_file()
    ]

    resultado = []

    with ThreadPoolExecutor(
        max_workers=n_threads
    ) as executor:
        futuros = [
            executor.submit(
                busca_arq,
                caminho_arq,
                tipo_busca,
                termo_busca
            )
            for caminho_arq in arquivos
        ]
        for caminho_arq, futuro in zip(
            arquivos,
            futuros
        ):
            if futuro.result():
                resultado.append(caminho_arq)

    return {
        "matches": resultado,
        "arquivos pesquisados": len(arquivos)
    }
