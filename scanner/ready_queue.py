from queue import Queue, PriorityQueue
from .process import Processo, EstadoProcesso

class FilaProntos:
    def __init__(self,gerenciador,algoritmo="FCFS"):
        if algoritmo not in ("FCFS", "SJF"):
            raise ValueError(
                f"Algoritmo não suportado: {algoritmo}"
            )
        self.algoritmo=algoritmo
        self.gerenciador=gerenciador
        if algoritmo == "FCFS":
            self.fila=Queue()
        else:
            self.fila=PriorityQueue()

    def adicionar(self, processo: Processo):
        self.gerenciador.alterar_estado(
            processo,
            EstadoProcesso.READY
        )
        if self.algoritmo=="FCFS":
            self.fila.put(processo)
        else:
            tamanho=processo.arquivo.stat().st_size
            self.fila.put(
                (tamanho,processo.pid,processo)
            )

    def proximo(self) -> Processo:
        if self.algoritmo=="FCFS":
            processo = self.fila.get()
        else:
            _,_,processo=self.fila.get()
        self.gerenciador.alterar_estado(
            processo,
            EstadoProcesso.RUNNING
        )
        return processo

    def concluir(self, processo: Processo):
        self.gerenciador.alterar_estado(
            processo,
            EstadoProcesso.TERMINATED
        )
        self.fila.task_done()

    def vazia(self) -> bool:
        return self.fila.empty()

    def tamanho(self) -> int:
        return self.fila.qsize()