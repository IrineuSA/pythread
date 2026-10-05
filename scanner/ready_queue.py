from queue import Queue
from .process import Processo, EstadoProcesso

class FilaProntos:
    def __init__(self):
        self.fila = Queue()

    def adicionar(self, processo: Processo):
        processo.estado = EstadoProcesso.READY
        self.fila.put(processo)

    def proximo(self) -> Processo:
        processo = self.fila.get()
        processo.estado = EstadoProcesso.RUNNING
        return processo

    def concluir(self, processo: Processo):
        processo.estado = EstadoProcesso.TERMINATED
        self.fila.task_done()

    def vazia(self) -> bool:
        return self.fila.empty()

    def tamanho(self) -> int:
        return self.fila.qsize()