from scanner.process import EstadoProcesso
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from .worker import busca_arq
from .process import Processo, EstadoProcesso
from .ready_queue import FilaProntos
from .process_manager import GerenciadorProcessos

import threading
import time

def busca_pasta(
    pasta: str,
    tipo_busca: str,
    termo_busca: str,
    n_threads: int,
    max_io: int = None,
    processo_callback=None,
    algoritmo: str="FCFS",
    delay_ms: int = 0,
    fila_callback=None
) -> dict:
    arquivos = [
        caminho
        for caminho in Path(pasta).rglob("*")
        if caminho.is_file()
    ]

    gerenciador = GerenciadorProcessos(
        callback=processo_callback
    )
    
    fila_prontos = FilaProntos(
    gerenciador,
    algoritmo=algoritmo,
    fila_callback=fila_callback
    )

    if delay_ms < 0:
        raise ValueError(
            "Atraso na simulaçao não pode ser negativo"
        )
    
    if max_io is None:
        max_io = 1
    if max_io < 1:
        raise ValueError(
            "Limite de I/O deve ser maior que 0"
        )
    semaforos_pasta={
        diretorio: threading.Semaphore(max_io)
        for diretorio in {arquivo.parent for arquivo in arquivos}
    }
    
    

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
                semaforos_pasta,
                gerenciador,
                delay_ms
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
    semaforos_pasta,
    gerenciador,
    delay_ms=0
):
    processo = fila_prontos.proximo()
    diretorio = processo.arquivo.parent
    semaforo_io = semaforos_pasta[diretorio]
    getSemaforo = False

    try:
        getSemaforo = semaforo_io.acquire(
            blocking=False
        )
        if not getSemaforo:
            gerenciador.alterar_estado(
                processo,
                EstadoProcesso.WAITING
            )
            semaforo_io.acquire()
            getSemaforo=True

        gerenciador.alterar_estado(
            processo,
            EstadoProcesso.RUNNING
        )
    
        encontrado = busca_arq(
            processo.arquivo,
            tipo_busca,
            termo_busca
        )

        if delay_ms > 0:
            time.sleep(delay_ms/1000)

        if encontrado:
            return processo.arquivo
        
        return None

    finally:
        if getSemaforo:
            semaforo_io.release()
        fila_prontos.concluir(
            processo
        )