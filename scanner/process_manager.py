import threading
from .process import Processo, EstadoProcesso

class GerenciadorProcessos:
    def __init__(self):
        self.processos = []
        self.lock = threading.Lock()

    def adicionar(self, processo: Processo):
        with self.lock:
            self.processos.append(processo)

    def alterar_estado(
        self,
        processo: Processo,
        estado: EstadoProcesso
    ):
        with self.lock:
            processo.estado = estado

    def obter_por_estado(
        self,
        estado: EstadoProcesso
    ):
        with self.lock:
            return [
                processo
                for processo in self.processos
                if processo.estado == estado
            ]

    def obter_todos(self):
        with self.lock:
            return list(self.processos)