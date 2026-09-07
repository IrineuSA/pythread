import threading
from tkinter import ttk
from tkinter import messagebox

from scanner.benchmark import (
    benchmark_threads,
    melhor_resultado
)
from visual.graficos import gerar_graficos

class BenchmarkTab(ttk.Frame):

    def __init__(self, parent):
        super().__init__(
            parent,
            padding=10
        )
        self._criar_tabela()

    def _criar_tabela(self):

        colunas = (
            "threads",
            "tempo",
            "arquivos",
            "encontrados",
            "throughput"
        )

        self.tree = ttk.Treeview(
            self,
            columns=colunas,
            show="headings"
        )
        self.tree.heading(
            "threads",
            text="Threads"
        )
        self.tree.heading(
            "tempo",
            text="Tempo"
        )
        self.tree.heading(
            "arquivos",
            text="Arquivos"
        )
        self.tree.heading(
            "encontrados",
            text="Encontrados"
        )
        self.tree.heading(
            "throughput",
            text="Arquivos/s"
        )
        self.tree.pack(
            fill="both",
            expand=True
        )

    def executar(
        self,
        config,
        graph_dir,
        on_complete=None
    ):

        thread = threading.Thread(
            target=self._executar_thread,
            args=(
                config,
                graph_dir,
                on_complete
            ),
            daemon=True
        )
        thread.start()
