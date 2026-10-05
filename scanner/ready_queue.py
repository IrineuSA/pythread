from queue import Queue
from .process import Processo, EstadoProcesso

class FilaProntos:
    def __init__(self,gerenciador):
        self.fila = Queue()
        self.gerenciador = gerenciador

    def adicionar(self, processo: Processo):
        self.gerenciador.alterar_estado(
            processo,
            EstadoProcesso.READY
        )
        self.fila.put(processo)

    def proximo(self) -> Processo:
        processo = self.fila.get()
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