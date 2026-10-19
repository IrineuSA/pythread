from pathlib import Path
from tempfile import TemporaryDirectory

from scanner.process import Processo
from scanner.process_manager import GerenciadorProcessos
from scanner.ready_queue import FilaProntos


def testar(algoritmo):
    with TemporaryDirectory() as pasta:
        pasta = Path(pasta)

        tamanhos = [5000, 100, 3000, 500]

        gerenciador = GerenciadorProcessos()

        fila = FilaProntos(
            gerenciador,
            algoritmo=algoritmo
        )

        for pid, tamanho in enumerate(tamanhos, start=1):
            arquivo = pasta / f"arquivo{pid}.txt"
            arquivo.write_bytes(b"A" * tamanho)

            processo = Processo(
                pid=pid,
                arquivo=arquivo
            )

            gerenciador.adicionar(processo)
            fila.adicionar(processo)

        ordem = []

        print(
            f"{algoritmo} - Fila pendente:",
            fila.obter_fila()
        )

        for _ in tamanhos:
            processo = fila.proximo()

            print(
                f"despacho #{processo.ordem_despacho} | "
                f"PID: {processo.pid} | "
                f"Tamanho: {processo.arquivo.stat().st_size} bytes"
            )

            ordem.append(processo.pid)
            fila.concluir(processo)
            tempo_total = (
                processo.tempo_conclusao
                - processo.tempo_chegada
            )

            print(
                f"PID {processo.pid} | "
                f"Ordem {processo.ordem_despacho} | "
                f"Tempo: {tempo_total * 1000:.3f} ms"
            )

        return ordem


print("FCFS:", testar("FCFS"))
print("SJF: ", testar("SJF"))