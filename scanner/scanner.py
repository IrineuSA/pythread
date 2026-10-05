from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from .worker import busca_arq
from .process import Processo
from .ready_queue import FilaProntos
from .process_manager import GerenciadorProcessos

import threading

def busca_pasta(
    pasta: str,
    tipo_busca: str,
    termo_busca: str,
    n_threads: int,
    max_io: int = None
) -> dict:
    arquivos = [
        caminho
        for caminho in Path(pasta).rglob("*")
        if caminho.is_file()
    ]

    gerenciador = GerenciadorProcessos()
    
    fila_prontos = FilaProntos(
    gerenciador
    )
    
    if max_io is None:
        max_io = n_threads
    semaforo_io =   threading.Semaphore(
        max_io
    )
    

    for pid, caminho_arq in enumerate(arquivos, start=1):
        processo = Processo(
            pid=pid,
            arquivo=caminho_arq
        )
        gerenciador.adicionar(processo)
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
                termo_busca,
                semaforo_io
            )
            for _ in arquivos
        ]
        for futuro in futuros:
            equivalente = futuro.result()

            if equivalente:
                resultado.append(equivalente)
    
    return {
        "matches": resultado,
        "arquivos pesquisados": len(arquivos)
    }

def executar_processo(
    fila_prontos,
    tipo_busca,
    termo_busca,
    semaforo_io
):
    processo = fila_prontos.proximo()

    try:
        with semaforo_io:
            encontrado = busca_arq(
                processo.arquivo,
                tipo_busca,
                termo_busca
            )
        if encontrado:
            return processo.arquivo

        return None

    finally:
        fila_prontos.concluir(processo)