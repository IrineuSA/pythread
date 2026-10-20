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

    monitor_lock = threading.Lock()
    operacoes_ativas = {
        pasta: 0 for pasta in semaforos_pasta
    }
    
    maximo_simultaneo = {
        pasta: 0 for pasta in semaforos_pasta
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
                delay_ms,
                monitor_lock,
                operacoes_ativas,
                maximo_simultaneo
            )
            for _ in arquivos
        ]
        for futuro in futuros:
            equivalente = futuro.result()

            if equivalente:
                resultado.append(equivalente)

    processos = gerenciador.obter_todos()
    tempos_retorno = [
        processo.tempo_conclusao - processo.tempo_chegada
        for processo in processos
        if (
            processo.tempo_chegada is not None
            and processo.tempo_conclusao is not None
        )
    ]

    if tempos_retorno:
        tempo_medio_retorno = (
            sum(tempos_retorno) / len(tempos_retorno)
        )
    else:
        tempo_medio_retorno = 0.0

    print("\n=== DIAGNOSTICO DE SINCRONIZAÇAO ===")
    for pasta,maximo in maximo_simultaneo.items():
        print(
            f"Pasta: {pasta.name} | "
            f"Máximo simultaneo: {maximo} | "
            f"Limite: {max_io}"
        )

        assert maximo <= max_io, (
            f"Limite de sincronizacao excedido: {pasta}"
        )

    print(
        "Tempo medio de retorno: "
        f"{tempo_medio_retorno * 1000:.3f} ms"
    )
    
    return {
        "matches": resultado,
        "arquivos pesquisados": len(arquivos),
        "tempo medio retorno": tempo_medio_retorno
    }

def executar_processo(
    fila_prontos,
    tipo_busca,
    termo_busca,
    semaforos_pasta,
    gerenciador,
    delay_ms,
    monitor_lock,
    operacoes_ativas,
    maximo_simultaneo
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

        with monitor_lock:
            operacoes_ativas[diretorio] += 1
                
            maximo_simultaneo[diretorio] = max(
                maximo_simultaneo[diretorio],
                operacoes_ativas[diretorio]
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
            with monitor_lock:
                operacoes_ativas[diretorio] -= 1
            semaforo_io.release()
        fila_prontos.concluir(processo)
    
 