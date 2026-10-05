from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from .worker import busca_arq
from .process import Processo
from .ready_queue import FilaProntos

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

    fila_prontos = FilaProntos()
    for pid, caminho_arq in enumerate(arquivos, start=1):
        processo = Processo(
            pid=pid,
            arquivo=caminho_arq
        )

        fila_prontos.adicionar(processo)


    resultado = []

    with ThreadPoolExecutor(
        max_workers=n_threads
    ) as executor:
        futuros = [
            executor.submit(
                executar_processo,
                fila_prontos,
                tipo_busca,
                termo_busca
            )
            for _ in arquivos
        ]
        for futuro in futuros:
            equivalente = futuro.result()

            if resultado:
                resultado.append(equivalente)

def executar_processo(
    fila_prontos,
    tipo_busca,
    termo_busca
):
    processo = fila_prontos.proximo()

    try:
        resultado = busca_arq(
            processo.arquivo,
            tipo_busca,
            termo_busca
        )

        return resultado

    finally:
        fila_prontos.concluir(processo)