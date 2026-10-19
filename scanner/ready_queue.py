from queue import Queue, PriorityQueue
from .process import Processo, EstadoProcesso

class FilaProntos:
    def __init__(self,gerenciador,algoritmo="FCFS",fila_callback=None):
        if algoritmo not in ("FCFS", "SJF"):
            raise ValueError(
                f"Algoritmo não suportado: {algoritmo}"
            )
        self.algoritmo=algoritmo
        self.gerenciador=gerenciador
        self.fila_callback = fila_callback
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
        self.notificar_fila()

    def proximo(self) -> Processo:
        if self.algoritmo=="FCFS":
            processo = self.fila.get()
        else:
            _,_,processo=self.fila.get()
        self.notificar_fila()
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

    def obter_fila(self):
        with self.fila.mutex:
            itens = list(self.fila.queue)

        if self.algoritmo == "FCFS":
            return [processo.pid for processo in itens]
        
        itens.sort(
            key=lambda item: (item[0],item[1])
        )
        return [
            processo.pid
            for _,_, processo in itens
        ]

    def notificar_fila(self):
        if self.fila_callback is not None:
            self.fila_callback(self.obter_fila())